from datetime import datetime, timezone

import pytest

from securelaunch.configuration import load_security_policy
from securelaunch.evidence import create_evidence_receipt
from securelaunch.scenarios import execute_scenario, load_scenarios


SCENARIOS = load_scenarios()


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda scenario: scenario.scenario_id)
def test_fixed_scenario_matches_approved_expected_result(scenario):
    result = execute_scenario(scenario)

    assert result.decision == scenario.expected_result.decision
    assert result.provider_invoked is scenario.expected_result.provider_invoked


def test_blocked_scenario_receipt_contains_no_raw_restricted_value():
    scenario = next(item for item in SCENARIOS if item.scenario_id == "SCN-03")
    policy = load_security_policy()
    result = execute_scenario(scenario)

    receipt = create_evidence_receipt(scenario, policy, result)
    receipt_json = receipt.model_dump_json()

    assert "000-12-3456" not in receipt_json
    assert "verify my identity" not in receipt_json
    assert receipt.provider_invoked is False
    assert receipt.risk_ids == ["R-03"]
    assert receipt.receipt_id.startswith("EVR-SCN-03-")


def test_same_run_material_produces_same_fingerprint():
    scenario = next(item for item in SCENARIOS if item.scenario_id == "SCN-01")
    policy = load_security_policy()
    result = execute_scenario(scenario)

    first = create_evidence_receipt(
        scenario,
        policy,
        result,
        created_at=datetime(2026, 9, 11, 12, 0, tzinfo=timezone.utc),
    )
    second = create_evidence_receipt(
        scenario,
        policy,
        result,
        created_at=datetime(2026, 9, 11, 13, 0, tzinfo=timezone.utc),
    )

    assert first.safe_test_fingerprint_sha256 == second.safe_test_fingerprint_sha256
    assert first.receipt_id == second.receipt_id
    assert first.created_at_utc != second.created_at_utc


def test_policy_version_change_changes_evidence_fingerprint():
    scenario = next(item for item in SCENARIOS if item.scenario_id == "SCN-01")
    policy = load_security_policy()
    result = execute_scenario(scenario)

    original = create_evidence_receipt(scenario, policy, result)
    revised_policy = policy.model_copy(update={"version": "1.0.1"})
    revised = create_evidence_receipt(scenario, revised_policy, result)

    assert original.safe_test_fingerprint_sha256 != revised.safe_test_fingerprint_sha256
    assert original.receipt_id != revised.receipt_id
