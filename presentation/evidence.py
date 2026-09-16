"""Presentation-only explanations derived from the executed result and source files."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def aws_test_text(case_id: str) -> str:
    report = (ROOT / "evidence/aws/AWS_GUARDRAIL_VALIDATION_REPORT.md").read_text(encoding="utf-8")
    match = re.search(rf"### {re.escape(case_id)}:.*?```text\n(.*?)\n```", report, re.S)
    if not match:
        raise ValueError(f"No documented AWS input for {case_id}")
    return match.group(1)


TYPE_NAMES = {
    "email_address": "email address", "phone_number": "phone number",
    "account_reference": "customer account reference", "credit_card_number": "payment-card number",
    "credit_debit_card_number": "payment-card number", "ssn": "Social Security number",
    "us_social_security_number": "Social Security number", "aws_access_key": "AWS access key",
    "aws_secret_key": "AWS secret key", "password": "password",
}


def process_steps(result):
    """Four short, factual explanations; never imply a real external API was called."""
    steps = {s.step_number: s for s in result.trace_steps}
    inspection = steps.get(5)
    detected = inspection.safe_details.get("detected_types", []) if inspection else []
    readable = ", ".join(TYPE_NAMES.get(str(x).lower(), str(x).replace("_", " ").lower()) for x in detected)
    reason = result.reason_codes[0].value
    if reason == "MANUAL_KILL_SWITCH":
        first = ("Emergency switch checked", "AI processing was disabled before ticket inspection.", "stopped")
    elif reason == "BLOCK_INPUT_SIZE_LIMIT":
        first = ("Ticket size checked", "The text exceeded the configured size limit.", "stopped")
    elif reason == "BLOCK_PROMPT_MANIPULATION":
        first = ("Ticket inspected", "An instruction-override phrase was detected.", "stopped")
    elif reason == "BLOCK_RESTRICTED_DATA":
        first = ("Ticket inspected", f"Detected: {readable or 'restricted information'}.", "stopped")
    elif inspection and inspection.safe_details.get("masked_types"):
        first = ("Ticket inspected", f"Removed from the text: {readable}.", "done")
    else:
        first = ("Ticket inspected", "No configured sensitive-data pattern was detected.", "done")
    gate = steps.get(7)
    second = ("Outgoing request checked", "The exact JSON passed a second security inspection.", "done") if gate and gate.status.value == "pass" else (
        "Outgoing request stopped", "Final inspection rejected the completed JSON.", "stopped") if gate else (
        "No outgoing request", "Processing stopped before an API request could be built.", "idle")
    third = ("External API simulated", "Only the approved request reached the local mock, not a live AI service.", "done") if result.provider_invoked else (
        "External API not called", "The ticket remained within the simulated organization boundary.", "stopped")
    if result.playbook:
        last = ("Agent review next", "The response passed checks. A support agent reviews it with approved guidance.", "done")
    elif not result.provider_invoked:
        last = ("Manual support instead", "No AI response exists. A support agent handles the original ticket.", "idle")
    elif reason == "MANUAL_INVALID_PROVIDER_RESPONSE":
        last = ("Unsafe response withheld", "The response failed validation. The case needs manual support.", "stopped")
    elif reason == "MANUAL_UNKNOWN_CATEGORY":
        last = ("Manual support instead", "No approved troubleshooting guide matched the response category.", "stopped")
    else:
        last = ("Manual support instead", "The simulated AI service failed or timed out. No usable summary was returned.", "stopped")
    return [first, second, third, last]


def source_excerpt(relative_path: str, start: str, end: str | None = None, limit: int = 36):
    """Read the real project source; never manufacture illustrative code as evidence."""
    lines = (ROOT / relative_path).read_text(encoding="utf-8").splitlines()
    begin = next(i for i, line in enumerate(lines) if start in line)
    finish = next((i for i in range(begin + 1, len(lines)) if end and end in lines[i]), min(begin + limit, len(lines)))
    return relative_path, begin + 1, "\n".join(lines[begin:finish]).rstrip()


def decision_source(result):
    reason = result.reason_codes[0].value
    path = "src/securelaunch/gateway.py"
    choices = {
        "MANUAL_KILL_SWITCH": ("    if policy.kill_switch_enabled:", "    trace_steps.append("),
        "BLOCK_RESTRICTED_DATA": ("    if blocked_types:", "    masked_types ="),
        "BLOCK_PROMPT_MANIPULATION": ("    if subject_result.prompt_manipulation_detected", "    blocked_types ="),
        "BLOCK_INPUT_SIZE_LIMIT": ("    if combined_length >", None),
        "BLOCK_FINAL_PAYLOAD_GATE": ("    if final_blocked_types or", None),
        "MANUAL_PROVIDER_TIMEOUT": ("    try:", "    except ProviderUnavailableError:"),
        "MANUAL_PROVIDER_FAILURE": ("    except ProviderUnavailableError:", None),
        "MANUAL_INVALID_PROVIDER_RESPONSE": ("        response = validate_provider_response", None),
        "MANUAL_UNKNOWN_CATEGORY": ("    if response.category ==", None),
    }
    start, end = choices.get(reason, ("    payload = ProviderPayload(", "    final_blocked_types ="))
    if reason == "MANUAL_KILL_SWITCH":
        # The inner append is part of the branch, not its end.
        return source_excerpt(path, start, "    excluded_fields =", limit=25)
    return source_excerpt(path, start, end)
