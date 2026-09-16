"""Load and execute fixed, reviewed synthetic demonstration scenarios."""

import json
from pathlib import Path

from pydantic import ValidationError

from .configuration import ConfigurationError, PROJECT_ROOT, load_playbooks, load_security_policy
from .gateway import run_signal_gateway
from .models import GatewayResult, Scenario
from .provider import MockProviderAdapter, ResponseMode


DEFAULT_SCENARIO_PATH = PROJECT_ROOT / "data" / "synthetic_scenarios.json"


def load_scenarios(path: Path = DEFAULT_SCENARIO_PATH) -> list[Scenario]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigurationError("Synthetic scenarios could not be loaded") from exc
    if not isinstance(raw, list):
        raise ConfigurationError("Synthetic scenario configuration must be a list")

    try:
        scenarios = [Scenario.model_validate(item) for item in raw]
    except ValidationError as exc:
        raise ConfigurationError("Synthetic scenario validation failed") from exc

    identifiers = [scenario.scenario_id for scenario in scenarios]
    if len(set(identifiers)) != len(identifiers):
        raise ConfigurationError("Every synthetic scenario ID must be unique")
    for scenario in scenarios:
        try:
            ResponseMode(scenario.test_setup.response_mode)
        except ValueError as exc:
            raise ConfigurationError(
                f"Scenario {scenario.scenario_id} has an unsupported response mode"
            ) from exc
    return scenarios


def execute_scenario(scenario: Scenario) -> GatewayResult:
    policy = load_security_policy().model_copy(
        update={"kill_switch_enabled": scenario.test_setup.kill_switch_enabled}
    )
    provider = MockProviderAdapter(ResponseMode(scenario.test_setup.response_mode))
    return run_signal_gateway(
        scenario.ticket,
        policy,
        load_playbooks(),
        provider,
    )
