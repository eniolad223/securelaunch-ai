"""Create sanitized, reproducible evidence receipts for synthetic gateway runs."""

import hashlib
import json
from datetime import datetime, timezone

from .models import EvidenceReceipt, GatewayResult, Scenario, SecurityPolicy


EVIDENCE_LIMITATIONS = [
    "This receipt covers one fixed synthetic scenario, not production customer data.",
    "HTTPX MockTransport did not contact or evaluate a real AI provider.",
    "The SHA-256 fingerprint identifies the tested material but is not a digital signature.",
]


def _fingerprint_material(
    scenario: Scenario,
    policy: SecurityPolicy,
    result: GatewayResult,
) -> str:
    material = {
        "scenario": scenario.model_dump(mode="json"),
        "policy_id": policy.policy_id,
        "policy_version": policy.version,
        "decision": result.decision.value,
        "reason_codes": [reason.value for reason in result.reason_codes],
        "provider_invoked": result.provider_invoked,
    }
    canonical = json.dumps(material, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def create_evidence_receipt(
    scenario: Scenario,
    policy: SecurityPolicy,
    result: GatewayResult,
    created_at: datetime | None = None,
) -> EvidenceReceipt:
    current_time = created_at or datetime.now(timezone.utc)
    fingerprint = _fingerprint_material(scenario, policy, result)
    return EvidenceReceipt(
        receipt_id=f"EVR-{scenario.scenario_id}-{fingerprint[:12].upper()}",
        created_at_utc=current_time.astimezone(timezone.utc).isoformat(),
        scenario_id=scenario.scenario_id,
        scenario_version=scenario.version,
        policy_id=policy.policy_id,
        policy_version=policy.version,
        decision=result.decision,
        reason_codes=result.reason_codes,
        provider_invoked=result.provider_invoked,
        risk_ids=scenario.traceability.risk_ids,
        safeguard_ids=scenario.traceability.safeguard_ids,
        evidence_ids=scenario.traceability.evidence_ids,
        release_gate_ids=scenario.traceability.release_gate_ids,
        safe_test_fingerprint_sha256=fingerprint,
        limitations=EVIDENCE_LIMITATIONS,
    )
