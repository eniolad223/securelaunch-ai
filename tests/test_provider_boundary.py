import json

import pytest

from securelaunch.configuration import load_playbooks, load_security_policy
from securelaunch.gateway import run_signal_gateway
from securelaunch.models import Decision, ReasonCode, Ticket
from securelaunch.provider import MockProviderAdapter, ResponseMode


def make_ticket(description="The receipt upload stops before completion."):
    return Ticket(
        scenario_id="SCN-PROVIDER-TEST",
        ticket_id="TKT-SYNTH-002",
        tenant_id="TENANT-SYNTH-A",
        subject="Receipt upload problem",
        description=description,
        customer_email="customer@example.test",
        account_reference="ACCT-SYNTH-1001",
        attachment_names=["synthetic-receipt.pdf"],
    )


def run_with_mode(mode, ticket=None):
    adapter = MockProviderAdapter(mode)
    result = run_signal_gateway(
        ticket or make_ticket(),
        load_security_policy(),
        load_playbooks(),
        adapter,
    )
    return result, adapter


def test_approved_payload_reaches_only_reserved_mock_endpoint():
    result, adapter = run_with_mode(ResponseMode.VALID)

    assert result.decision == Decision.ALLOW
    assert result.provider_invoked is True
    assert adapter.call_count == 1
    assert adapter.last_request_url == "https://tp-ai-01.invalid/v1/signal"
    captured = json.loads(adapter.last_request_body)
    assert set(captured) == {"request_id", "subject", "ticket_text", "allowed_categories"}
    assert "customer@example.test" not in adapter.last_request_body.decode()
    assert result.playbook is not None
    assert result.playbook.playbook_id == "PB-REC-001"


def test_blocked_ticket_never_invokes_mock_provider():
    blocked = make_ticket("My SSN is 000-12-3456 and the upload failed.")

    result, adapter = run_with_mode(ResponseMode.VALID, blocked)

    assert result.decision == Decision.BLOCK
    assert result.provider_invoked is False
    assert adapter.call_count == 0
    assert adapter.last_request_body is None


@pytest.mark.parametrize(
    "mode",
    [
        ResponseMode.INVALID_SCHEMA,
        ResponseMode.UNAUTHORIZED_CATEGORY,
        ResponseMode.SENSITIVE_OUTPUT,
        ResponseMode.MARKUP_OUTPUT,
    ],
)
def test_unsafe_provider_output_is_rejected(mode):
    result, adapter = run_with_mode(mode)

    assert adapter.call_count == 1
    assert result.decision == Decision.MANUAL_FALLBACK
    assert result.reason_codes == [ReasonCode.MANUAL_INVALID_PROVIDER_RESPONSE]
    assert result.provider_response is None
    assert "000-12-3456" not in result.model_dump_json()


def test_unknown_category_uses_manual_fallback_without_playbook():
    result, adapter = run_with_mode(ResponseMode.UNKNOWN_CATEGORY)

    assert adapter.call_count == 1
    assert result.decision == Decision.MANUAL_FALLBACK
    assert result.reason_codes == [ReasonCode.MANUAL_UNKNOWN_CATEGORY]
    assert result.playbook is None


@pytest.mark.parametrize(
    ("mode", "expected_reason"),
    [
        (ResponseMode.TIMEOUT, ReasonCode.MANUAL_PROVIDER_TIMEOUT),
        (ResponseMode.SERVICE_ERROR, ReasonCode.MANUAL_PROVIDER_FAILURE),
    ],
)
def test_provider_failure_uses_safe_manual_fallback(mode, expected_reason):
    result, adapter = run_with_mode(mode)

    assert adapter.call_count == 1
    assert result.decision == Decision.MANUAL_FALLBACK
    assert result.reason_codes == [expected_reason]
    assert result.provider_response is None
