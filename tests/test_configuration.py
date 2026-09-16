import json

import pytest

from securelaunch.configuration import (
    ConfigurationError,
    load_playbooks,
    load_security_policy,
    select_approved_playbook,
)


def test_approved_category_selects_lindenarc_playbook():
    policy = load_security_policy()
    playbooks = load_playbooks()

    selected = select_approved_playbook("receipt_upload_error", policy, playbooks)

    assert selected is not None
    assert selected.playbook_id == "PB-REC-001"
    assert selected.owner == "LindenArc Support Operations"


def test_unknown_category_requires_manual_handling():
    policy = load_security_policy()
    playbooks = load_playbooks()

    assert select_approved_playbook("unknown", policy, playbooks) is None
    assert select_approved_playbook("unapproved_category", policy, playbooks) is None


def test_invalid_policy_fails_closed(tmp_path):
    invalid_policy = tmp_path / "invalid_policy.json"
    invalid_policy.write_text(json.dumps({"policy_id": "incomplete"}), encoding="utf-8")

    with pytest.raises(ConfigurationError, match="failed validation"):
        load_security_policy(invalid_policy)


def test_duplicate_playbook_category_fails_closed(tmp_path):
    playbooks = load_playbooks()
    duplicate = [
        playbooks["account_access"].model_dump(mode="json"),
        playbooks["account_access"].model_dump(mode="json"),
    ]
    invalid_playbooks = tmp_path / "duplicate_playbooks.json"
    invalid_playbooks.write_text(json.dumps(duplicate), encoding="utf-8")

    with pytest.raises(ConfigurationError, match="must be unique"):
        load_playbooks(invalid_playbooks)
