"""Deterministic text normalization, sensitive-data inspection, and masking."""

import re
import unicodedata
from dataclasses import dataclass

from .models import (
    DetectionFinding,
    FindingAction,
    InspectionResult,
    SecurityPolicy,
)


ZERO_WIDTH_CHARACTERS = re.compile(r"[\u200b-\u200f\u2060\ufeff]")
REPEATED_WHITESPACE = re.compile(r"[ \t]+")


@dataclass(frozen=True)
class DetectionRule:
    rule_id: str
    data_type: str
    pattern: re.Pattern[str]


RULES = (
    DetectionRule(
        "DET-SSN-01",
        "social_security_number",
        re.compile(
            r"(?i)(?:\bssn\b|social\s+security(?:\s+number)?)\s*(?:is\s*)?[:#-]?\s*"
            r"\d{3}[ .-]?\d{2}[ .-]?\d{4}\b"
            r"|\b(?!000|666|9\d{2})\d{3}[- ](?!00)\d{2}[- ](?!0000)\d{4}\b"
        ),
    ),
    DetectionRule(
        "DET-ROUTING-01",
        "routing_number",
        re.compile(r"(?i)\b(?:routing|aba)\s*(?:number|no\.?|#)?\s*[:#-]?\s*\d(?:[ .-]?\d){8}\b"),
    ),
    DetectionRule(
        "DET-BANK-01",
        "bank_account_number",
        re.compile(r"(?i)\bbank\s+account\s*(?:number|no\.?|#)?\s*[:#-]?\s*\d(?:[ .-]?\d){5,16}\b"),
    ),
    DetectionRule(
        "DET-CREDENTIAL-01",
        "credential",
        re.compile(r"(?i)\b(?:password|passcode|one[- ]time\s+code|otp)\s*[:=]\s*\S+"),
    ),
    DetectionRule(
        "DET-APIKEY-01",
        "api_key",
        re.compile(r"(?i)\b(?:api[-_ ]?key|secret[-_ ]?key)\s*[:=]\s*[A-Za-z0-9_\-]{8,}\b"),
    ),
    DetectionRule(
        "DET-EMAIL-01",
        "email_address",
        re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    ),
    DetectionRule(
        "DET-PHONE-01",
        "phone_number",
        re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)"),
    ),
    DetectionRule(
        "DET-ACCOUNTREF-01",
        "account_reference",
        re.compile(
            r"(?i)\b(?:account\s+(?:reference|ref)|customer\s+id)\s*[:#-]?\s*[A-Z0-9][A-Z0-9-]{4,29}\b"
        ),
    ),
)

CARD_CANDIDATE = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")


def normalize_text(text: str) -> str:
    """Make equivalent Unicode and spacing forms easier to inspect consistently."""

    normalized = unicodedata.normalize("NFKC", text)
    normalized = ZERO_WIDTH_CHARACTERS.sub("", normalized)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    return REPEATED_WHITESPACE.sub(" ", normalized).strip()


def _luhn_valid(candidate: str) -> bool:
    digits = [int(character) for character in candidate if character.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def _action_for(data_type: str, policy: SecurityPolicy) -> FindingAction | None:
    if data_type in policy.block_data_types:
        return FindingAction.BLOCK
    if data_type in policy.mask_data_types:
        return FindingAction.MASK
    return None


def _overlaps_existing(start: int, end: int, findings: list[DetectionFinding]) -> bool:
    return any(start < finding.end and end > finding.start for finding in findings)


def _find_sensitive_data(text: str, policy: SecurityPolicy) -> list[DetectionFinding]:
    findings: list[DetectionFinding] = []

    for rule in RULES:
        action = _action_for(rule.data_type, policy)
        if action is None:
            continue
        for match in rule.pattern.finditer(text):
            if not _overlaps_existing(match.start(), match.end(), findings):
                findings.append(
                    DetectionFinding(
                        rule_id=rule.rule_id,
                        data_type=rule.data_type,
                        action=action,
                        start=match.start(),
                        end=match.end(),
                    )
                )

    action = _action_for("payment_card_number", policy)
    if action is not None:
        for match in CARD_CANDIDATE.finditer(text):
            if _luhn_valid(match.group()) and not _overlaps_existing(match.start(), match.end(), findings):
                findings.append(
                    DetectionFinding(
                        rule_id="DET-CARD-01",
                        data_type="payment_card_number",
                        action=action,
                        start=match.start(),
                        end=match.end(),
                    )
                )

    return sorted(findings, key=lambda finding: (finding.start, finding.end))


def _mask_findings(text: str, findings: list[DetectionFinding]) -> str:
    protected = text
    maskable = [finding for finding in findings if finding.action == FindingAction.MASK]
    for finding in reversed(maskable):
        replacement = f"[MASKED_{finding.data_type.upper()}]"
        protected = protected[: finding.start] + replacement + protected[finding.end :]
    return protected


def inspect_text(text: str, policy: SecurityPolicy) -> InspectionResult:
    """Normalize text, identify configured sensitive types, and mask allowed types."""

    normalized = normalize_text(text)
    findings = _find_sensitive_data(normalized, policy)
    lowered = normalized.casefold()
    prompt_manipulation_detected = any(
        phrase.casefold() in lowered for phrase in policy.prompt_manipulation_phrases
    )
    return InspectionResult(
        protected_text=_mask_findings(normalized, findings),
        findings=findings,
        prompt_manipulation_detected=prompt_manipulation_detected,
    )
