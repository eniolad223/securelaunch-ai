"""Pre-provider security gateway for the LindenArc Signal prototype."""

from .inspection import inspect_text
from .models import (
    Decision,
    FindingAction,
    GatewayResult,
    Playbook,
    ProviderPayload,
    ReasonCode,
    SecurityPolicy,
    Ticket,
    TraceStatus,
    TraceStep,
)
from .provider import MockProviderAdapter, ProviderTimeoutError, ProviderUnavailableError
from .response_validation import ResponseValidationError, validate_provider_response


def _trace(
    number: int,
    name: str,
    status: TraceStatus,
    explanation: str,
    **safe_details: object,
) -> TraceStep:
    return TraceStep(
        step_number=number,
        name=name,
        status=status,
        explanation=explanation,
        safe_details=safe_details,
    )


def _stopped_result(
    decision: Decision,
    reason: ReasonCode,
    trace_steps: list[TraceStep],
) -> GatewayResult:
    return GatewayResult(
        decision=decision,
        reason_codes=[reason],
        provider_invoked=False,
        provider_payload=None,
        trace_steps=trace_steps,
    )


def prepare_provider_request(ticket: Ticket, policy: SecurityPolicy) -> GatewayResult:
    """Create an approved provider payload or stop safely before any API call."""

    trace_steps: list[TraceStep] = []
    trace_steps.append(
        _trace(
            1,
            "Receive synthetic ticket",
            TraceStatus.PASS,
            "The fixed synthetic scenario passed strict ticket-structure validation.",
            scenario_id=ticket.scenario_id,
        )
    )

    if policy.kill_switch_enabled:
        trace_steps.append(
            _trace(
                2,
                "Check Signal kill switch",
                TraceStatus.BLOCKED,
                "Signal is disabled, so the ticket must remain in the normal manual support process.",
                policy_version=policy.version,
            )
        )
        return _stopped_result(
            Decision.MANUAL_FALLBACK,
            ReasonCode.MANUAL_KILL_SWITCH,
            trace_steps,
        )

    trace_steps.append(
        _trace(
            2,
            "Check Signal kill switch",
            TraceStatus.PASS,
            "The versioned policy permits Signal processing.",
            policy_version=policy.version,
        )
    )

    excluded_fields = ["tenant_id"]
    if ticket.customer_email:
        excluded_fields.append("customer_email")
    if ticket.account_reference:
        excluded_fields.append("account_reference")
    if ticket.attachment_names:
        excluded_fields.append("attachment_names")
    trace_steps.append(
        _trace(
            3,
            "Minimize ticket fields",
            TraceStatus.CHANGED,
            "Tenant metadata, contact fields, account references, and attachments are excluded from the provider payload.",
            excluded_fields=excluded_fields,
            outbound_content_fields=["subject", "ticket_text"],
        )
    )

    combined_length = len(ticket.subject) + len(ticket.description)
    if combined_length > policy.maximum_ticket_characters:
        trace_steps.append(
            _trace(
                4,
                "Enforce input-size boundary",
                TraceStatus.BLOCKED,
                "The permitted text exceeds the policy limit and cannot enter Signal.",
                observed_characters=combined_length,
                maximum_characters=policy.maximum_ticket_characters,
            )
        )
        return _stopped_result(
            Decision.BLOCK,
            ReasonCode.BLOCK_INPUT_SIZE_LIMIT,
            trace_steps,
        )

    trace_steps.append(
        _trace(
            4,
            "Enforce input-size boundary",
            TraceStatus.PASS,
            "The permitted text is within the configured size boundary.",
            observed_characters=combined_length,
            maximum_characters=policy.maximum_ticket_characters,
        )
    )

    subject_result = inspect_text(ticket.subject, policy)
    description_result = inspect_text(ticket.description, policy)
    findings = subject_result.findings + description_result.findings
    finding_types = sorted({finding.data_type for finding in findings})

    if subject_result.prompt_manipulation_detected or description_result.prompt_manipulation_detected:
        trace_steps.append(
            _trace(
                5,
                "Inspect ticket content",
                TraceStatus.BLOCKED,
                "A configured prompt-manipulation phrase requires manual handling.",
                detected_types=finding_types,
                prompt_manipulation_detected=True,
            )
        )
        return _stopped_result(
            Decision.BLOCK,
            ReasonCode.BLOCK_PROMPT_MANIPULATION,
            trace_steps,
        )

    blocked_types = sorted(
        {
            finding.data_type
            for finding in findings
            if finding.action == FindingAction.BLOCK
        }
    )
    if blocked_types:
        trace_steps.append(
            _trace(
                5,
                "Inspect ticket content",
                TraceStatus.BLOCKED,
                "Restricted information was detected; no provider payload will be created.",
                detected_types=finding_types,
                blocked_types=blocked_types,
            )
        )
        return _stopped_result(
            Decision.BLOCK,
            ReasonCode.BLOCK_RESTRICTED_DATA,
            trace_steps,
        )

    masked_types = sorted(
        {
            finding.data_type
            for finding in findings
            if finding.action == FindingAction.MASK
        }
    )
    trace_steps.append(
        _trace(
            5,
            "Inspect ticket content",
            TraceStatus.CHANGED if masked_types else TraceStatus.PASS,
            "Configured lower-risk identifiers were masked."
            if masked_types
            else "No configured sensitive-data patterns were detected.",
            detected_types=finding_types,
            masked_types=masked_types,
        )
    )

    payload = ProviderPayload(
        request_id=ticket.ticket_id,
        subject=subject_result.protected_text,
        ticket_text=description_result.protected_text,
        allowed_categories=policy.allowed_categories,
    )
    trace_steps.append(
        _trace(
            6,
            "Construct provider JSON",
            TraceStatus.PASS,
            "Python created a strict payload containing only approved provider fields.",
            payload_fields=list(type(payload).model_fields.keys()),
        )
    )

    serialized_payload = payload.model_dump_json()
    final_inspection = inspect_text(serialized_payload, policy)
    final_blocked_types = sorted(
        {
            finding.data_type
            for finding in final_inspection.findings
            if finding.action == FindingAction.BLOCK
        }
    )
    if final_blocked_types or final_inspection.prompt_manipulation_detected:
        trace_steps.append(
            _trace(
                7,
                "Run final outbound gate",
                TraceStatus.BLOCKED,
                "The exact serialized JSON failed its final inspection and cannot reach the provider adapter.",
                blocked_types=final_blocked_types,
                prompt_manipulation_detected=final_inspection.prompt_manipulation_detected,
            )
        )
        return _stopped_result(
            Decision.BLOCK,
            ReasonCode.BLOCK_FINAL_PAYLOAD_GATE,
            trace_steps,
        )

    trace_steps.append(
        _trace(
            7,
            "Run final outbound gate",
            TraceStatus.PASS,
            "The exact serialized JSON passed reinspection and is eligible for the provider adapter.",
            serialized_size_bytes=len(serialized_payload.encode("utf-8")),
        )
    )
    return GatewayResult(
        decision=Decision.MASK if masked_types else Decision.ALLOW,
        reason_codes=[
            ReasonCode.ALLOW_MASKED if masked_types else ReasonCode.ALLOW_CLEAN
        ],
        provider_invoked=False,
        provider_payload=payload,
        trace_steps=trace_steps,
    )


def _manual_after_provider(
    preflight: GatewayResult,
    reason: ReasonCode,
    trace_steps: list[TraceStep],
) -> GatewayResult:
    return GatewayResult(
        decision=Decision.MANUAL_FALLBACK,
        reason_codes=[reason],
        provider_invoked=True,
        provider_payload=preflight.provider_payload,
        provider_response=None,
        playbook=None,
        trace_steps=trace_steps,
    )


def run_signal_gateway(
    ticket: Ticket,
    policy: SecurityPolicy,
    playbooks: dict[str, Playbook],
    provider: MockProviderAdapter,
) -> GatewayResult:
    """Run the complete local gateway through response validation and playbook lookup."""

    preflight = prepare_provider_request(ticket, policy)
    if preflight.provider_payload is None:
        return preflight

    trace_steps = list(preflight.trace_steps)
    try:
        raw_response = provider.invoke(preflight.provider_payload)
    except ProviderTimeoutError:
        trace_steps.append(
            _trace(
                8,
                "Call simulated AI provider",
                TraceStatus.FAILED,
                "The local mock simulated a timeout; Signal moved to manual handling.",
                destination="tp-ai-01.invalid",
            )
        )
        return _manual_after_provider(
            preflight,
            ReasonCode.MANUAL_PROVIDER_TIMEOUT,
            trace_steps,
        )
    except ProviderUnavailableError:
        trace_steps.append(
            _trace(
                8,
                "Call simulated AI provider",
                TraceStatus.FAILED,
                "The local mock simulated a provider failure; Signal moved to manual handling.",
                destination="tp-ai-01.invalid",
            )
        )
        return _manual_after_provider(
            preflight,
            ReasonCode.MANUAL_PROVIDER_FAILURE,
            trace_steps,
        )

    trace_steps.append(
        _trace(
            8,
            "Call simulated AI provider",
            TraceStatus.PASS,
            "HTTPX sent the approved JSON to a local MockTransport; no external network call occurred.",
            destination="tp-ai-01.invalid",
            transport="HTTPX MockTransport",
        )
    )

    try:
        response = validate_provider_response(raw_response, policy)
    except ResponseValidationError:
        trace_steps.append(
            _trace(
                9,
                "Validate provider response",
                TraceStatus.BLOCKED,
                "The untrusted response failed LindenArc validation and will not be displayed.",
            )
        )
        return _manual_after_provider(
            preflight,
            ReasonCode.MANUAL_INVALID_PROVIDER_RESPONSE,
            trace_steps,
        )

    trace_steps.append(
        _trace(
            9,
            "Validate provider response",
            TraceStatus.PASS,
            "The response passed schema, category, size, markup, and sensitive-content checks.",
            category=response.category,
        )
    )

    playbook = playbooks.get(response.category)
    if response.category == "unknown" or playbook is None:
        trace_steps.append(
            _trace(
                10,
                "Retrieve approved LindenArc playbook",
                TraceStatus.FAILED,
                "No approved playbook applies, so the support agent must handle the case manually.",
                category=response.category,
            )
        )
        return GatewayResult(
            decision=Decision.MANUAL_FALLBACK,
            reason_codes=[ReasonCode.MANUAL_UNKNOWN_CATEGORY],
            provider_invoked=True,
            provider_payload=preflight.provider_payload,
            provider_response=response,
            playbook=None,
            trace_steps=trace_steps,
        )

    trace_steps.append(
        _trace(
            10,
            "Retrieve approved LindenArc playbook",
            TraceStatus.PASS,
            "LindenArc—not the model—supplied the versioned troubleshooting guidance.",
            playbook_id=playbook.playbook_id,
            playbook_version=playbook.version,
        )
    )
    return GatewayResult(
        decision=preflight.decision,
        reason_codes=preflight.reason_codes,
        provider_invoked=True,
        provider_payload=preflight.provider_payload,
        provider_response=response,
        playbook=playbook,
        trace_steps=trace_steps,
    )
