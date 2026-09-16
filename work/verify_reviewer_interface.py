"""Exercise reviewer navigation and evidence state using Streamlit's test runner.

Run separately from the 43 backend security tests:
    python work/verify_reviewer_interface.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from streamlit.testing.v1 import AppTest
from presentation.evidence import aws_test_text, decision_source, process_steps


def no_errors(app):
    assert not app.exception, [str(item.value) for item in app.exception]


app = AppTest.from_file(str(ROOT / "app_redesign.py"), default_timeout=20).run()
no_errors(app)
for key in ["preview_SCN-04", "preview_SCN-01", "preview_SCN-02"]:
    app.button(key=key).click().run()
    no_errors(app)

app.button(key="hero_cta").click().run()
assert app.session_state.rv_page == "lab"
for index in range(1, 16):
    sid = f"SCN-{index:02}"
    app.selectbox(key="rv_all_scenarios").select(sid).run()
    app.button(key="use_scenario").click().run()
    assert "rv_result" not in app.session_state
    app.button(key="run_gateway").click().run()
    no_errors(app)
    result = app.session_state.rv_result
    flow = process_steps(result)
    assert len(flow) == 4
    assert all(len(item[1]) > 15 for item in flow)
    path, line, excerpt = decision_source(result)
    source = (ROOT / path).read_text(encoding="utf-8").splitlines()
    assert excerpt == "\n".join(source[line - 1:line - 1 + len(excerpt.splitlines())]).rstrip()
    assert len(app.code) >= 2
    if result.provider_invoked:
        assert flow[1][2] == "done", (sid, flow)
        assert "local mock" in flow[2][1]
    if sid == "SCN-02":
        assert "mia.brooks@example.test" not in result.provider_payload.ticket_text
        assert "MASKED_EMAIL_ADDRESS" in result.provider_payload.ticket_text
        assert "email address" in flow[0][1]
    if sid == "SCN-04":
        assert "payment card number" in flow[0][1]
        assert flow[2][0] == "External API not called"
    if sid in ["SCN-03", "SCN-04", "SCN-05", "SCN-06", "SCN-07", "SCN-14"]:
        assert result.provider_invoked is False
        assert result.provider_payload is None
    assert app.session_state.rv_receipt.scenario_id == sid
print("PASS: 15 scenarios, result reset, masking, provider suppression, evidence association")

app.button(key="nav_aws").click().run()
no_errors(app)
for index in range(9):
    app.selectbox(key="rv_aws_picker").select(index).run()
    no_errors(app)
    assert len(aws_test_text(f"AWS-T{index+1:02}")) > 50
print("PASS: 9 AWS evidence views")

app.button(key="nav_governance").click().run()
for index in range(4):
    app.button(key=f"risk_{index}").click().run()
    no_errors(app)
app.button(key="governance_Frameworks & law").click().run()
for name in ["NIST CSF 2.0", "NIST AI RMF", "GDPR", "GLBA safeguards"]:
    app.button(key=f"framework_{name}").click().run()
    no_errors(app)
assert not any(button.label == "Launch recommendation" for button in app.button)
app.button(key="governance_Risks & mitigations").click().run()
no_errors(app)
print("PASS: risks, mitigations, residual risks, and framework views; launch tab removed")

app.button(key="nav_approach").click().run()
for index in range(5):
    app.button(key=f"approach_{index}").click().run()
    no_errors(app)
app.button(key="nav_overview").click().run()
no_errors(app)
assert app.session_state.rv_page == "overview"
print("PASS: 5 approach views and return navigation")
