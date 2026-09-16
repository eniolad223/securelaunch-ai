"""Load and validate versioned policy and playbook configuration."""

import json
from pathlib import Path

from pydantic import ValidationError

from .models import Playbook, SecurityPolicy


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY_PATH = PROJECT_ROOT / "config" / "security_policy.json"
DEFAULT_PLAYBOOK_PATH = PROJECT_ROOT / "config" / "playbooks.json"


class ConfigurationError(RuntimeError):
    """Raised when a required security configuration cannot be trusted."""


def _read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigurationError(f"Required configuration could not be loaded: {path.name}") from exc


def load_security_policy(path: Path = DEFAULT_POLICY_PATH) -> SecurityPolicy:
    """Return a validated policy or fail closed with a safe error."""

    try:
        return SecurityPolicy.model_validate(_read_json(path))
    except ValidationError as exc:
        raise ConfigurationError("Security policy failed validation") from exc


def load_playbooks(path: Path = DEFAULT_PLAYBOOK_PATH) -> dict[str, Playbook]:
    """Return approved playbooks indexed by their allowed category."""

    raw = _read_json(path)
    if not isinstance(raw, list):
        raise ConfigurationError("Playbook configuration must be a list")

    try:
        playbooks = [Playbook.model_validate(item) for item in raw]
    except ValidationError as exc:
        raise ConfigurationError("Playbook configuration failed validation") from exc

    indexed = {playbook.category: playbook for playbook in playbooks}
    if len(indexed) != len(playbooks):
        raise ConfigurationError("Every approved playbook category must be unique")
    return indexed


def select_approved_playbook(
    category: str,
    policy: SecurityPolicy,
    playbooks: dict[str, Playbook],
) -> Playbook | None:
    """Return LindenArc guidance only for a policy-approved category."""

    if category == "unknown" or category not in policy.allowed_categories:
        return None
    return playbooks.get(category)
