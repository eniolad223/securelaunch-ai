"""Guided showcase for the existing Python gateway and independent AWS lab."""
from __future__ import annotations
import base64
import html
import io
import json
import re
import sys
import textwrap
import zipfile
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
from securelaunch.configuration import load_security_policy
from securelaunch.evidence import create_evidence_receipt
from securelaunch.models import Decision, GatewayResult, TraceStatus
from securelaunch.scenarios import execute_scenario, load_scenarios
from presentation.content import APPROACH, AWS_CASES, DECISIONS, FRAMEWORKS
from presentation.evidence import aws_test_text, process_steps, decision_source, source_excerpt

st.set_page_config(page_title="AI Security Case Study | Eniola Durojaiye", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")
st.html(f"<style>{(ROOT / 'presentation/theme.css').read_text(encoding='utf-8')}</style>")
SCENARIOS = {item.scenario_id: item for item in load_scenarios()}
PAGES = [("overview", "Overview", "grid_view"), ("lab", "Try the gateway", "tune"), ("aws", "AWS validation", "cloud_done"), ("governance", "Risk & governance", "policy"), ("approach", "My approach", "route")]
for key, value in {"rv_page": "overview", "rv_preview": "SCN-02", "rv_scenario": "SCN-02", "rv_aws": 2, "rv_risk": 0, "rv_governance": "Decisions", "rv_framework": "NIST CSF 2.0", "rv_approach": 0}.items():
    st.session_state.setdefault(key, value)

ICONS = {
    "shield": '<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6z"/><path d="m8 12 3 3 5-6"/>',
    "arrow": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    "lock": '<rect x="5" y="10" width="14" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3m-4 4v3"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    "stop": '<path d="m8 3-5 5v8l5 5h8l5-5V8l-5-5z"/><path d="M8 12h8"/>',
    "person": '<circle cx="12" cy="7" r="4"/><path d="M5 21v-3a7 7 0 0 1 14 0v3"/>',
}

def icon(name: str, size: int = 24) -> str:
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#7152d6" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'
    encoded = base64.b64encode(svg.encode()).decode()
    return f'<img class="line-icon" src="data:image/svg+xml;base64,{encoded}" width="{size}" height="{size}" alt="" aria-hidden="true">'

def safe(value: object) -> str:
    return html.escape(str(value))

def block(markup: str) -> None:
    st.html(textwrap.dedent(markup))

def protected(text: str) -> str:
    return re.sub(r"(\[MASKED_[A-Z_]+\]|\{(?:EMAIL|PHONE|LindenArcAccountReference)\})", r'<mark class="changed">\1</mark>', safe(text)).replace("\n", "<br>")

def go(page: str) -> None:
    st.session_state.rv_page = page

def choose(key: str, value: object) -> None:
    st.session_state[key] = value

def select_scenario(scenario_id: str) -> None:
    st.session_state.rv_scenario = scenario_id
    st.session_state.rv_all_scenarios = scenario_id
    st.session_state.pop("rv_result", None)
    st.session_state.pop("rv_receipt", None)

def run_selected() -> None:
    scenario = SCENARIOS[st.session_state.rv_scenario]
    result = execute_scenario(scenario)
    st.session_state.rv_result = result
    policy = load_security_policy().model_copy(update={"kill_switch_enabled": scenario.test_setup.kill_switch_enabled})
    st.session_state.rv_receipt = create_evidence_receipt(scenario, policy, result)

def open_preview() -> None:
    select_scenario(st.session_state.rv_preview)
    st.session_state.rv_page = "lab"

def section(number: str, label: str, title: str, description: str) -> None:
    block(f'<div class="section-title"><div><div class="eyebrow"><span class="dot"></span>{label}</div><h1>{title}</h1><p>{description}</p></div><span class="section-number">{number}</span></div>')

def next_step(page: str, label: str) -> None:
    with st.container(key="next_step"):
        st.button(label, icon=":material/arrow_forward:", on_click=go, args=(page,), key=f"next_{page}")

def journey(labels: list[str], active: int = -1) -> None:
    items = ''.join(f'<div class="journey-step {"current" if i == active else ""}"><span>{i + 1:02}</span>{safe(label)}</div>' for i, label in enumerate(labels))
    block(f'<div class="journey" aria-label="Process at a glance">{items}</div>')

def download_source(relative_path: str, label: str, key: str) -> None:
    path = ROOT / relative_path
    if path.is_file():
        mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document" if path.suffix.lower() == ".docx" else "text/plain"
        st.download_button(label, path.read_bytes(), file_name=path.name, mime=mime, icon=":material/download:", key=key)

def header() -> None:
    block(f'<div class="masthead"><div class="identity"><div class="brand-mark">{icon("shield",24)}</div><div><strong>AI Security Case Study</strong><small>SecureLaunch AI · Fictional fintech scenario</small></div></div><div class="byline">Built & investigated by<br><b>Eniola Durojaiye</b></div></div>')
    with st.container(key="review_nav", horizontal=True, gap="xxsmall"):
        for page, label, glyph in PAGES:
            st.button(label, key=f"nav_{page}", icon=f":material/{glyph}:", type="primary" if st.session_state.rv_page == page else "secondary", on_click=go, args=(page,))

def render_preview() -> None:
    result = execute_scenario(SCENARIOS[st.session_state.rv_preview])
    blocked = result.decision == Decision.BLOCK
    if result.decision == Decision.MASK:
        before = 'My expense receipt will not upload. Please send updates to <mark>mia.brooks@example.test</mark>.'
        after = 'My expense receipt will not upload. Please send updates to <span class="mask">[MASKED_EMAIL_ADDRESS]</span>.'
        decision, description = "Email removed before sending", "The AI can summarize the upload problem without needing the customer's email. The placeholder replaces the address."
        color = "amber"
    elif blocked:
        before = 'Invoice appears twice. The ticket also contains a <mark>payment-card number</mark>.'
        after = '<span class="stop-note">No API request to the external AI provider.</span>'
        decision, description = "Payment data detected: blocked", "The original ticket stays within the organization for a support agent to handle manually."
        color = "rose"
    else:
        before = "My receipt upload freezes at 80 percent. Can you help?"
        after = "My receipt upload freezes at 80 percent. Can you help?"
        decision, description = "Ticket text approved", "No configured sensitive-data pattern was found. Only approved fields can continue; attachments and unnecessary metadata are excluded."
        color = "green"
    block(f'''<div class="stage" role="img" aria-label="Illustrated result from the Python gateway: {decision}. {description}">
      <div class="stage-head"><span>A customer asks for help</span><span><i class="live-dot"></i>Example</span></div>
      <div class="ticket-chip"><small>1 · ORIGINAL SUPPORT REQUEST · EXCERPT</small><p>{before}</p></div>
      <div class="connector"></div><div class="gate-node {color}">{icon('stop' if blocked else 'shield')}<b>2 · {decision}</b></div>
      <div class="connector {'halted' if blocked else ''}"></div><div class="ticket-chip output {color}"><small>3 · {'NOT SENT TO EXTERNAL AI' if blocked else 'CONTENT PERMITTED FOR EXTERNAL AI'}</small><p>{after}</p></div>
      <div class="stage-foot">{description}</div><div class="stage-scope">Illustrated excerpt · Real Python decision · No live AI call</div></div>''')
    block('<p class="preview-title">Try a different decision ↓</p>')
    with st.container(key="preview_choices", horizontal=True, gap="small"):
        for sid, label in [("SCN-02", "Mask an email"), ("SCN-04", "Block card data"), ("SCN-01", "Allow clean text")]:
            st.button(label, key=f"preview_{sid}", type="primary" if st.session_state.rv_preview == sid else "secondary", on_click=choose, args=("rv_preview", sid))

def overview() -> None:
    with st.container(key="overview_columns"):
        left, right = st.columns([1.13, 1], gap="large", vertical_alignment="center")
        with left:
            block('''<div class="hero-copy"><div class="eyebrow"><span class="dot"></span>Security engineering + risk & governance</div>
            <h1>Protecting data.<br>Before it reaches<br><span>external AI.</span></h1>
            <p class="lead">This project turns an AI data-exposure risk into a working security gateway: remove unnecessary information, mask approved identifiers, and block restricted content <b>before an external API request is sent.</b></p>
            <p class="scenario"><b>The scenario:</b> LindenArc is a fictional B2B fintech company providing invoice and expense software. Its proposed support product, <b>Signal</b>, would use an <b>external AI provider</b> to summarize tickets and help agents find approved troubleshooting steps.</p>
            <div class="owner-note"><strong>My role: security analyst.</strong> I analyzed the risks, built and tested the Python controls, and independently validated data protection with Amazon Bedrock Guardrails.</div></div>''')
            st.button("Explore the working gateway", icon=":material/arrow_forward:", type="primary", on_click=open_preview, key="hero_cta")
            block('<p class="mini-note">Next: choose a sample ticket and see the protection work.</p>')
        with right:
            render_preview()
    block('<div class="evidence-strip"><div class="evidence-stat"><b>43</b><span><strong>Automated Python checks</strong><br>Control behavior and safe failure</span></div><div class="evidence-stat"><b>9/9</b><span><strong>Selected AWS cases matched</strong><br>Real Guardrail · synthetic test data</span></div><div class="evidence-stat"><b>10</b><span><strong>Risks tied to release gates</strong><br>Business decisions backed by evidence</span></div></div>')
    block('<div class="purpose-callout"><span class="eyebrow">The purpose behind the controls</span><h2>Gain value from AI. Reduce data exposure. Keep people accountable.</h2><p>My starting question: what new exposure does AI create, and how can I design and test protections against it?</p></div>')

REASONS = {
    "ALLOW_CLEAN": "The permitted ticket text passed the configured checks. Unnecessary metadata was excluded.",
    "ALLOW_MASKED": "Approved identifiers were removed from the ticket text before the completed request passed a second inspection.",
    "BLOCK_RESTRICTED_DATA": "Restricted data was detected. The gateway created no API request to the external AI provider.",
    "BLOCK_PROMPT_MANIPULATION": "An instruction-override phrase was detected. The gateway created no API request to the external AI provider.",
    "BLOCK_INPUT_SIZE_LIMIT": "The ticket exceeded the configured size limit. Processing stopped before the provider boundary.",
    "BLOCK_FINAL_PAYLOAD_GATE": "The completed request failed its final inspection. The provider was not called.",
    "MANUAL_KILL_SWITCH": "The emergency switch disabled AI processing. The ticket stays in the manual support workflow.",
    "MANUAL_PROVIDER_TIMEOUT": "The local provider simulation timed out. The result requires manual support handling.",
    "MANUAL_PROVIDER_FAILURE": "The local provider simulation returned an error. The result requires manual support handling.",
    "MANUAL_INVALID_PROVIDER_RESPONSE": "The simulated provider response failed validation and was withheld from the support view.",
    "MANUAL_UNKNOWN_CATEGORY": "The response had no approved troubleshooting category. A person must handle the case.",
}

def result_summary(result: GatewayResult) -> None:
    title, color, glyph = {
        Decision.ALLOW: ("Allowed: approved text can continue to external AI.", "green", "check"),
        Decision.MASK: ("Masked: identifiers removed, support context retained.", "amber", "shield"),
        Decision.BLOCK: ("Blocked: no API request to external AI.", "rose", "stop"),
        Decision.MANUAL_FALLBACK: ("Manual handling. The workflow stopped safely.", "amber", "person"),
    }[result.decision]
    expected = SCENARIOS[st.session_state.rv_scenario].expected_result
    matched = result.decision == expected.decision and result.provider_invoked == expected.provider_invoked
    block(f'<div class="outcome {color}">{icon(glyph,29)}<div><h3>{title}</h3><p>{REASONS[result.reason_codes[0].value]}</p></div><div class="result-meta"><b>{"Expected result matched" if matched else "Unexpected result"}</b>{"API simulated locally" if result.provider_invoked else "No API request created"}</div></div>')

def control_flow(result: GatewayResult) -> None:
    items = [f'<div class="flow-item {status}"><i>{i:02}</i><b>{safe(label)}</b><span>{safe(description)}</span></div>' for i, (label, description, status) in enumerate(process_steps(result), 1)]
    block('<div class="flow">' + ''.join(items) + '</div>')

def technical_evidence(result: GatewayResult) -> None:
    st.write("These excerpts are read directly from the Python files used by this demo. They are not pseudocode.")
    path, line, code = decision_source(result)
    st.markdown("**1. The code behind this decision**")
    st.caption(f"{path} · starting at line {line}")
    st.code(code, language="python")
    if result.decision == Decision.MASK:
        st.markdown("**2. How identifiers are replaced**")
        path, line, code = source_excerpt("src/securelaunch/inspection.py", "def _mask_findings", "def inspect_text")
    else:
        st.markdown("**2. The boundary before the external API call**")
        path, line, code = source_excerpt("src/securelaunch/gateway.py", "    preflight = prepare_provider_request", "    except ProviderTimeoutError:")
    st.caption(f"{path} · starting at line {line}")
    st.code(code, language="python")
    st.markdown("**3. Actual result from this run**")
    st.json({"decision": result.decision.value, "reason": result.reason_codes[0].value, "external_api_simulated": result.provider_invoked, "live_external_calls": 0, "approved_request": result.provider_payload.model_dump() if result.provider_payload else None}, expanded=True)
    with st.expander("Show the complete execution trace"):
        for step in result.trace_steps:
            st.markdown(f"**{step.step_number}. {step.name}** · `{step.status.value}`  \n{step.explanation}")
    receipt = st.session_state.rv_receipt
    st.download_button("Download sanitized evidence receipt", receipt.model_dump_json(indent=2), file_name=f"{receipt.scenario_id.lower()}-evidence.json", mime="application/json", icon=":material/download:", key="download_receipt")

def lab() -> None:
    section("02", "Working Python demonstration", "What would leave the company?", "A support ticket is a customer's request for help. Choose an example below, then run the gateway to see what is removed, allowed, or blocked before an external AI request.")
    result = st.session_state.get("rv_result")
    journey(["Choose a ticket", "Run the security check", "See what can leave"], 2 if result else 1)
    with st.container(key="scenario_picks", horizontal=True, gap="small"):
        for sid, label in [("SCN-02", "Email exposure"), ("SCN-04", "Payment data"), ("SCN-07", "Prompt attack"), ("SCN-12", "Provider timeout"), ("SCN-01", "Clean ticket")]:
            st.button(label, key=f"pick_{sid}", type="primary" if st.session_state.rv_scenario == sid else "secondary", on_click=select_scenario, args=(sid,))
    with st.expander("Explore all 15 scenarios"):
        st.session_state.setdefault("rv_all_scenarios", st.session_state.rv_scenario)
        pick = st.selectbox("Synthetic scenario", list(SCENARIOS), index=None, format_func=lambda sid: f"{sid} · {SCENARIOS[sid].title}", key="rv_all_scenarios")
        st.button("Use this scenario", on_click=select_scenario, args=(pick,), key="use_scenario")
    scenario = SCENARIOS[st.session_state.rv_scenario]
    with st.container(key="lab_columns"):
        left, right = st.columns(2, gap="medium")
        with left:
            block(f'<div class="panel"><div class="panel-label">Customer request inside the company <span class="tag">Synthetic example</span></div><h3>{safe(scenario.ticket.subject)}</h3><p>{safe(scenario.ticket.description)}</p></div>')
        with right:
            if result is None:
                block(f'<div class="panel waiting"><div class="waiting-icon">{icon("lock",32)}</div><h3>What could the external AI receive?</h3><p>Click the purple <b>Run the security gateway</b> button below to reveal the answer.</p><div class="connector"></div></div>')
            elif result.provider_payload is not None:
                changed = any(s.safe_details.get("masked_types") for s in result.trace_steps)
                tint = "amber" if changed else "green"
                block(f'<div class="panel outbound {tint}"><div class="panel-label">Text permitted for external AI <span class="tag {tint}">{"Identifiers removed" if changed else "Text approved"}</span></div><h3>{protected(result.provider_payload.subject)}</h3><p>{protected(result.provider_payload.ticket_text)}</p><div class="panel-explanation">{"Highlighted placeholders replace identifiers. The support problem stays readable." if changed else "No configured sensitive-data pattern was detected in this text."} The API call is simulated locally.</div></div>')
            else:
                tint = "rose" if result.decision == Decision.BLOCK else "amber"
                block(f'<div class="panel outbound {tint}"><div class="panel-label">No API request to external AI <span class="tag {tint}">{"Blocked" if tint == "rose" else "AI disabled"}</span></div><h3>The ticket stayed within the organization.</h3><p>A support agent can handle the original request manually. No ticket content reached the simulated external AI service.</p><div class="boundary-stop">{icon("stop")} External AI route stopped</div></div>')
    with st.container(key="run_ready" if result is None else "run_complete"):
        a, b = st.columns([1, 2], vertical_alignment="center")
        with a:
            st.button("Run the security gateway" if result is None else "Run again", type="primary", icon=":material/play_arrow:", on_click=run_selected, key="run_gateway", width="stretch")
        with b:
            block(f'<p class="mini-note"><b>{"Your next step: run this example." if result is None else "Try another ticket to compare decisions."}</b><br>Real Python controls, simulated external AI. No live AI or AWS calls.</p>')
    if result is not None:
        result_summary(result)
        control_flow(result)
        with st.expander("Technical evidence · actual Python code and this run's result"):
            technical_evidence(result)
        with st.expander("What happens next · validated output and human review"):
            if result.provider_response:
                st.markdown("**Validated summary from the local simulation**")
                st.write(result.provider_response.summary)
            if result.playbook:
                st.markdown(f"**Human-authored playbook: {result.playbook.title}**")
                for number, step in enumerate(result.playbook.approved_steps, 1):
                    st.write(f"{number}. {step}")
                st.caption("A support agent reviews the original ticket, the summary, and the approved steps. The AI cannot execute actions.")
            else:
                st.write("A support agent handles this case through the normal manual process. No troubleshooting action is executed by the AI.")
    next_step("aws", "Next: compare with the independent AWS validation")

@st.cache_data(show_spinner=False)
def aws_evidence_zip() -> bytes:
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED) as package:
        base = ROOT / "evidence/aws"
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in {".md", ".json", ".png"}:
                package.writestr(path.relative_to(base).as_posix(), path.read_bytes())
    return data.getvalue()

def aws() -> None:
    section("03", "Independent cloud validation", "From Python controls to AWS evidence.", "I separately configured Amazon Bedrock Guardrails and tested sensitive-data and prompt-attack filters with synthetic tickets. Select a case to inspect the recorded result.")
    block('<div class="cloud-proof"><span class="proof-orbit">'+icon("shield",32)+'</span><div><h3>Not just a prototype: independently tested in AWS.</h3><p>The Python demo tests application controls. This separate lab shows how a real cloud security service handled the same data-exposure risks.</p></div></div>')
    block('<div class="aws-banner"><div><span class="big">9/9</span><p>Selected tests produced<br>the expected result</p></div><div class="aws-mini"><div><b>12 + 1 rules</b><span>12 sensitive-data types configured,<br>plus 1 custom account pattern</span></div><div><b>Version 1 saved</b><span>Fixed configuration checked<br>in the console and through the API</span></div><div><b>No AI model called</b><span>Text checked by Guardrails only.<br>No real customer records used.</span></div></div></div>')
    journey(["Choose a recorded test", "Read its input and outcome", "Inspect the AWS capture"], 0)
    left, right = st.columns([.88, 1.35], gap="large")
    with left:
        selected = st.selectbox("Choose an AWS test result", range(len(AWS_CASES)), index=st.session_state.rv_aws, format_func=lambda i: f"{AWS_CASES[i]['id']} · {AWS_CASES[i]['name']}", key="rv_aws_picker")
        st.session_state.rv_aws = selected
        case = AWS_CASES[selected]
        color = "green" if case["decision"] == "Allow" else "rose" if case["decision"] == "Block" else "amber"
        text = safe(aws_test_text(case["id"])).replace("\n", "<br>")
        label = "Example AI response supplied to AWS" if case["source"] == "Output" else "Support ticket supplied to AWS"
        block(f'<div class="detail-card aws-case"><div class="panel-label">{label}</div><div class="aws-input">{text}</div><div class="connector"></div><div class="aws-result {color}"><strong>{case["decision"]} · Recorded AWS outcome</strong><p>{case["observed"]}</p></div><div class="takeaway">{case["why"]}</div></div>')
        if case["id"] in {"AWS-T04", "AWS-T05", "AWS-T06"}:
            st.caption("This public transcript replaces synthetic financial values or example credentials with labels. The original test values are visible in the capture.")
        block('<p class="mini-note">Recorded AWS evidence · September 14–15, 2026.<br>The nine cases used the working draft. Version 1 received a console smoke test and a direct API reproduction.</p>')
    with right:
        block('<div class="panel-label" style="margin:2px 0 10px">Original AWS test capture <span class="tag">Synthetic test data</span></div>')
        filename = case.get("summary", f"{case['file']}-summary.png")
        path = ROOT / "evidence/aws/screenshots/validation" / filename
        st.image(str(path), caption="Open fullscreen to examine the AWS console result.", width="stretch")
    with st.expander("Inspect the full detection trace for this case"):
        trace = ROOT / "evidence/aws/screenshots/validation" / f"{case['file']}-trace.png"
        st.image(str(trace), width="stretch")
        if case["id"] == "AWS-T07":
            st.caption("Prompt-attack detection is shown in the main capture above. This supplementary trace shows that the PII detectors did not trigger.")
    with st.expander("All nine cases · expected versus observed"):
        rows = ''.join(f'<tr><td>{item["id"]}</td><td>{item["name"]}</td><td>{item["decision"]}</td><td>{item["observed"]}</td></tr>' for item in AWS_CASES)
        block(f'<table class="mapping"><thead><tr><th>Case</th><th>Test</th><th>Expected</th><th>Observed · matched</th></tr></thead><tbody>{rows}</tbody></table>')
        st.caption("This bounded sample does not measure a production detection rate. The Python gateway and AWS Guardrail were tested independently.")
    with st.expander("Custom account rule, Version 1, and API reproduction"):
        st.markdown("**Custom regex: `ACCT-(SYNTH-)?[0-9]{4,12}`**")
        st.write("The fictional identifier format starts with ACCT-, optionally includes SYNTH-, then contains 4 to 12 digits. For example, ACCT-SYNTH-8421. I added this rule because a managed service cannot know a company's custom account format. This is a lab pattern; a production rule would need stricter boundary and edge-case testing.")
        st.write("Version 1 preserves the tested configuration as a fixed reference. A direct ApplyGuardrail request then masked both the phone number and custom account reference using that version.")
        evidence = json.loads((ROOT / "evidence/aws/api/guardrail-v1-api-evidence-sanitized.json").read_text(encoding="utf-8"))
        block(f'<div class="panel protected"><div class="panel-label">API evidence · Version {evidence["guardrail_version"]}</div><h3>{evidence["action"]}</h3><p>{protected(evidence["sanitized_output"])}</p></div>')
        st.caption("The configuration is real AWS. The input and output text are synthetic. No external foundation model was invoked, and this app does not call the Guardrail.")
        st.download_button("Download complete AWS evidence pack", aws_evidence_zip(), file_name="aws-guardrail-evidence.zip", mime="application/zip", icon=":material/download:", key="download_aws")
    next_step("governance", "Next: see the risk and governance decisions")

def risk_decisions() -> None:
    left, right = st.columns([.75, 1.9], gap="large")
    with left:
        block('<p class="hint">Choose a lesson to explore the risk and my response.</p>')
        with st.container(key="risk_choices"):
            for i, item in enumerate(DECISIONS):
                st.button(item["name"], key=f"risk_{i}", type="primary" if st.session_state.rv_risk == i else "secondary", on_click=choose, args=("rv_risk", i), width="stretch", icon=":material/arrow_forward:")
    with right:
        item = DECISIONS[st.session_state.rv_risk]
        journey(["Risk I identified", "Action I took", "Limits I learned"], 1)
        block(f'<div class="decision-card"><h2>{item["question"]}</h2><div class="decision-grid"><div><span class="label">Risk I identified</span><p>{item["risk"]}</p></div><div><span class="label">My decision and mitigation</span><p>{item["choice"]}</p></div></div><div class="judgment"><b>Why it matters:</b> {item["value"]}</div><div class="remaining-risk"><b>What remains unresolved</b><p>{item["remaining"]}</p></div></div>')
        with st.expander("Evidence and controls that could address the remaining risk"):
            st.markdown(f'**Evidence from this project:** {item["evidence"]}. {item["status"]}.')
            st.markdown(f'**Further controls to evaluate:** {item["next_control"]}')
        download_source(item["file"], "Download the underlying analysis", "risk_source")

def standards() -> None:
    st.write("These selected mappings connect project choices to established guidance. NIST provides frameworks; GDPR and the FTC Safeguards Rule create legal duties where applicable. This prototype is not a compliance assessment.")
    with st.container(key="frameworks", horizontal=True, gap="small"):
        for name in FRAMEWORKS:
            st.button(name, key=f"framework_{name}", type="primary" if st.session_state.rv_framework == name else "secondary", on_click=choose, args=("rv_framework", name))
    item = FRAMEWORKS[st.session_state.rv_framework]
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in item["rows"])
    journey(["Read the principle", "Connect it to a control", "Check the evidence"], 1)
    block(f'<div class="detail-card"><div class="panel-label">{item["type"]} <span class="tag">Selected project mapping</span></div><h2>{item["title"]}</h2><p>{item["body"]}</p><table class="mapping"><thead><tr><th>Reference</th><th>Security purpose</th><th>What I implemented or documented</th></tr></thead><tbody>{rows}</tbody></table><p class="mini-note">{item["note"]}</p></div>')
    st.link_button(item["label"], item["url"], icon=":material/open_in_new:")

def governance() -> None:
    section("04", "Risk, governance & lessons learned", "What I protected. What still needs protection.", "This work established a functioning security gateway, selected AWS validation results, and documented risks. Here is how I connected the risks to controls, business value, and the limits of those controls.")
    if st.session_state.rv_governance not in {"Risks & mitigations", "Frameworks & law"}:
        st.session_state.rv_governance = "Risks & mitigations"
    with st.container(key="governance_subnav", horizontal=True, gap="small"):
        for name in ["Risks & mitigations", "Frameworks & law"]:
            st.button(name, key=f"governance_{name}", type="primary" if st.session_state.rv_governance == name else "secondary", on_click=choose, args=("rv_governance", name))
    {"Risks & mitigations": risk_decisions, "Frameworks & law": standards}[st.session_state.rv_governance]()
    next_step("approach", "Next: follow my thinking from question to evidence")

def approach() -> None:
    reviewer_reports = [
        "outputs/reviewer_documents/01-project-scope-and-security-boundary.docx",
        "outputs/reviewer_documents/02-data-lifecycle-and-risk-analysis.docx",
        "outputs/reviewer_documents/03-python-security-gateway-technical-report.docx",
        "outputs/reviewer_documents/04-validation-evidence-report.docx",
        "outputs/reviewer_documents/05-risk-treatment-and-project-lessons.docx",
    ]
    section("05", "My contribution & reasoning", "From a security question to tested controls.", "I used this project to apply cybersecurity knowledge to a realistic business problem, connecting technical work with risk decisions and the evidence behind them.")
    block('''<div class="method-intro"><span class="quote-mark">“</span><div><p>As organizations adopt AI, I want to understand the new exposure it creates, design protections, and test whether those protections work.</p><small>THE QUESTION THAT DROVE THIS PROJECT</small></div></div>''')
    block('<p class="hint">Follow the five steps below to see the question, my work, and the evidence at each stage.</p>')
    left, right = st.columns([.65, 2], gap="large")
    with left:
        with st.container(key="approach_choices"):
            for i, item in enumerate(APPROACH):
                st.button(item["label"], type="primary" if st.session_state.rv_approach == i else "secondary", key=f"approach_{i}", on_click=choose, args=("rv_approach", i), width="stretch")
    with right:
        item = APPROACH[st.session_state.rv_approach]
        journey(["The question", "What I did", "Supporting evidence"], 1)
        block(f'<div class="detail-card"><div class="panel-label">Step {st.session_state.rv_approach + 1} of 5 · My process</div><h2>{item["title"]}</h2><div class="label">The question</div><div class="value">{item["question"]}</div><div class="label">What I did</div><p>{item["action"]}</p><div class="takeaway">Evidence: {item["proof"]}</div></div>')
        download_source(reviewer_reports[st.session_state.rv_approach], "Download the reviewer-ready Word report", "approach_source")
    with st.expander("Explore the supporting reports"):
        st.write("Choose a concise, reviewer-ready Word report. The complete Markdown notes, JSON policy, and Python files remain available in the technical repository, but they are intentionally not presented here as Word documents.")
        artifact = st.selectbox(
            "Choose a report",
            [
                "Project scope, architecture, and security boundary",
                "Data lifecycle and PASTA risk analysis",
                "Python gateway and security policy",
                "Local and AWS validation evidence",
                "Risk treatment and project lessons",
            ],
            key="rv_artifact",
        )
        paths = {
            "Project scope, architecture, and security boundary": "outputs/reviewer_documents/01-project-scope-and-security-boundary.docx",
            "Data lifecycle and PASTA risk analysis": "outputs/reviewer_documents/02-data-lifecycle-and-risk-analysis.docx",
            "Python gateway and security policy": "outputs/reviewer_documents/03-python-security-gateway-technical-report.docx",
            "Local and AWS validation evidence": "outputs/reviewer_documents/04-validation-evidence-report.docx",
            "Risk treatment and project lessons": "outputs/reviewer_documents/05-risk-treatment-and-project-lessons.docx",
        }
        download_source(paths[artifact], "Download selected Word report", "approach_artifact")
    with st.expander("About this presentation"):
        st.markdown("**My technical work**")
        st.write("I developed the Python security gateway and automated tests, completed the risk analysis, and independently configured and tested the Amazon Bedrock Guardrail. The security decisions, evidence, and conclusions presented here reflect that work.")
        st.markdown("**How I used AI**")
        st.write("I used AI-assisted development for the visual implementation of this reviewer-facing interface. I defined the content, visual direction, and acceptance criteria so the interface would communicate my technical work clearly.")
        st.markdown("**Why the scenario uses synthetic data**")
        st.write("I created LindenArc as a realistic business scenario so I could apply security analysis and control design without using a real organization's data. The support tickets are realistic synthetic records that I created to test the Python gateway and the AWS Guardrail configuration. The Python demonstration uses a simulated external AI service; the Amazon Bedrock Guardrail configuration and the recorded AWS results are real.")
    next_step("lab", "Return to the working security gateway")

header()
{"overview": overview, "lab": lab, "aws": aws, "governance": governance, "approach": approach}[st.session_state.rv_page]()
block('<div class="footer-line"><span><b>Eniola Durojaiye</b> · Security engineering, risk analysis & cloud validation</span><span>Fictional scenario · Synthetic data · Bounded prototype evidence</span></div>')
