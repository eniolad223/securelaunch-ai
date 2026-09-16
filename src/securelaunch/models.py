"""Validated data structures shared by the gateway, interface, and tests."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    """Reject unexpected fields instead of silently accepting them."""

    model_config = ConfigDict(extra="forbid")


class Decision(str, Enum):
    ALLOW = "allow"
    MASK = "mask"
    BLOCK = "block"
    MANUAL_FALLBACK = "manual_fallback"


class ReasonCode(str, Enum):
    ALLOW_CLEAN = "ALLOW_CLEAN"
    ALLOW_MASKED = "ALLOW_MASKED"
    BLOCK_RESTRICTED_DATA = "BLOCK_RESTRICTED_DATA"
    BLOCK_PROMPT_MANIPULATION = "BLOCK_PROMPT_MANIPULATION"
    BLOCK_INPUT_SIZE_LIMIT = "BLOCK_INPUT_SIZE_LIMIT"
    BLOCK_FINAL_PAYLOAD_GATE = "BLOCK_FINAL_PAYLOAD_GATE"
    MANUAL_KILL_SWITCH = "MANUAL_KILL_SWITCH"
    MANUAL_PROVIDER_TIMEOUT = "MANUAL_PROVIDER_TIMEOUT"
    MANUAL_PROVIDER_FAILURE = "MANUAL_PROVIDER_FAILURE"
    MANUAL_INVALID_PROVIDER_RESPONSE = "MANUAL_INVALID_PROVIDER_RESPONSE"
    MANUAL_UNKNOWN_CATEGORY = "MANUAL_UNKNOWN_CATEGORY"


class TraceStatus(str, Enum):
    PASS = "pass"
    CHANGED = "changed"
    BLOCKED = "blocked"
    FAILED = "failed"
    NOT_RUN = "not_run"


class FindingAction(str, Enum):
    MASK = "mask"
    BLOCK = "block"


class SecurityPolicy(StrictModel):
    policy_id: str
    version: str
    kill_switch_enabled: bool
    allowed_ticket_fields: list[str]
    provider_payload_fields: list[str]
    mask_data_types: list[str]
    block_data_types: list[str]
    prompt_manipulation_phrases: list[str]
    allowed_categories: list[str]
    maximum_ticket_characters: int = Field(gt=0)
    maximum_response_characters: int = Field(gt=0)


class Ticket(StrictModel):
    scenario_id: str
    ticket_id: str
    tenant_id: str
    subject: str
    description: str
    customer_email: str | None = None
    account_reference: str | None = None
    attachment_names: list[str] = Field(default_factory=list)


class DetectionFinding(StrictModel):
    """A safe description of a match; the sensitive value is deliberately omitted."""

    rule_id: str
    data_type: str
    action: FindingAction
    start: int = Field(ge=0)
    end: int = Field(gt=0)


class InspectionResult(StrictModel):
    protected_text: str
    findings: list[DetectionFinding]
    prompt_manipulation_detected: bool


class TraceStep(StrictModel):
    step_number: int = Field(gt=0)
    name: str
    status: TraceStatus
    explanation: str
    safe_details: dict[str, Any] = Field(default_factory=dict)


class ProviderResponse(StrictModel):
    summary: str
    category: str


class ProviderPayload(StrictModel):
    request_id: str
    subject: str
    ticket_text: str
    allowed_categories: list[str]


class GatewayResult(StrictModel):
    decision: Decision
    reason_codes: list[ReasonCode]
    provider_invoked: bool = False
    provider_payload: ProviderPayload | None = None
    provider_response: ProviderResponse | None = None
    playbook: "Playbook | None" = None
    trace_steps: list[TraceStep]


class ScenarioTestSetup(StrictModel):
    response_mode: str
    kill_switch_enabled: bool = False


class ScenarioExpectedResult(StrictModel):
    decision: Decision
    provider_invoked: bool


class ScenarioTraceability(StrictModel):
    risk_ids: list[str]
    safeguard_ids: list[str]
    evidence_ids: list[str]
    release_gate_ids: list[str]


class Scenario(StrictModel):
    scenario_id: str
    version: str
    title: str
    purpose: str
    ticket: Ticket
    test_setup: ScenarioTestSetup
    expected_result: ScenarioExpectedResult
    traceability: ScenarioTraceability


class Playbook(StrictModel):
    playbook_id: str
    version: str
    title: str
    category: str
    approved_steps: list[str]
    owner: str
    review_date: str


class EvidenceReceipt(StrictModel):
    receipt_id: str
    created_at_utc: str
    scenario_id: str
    scenario_version: str
    policy_id: str
    policy_version: str
    decision: Decision
    reason_codes: list[ReasonCode]
    provider_invoked: bool
    risk_ids: list[str]
    safeguard_ids: list[str]
    evidence_ids: list[str]
    release_gate_ids: list[str]
    safe_test_fingerprint_sha256: str
    limitations: list[str]


# Resolve the Playbook reference after every model class has been defined.
GatewayResult.model_rebuild()
