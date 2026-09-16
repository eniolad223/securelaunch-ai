"""Concise presentation copy, with evidence and source references."""

AWS_CASES = [
    {"id": "AWS-T01", "name": "Clean support ticket", "decision": "Allow", "source": "Input", "observed": "No intervention. The support request remained usable.", "why": "Security should preserve legitimate support work.", "file": "aws-t01-clean-allow"},
    {"id": "AWS-T02", "name": "Email in ticket text", "decision": "Mask", "source": "Input", "observed": "The email was replaced with {EMAIL}.", "why": "The support problem is useful. The customer's contact address is unnecessary for summarization.", "file": "aws-t02-email-mask"},
    {"id": "AWS-T03", "name": "Phone + account reference", "decision": "Mask", "source": "Input", "observed": "Both identifiers were replaced, including the custom account format.", "why": "Built-in detection and an organization-specific rule preserved the ticket's business context.", "file": "aws-t03-phone-account-mask"},
    {"id": "AWS-T04", "name": "Social Security number", "decision": "Block", "source": "Input", "observed": "The SSN was detected and the request was blocked.", "why": "Restricted identity data should stop this AI processing route.", "file": "aws-t04-ssn-block"},
    {"id": "AWS-T05", "name": "Payment-card details", "decision": "Block", "source": "Input", "observed": "Card number, expiry, and CVV produced three blocking detections.", "why": "Payment details are outside the support summarization purpose.", "file": "aws-t05-payment-card-block"},
    {"id": "AWS-T06", "name": "AWS credentials", "decision": "Block", "source": "Input", "observed": "The example access key and secret key were both blocked.", "why": "Troubleshooting should never require forwarding cloud credentials to an AI provider.", "file": "aws-t06-credentials-block"},
    {"id": "AWS-T07", "name": "Prompt manipulation", "decision": "Block", "source": "Input", "observed": "The direct instruction override was blocked with High confidence.", "why": "Customer text must not override the instructions or security controls around it.", "file": "aws-t07-prompt-attack", "summary": "aws-t07-prompt-attack-block-summary.png"},
    {"id": "AWS-T08", "name": "Harmless quoted instruction", "decision": "Allow", "source": "Input", "observed": "A suspicious phrase quoted as part of an error report was allowed.", "why": "This case checks overblocking: reporting a phrase is different from instructing the system to follow it.", "file": "aws-t08-benign-quoted-text-allow"},
    {"id": "AWS-T09", "name": "Email in simulated AI output", "decision": "Mask", "source": "Output", "observed": "The email in a manually supplied example response was masked.", "why": "The return path needs inspection as well as the outbound path.", "file": "aws-t09-output-email-mask"},
]

DECISIONS = [
    {
        "name": "Minimize exposure", "question": "What does the external AI actually need?",
        "risk": "Free-form support tickets can carry personal details, payment data, secrets, and unrelated attachments.",
        "choice": "Send only approved fields. Mask permitted identifiers. Block restricted content. Inspect the exact outgoing JSON again before a provider call.",
        "value": "Preserve useful support context while reducing unnecessary disclosure.",
        "evidence": "Python request controls and AWS masking/blocking examples", "status": "Prototype + AWS evidence", "ids": "R-03 · SG-05/06/07 · RG-03",
        "file": "work/03_data_inventory_and_lifecycle.md",
        "remaining": "Unknown data formats and prompt attacks can evade selected detectors. Neither the Python tests nor nine AWS cases prove complete coverage.",
        "next_control": "Expand adversarial and false-positive tests, monitor detections, and review new data formats before adding them to the workflow.",
    },
    {
        "name": "Keep people accountable", "question": "What if a convincing AI response is wrong?",
        "risk": "A plausible summary or invented action could mislead a busy support agent.",
        "choice": "Validate the response, restrict issue categories, retrieve human-authored playbooks, and retain human review. Give the AI no payment or account-changing authority.",
        "value": "Support faster understanding without handing business decisions to the model.",
        "evidence": "Unsafe-output rejection, unknown-category fallback, and approved-playbook checks", "status": "Prototype evidence; pilot review still needed", "ids": "R-04 · SG-09/10/11 · RG-04",
        "file": "work/04_pasta_threat_model.md",
        "remaining": "A correctly formatted summary can still be inaccurate, and a person can rely on it too heavily. Schema checks do not establish factual accuracy.",
        "next_control": "Evaluate summary quality against source tickets and test whether support agents can detect errors during a supervised pilot.",
    },
    {
        "name": "Fail safely", "question": "What happens when a dependency fails?",
        "risk": "Timeouts, malformed output, and a disabled service can disrupt support or bypass a required check.",
        "choice": "Stop unsafe processing, use controlled manual fallback, and test the emergency kill switch. The existing support process remains the fallback route.",
        "value": "Keep a service failure from becoming a security exception.",
        "evidence": "Timeout, provider-error, invalid-response, and kill-switch scenarios", "status": "Prototype evidence; operations still needed", "ids": "R-05/06 · SG-10/13 · RG-05/06",
        "file": "work/05_risk_register_and_control_plan.md",
        "remaining": "A local failure simulation does not verify real availability, recovery times, or whether the support team has enough manual capacity.",
        "next_control": "Test recovery and fallback under realistic load, monitor failures, and rehearse the manual support procedure.",
    },
    {
        "name": "Know the control's limits", "question": "What does a data filter leave unresolved?",
        "risk": "Filtering ticket text does not establish tenant isolation, a supplier's handling of retained data, or security of production access.",
        "choice": "Document those risks separately and distinguish implemented, tested controls from proposed safeguards. A passing sample is evidence of one behavior, not proof that every risk is resolved.",
        "value": "Avoid false assurance and direct further security work toward the gaps a filter cannot solve.",
        "evidence": "Data-flow analysis, provider review, and a register of 10 risks", "status": "Analyzed; not validated by the prototype", "ids": "R-01 to R-10 · RG-01 to RG-10",
        "file": "work/05_risk_register_and_control_plan.md",
        "remaining": "Tenant separation, provider retention and training practices, production permissions, and data deletion remain outside these tests.",
        "next_control": "Verify tenant-scoped authorization, review provider contracts and data-use terms, test least-privilege access, and validate deletion and retention controls.",
    },
]

FRAMEWORKS = {
    "NIST CSF 2.0": {
        "type": "Risk framework", "title": "Connect controls to business risk.",
        "body": "Selected CSF outcomes provide a structure for the project's data inventory, risk prioritization, provider review, and protection decisions.",
        "rows": [
            ("ID.AM-03 / ID.AM-07", "Know the data and its routes", "Architecture and data-lifecycle records"),
            ("ID.RA-05 / ID.RA-06", "Prioritize and treat risk", "Risk register, owners, safeguards, release gates"),
            ("PR.DS", "Protect data", "Minimization and inspection prototype; wider protection remains design scope"),
            ("GV.SC-05 / GV.SC-06", "Set supplier requirements", "Provider due-diligence and contract requirements; provider evidence outstanding"),
        ],
        "note": "This is a selected project mapping, not a full CSF assessment or a certification.",
        "url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf", "label": "Read NIST CSF 2.0",
    },
    "NIST AI RMF": {
        "type": "Voluntary AI risk framework", "title": "Evaluate the risks introduced by AI.",
        "body": "The AI Risk Management Framework organizes risk work through Govern, Map, Measure, and Manage. These functions offer a useful lens for this case study.",
        "rows": [
            ("Govern", "Assign accountability", "Human oversight, change control, risk ownership"),
            ("Map", "Understand the use case", "Business purpose, external provider, sensitive data and trust boundaries"),
            ("Measure", "Evaluate the controls", "Automated Python checks and bounded AWS tests"),
            ("Manage", "Choose a response", "Mask/block rules, manual fallback, and launch conditions"),
        ],
        "note": "The mapping shows relevant practices. It does not establish full framework implementation or model safety.",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework", "label": "Read the NIST AI RMF",
    },
    "GDPR": {
        "type": "EU law, where applicable", "title": "Build data protection into the workflow.",
        "body": "If the processing falls within GDPR scope, the organization must consider data minimization, protection by design, processor arrangements, and appropriate security.",
        "rows": [
            ("Article 5(1)(c)", "Minimize personal data", "Exclude unnecessary fields and mask approved identifiers"),
            ("Article 25", "Protect by design and default", "Put inspection before the external-provider request"),
            ("Article 28", "Evaluate processor obligations", "Require suitable contracts and provider evidence"),
            ("Article 32", "Use appropriate security", "Test selected safeguards; broader operational measures remain required"),
        ],
        "note": "Masking alone does not establish anonymity or legal compliance. Applicability, lawful basis, transfers, retention, and other duties require a separate legal assessment.",
        "url": "https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng", "label": "Read the GDPR text",
    },
    "GLBA safeguards": {
        "type": "US rule, for covered institutions", "title": "Keep customer protection in supplier decisions.",
        "body": "The FTC Safeguards Rule requires covered financial institutions to protect customer information and oversee service providers. A fintech label alone does not determine coverage.",
        "rows": [
            ("Risk assessment", "Understand foreseeable exposure", "Data inventory and threat/risk analysis"),
            ("Safeguards", "Protect customer information", "Prototype minimization, inspection, and restricted-data blocking"),
            ("Service providers", "Assess and oversee suppliers", "Documented provider requirements and unresolved evidence"),
            ("Testing", "Check safeguard effectiveness", "Selected Python and AWS results; broader program testing still needed"),
        ],
        "note": "The fictional company is a B2B software provider. Direct coverage and customer contract obligations would need assessment; this is a relevance mapping, not a finding of compliance.",
        "url": "https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know", "label": "Read the FTC guidance",
    },
}

APPROACH = [
    {"label": "01  Ask", "title": "Start with the business need.", "question": "How can support work faster without expanding data exposure?", "action": "I defined the fictional company, the support use case, the external-provider boundary, and the actions the AI must never take.", "proof": "Scenario charter and AWS reference architecture", "file": "outputs/reviewer_documents/01-project-scope-and-security-boundary.docx", "skill": "Requirements analysis · Scope definition"},
    {"label": "02  Analyze", "title": "Follow the data. Identify the risks.", "question": "What new threats and weaknesses does this data flow introduce?", "action": "I traced data through its lifecycle, applied all seven PASTA threat-modeling stages, and connected risks to safeguards, accountable owners, and release evidence.", "proof": "Data inventory, threat model, and risk register", "file": "outputs/reviewer_documents/02-data-lifecycle-and-risk-analysis.docx", "skill": "Security analysis · Risk prioritization"},
    {"label": "03  Build", "title": "Turn the policy into working controls.", "question": "Can I demonstrate the protection before a request is sent?", "action": "I implemented the Python gateway: field minimization, detection, masking/blocking, final payload inspection, response validation, and safe fallback.", "proof": "Working Python gateway and versioned policy", "file": "outputs/reviewer_documents/03-python-security-gateway-technical-report.docx", "skill": "Python · API boundaries · Control engineering"},
    {"label": "04  Validate", "title": "Test the decisions in two environments.", "question": "What evidence shows the controls behave as intended?", "action": "I tested fixed scenarios locally and independently configured Amazon Bedrock Guardrails. I captured expected versus observed outcomes, froze Version 1, and reproduced a result through the API.", "proof": "43 automated checks, 15 local scenarios, 9 selected AWS cases", "file": "outputs/reviewer_documents/04-validation-evidence-report.docx", "skill": "Test design · AWS · Reproducibility"},
    {"label": "05  Reflect", "title": "Know what the evidence proves, and what it does not.", "question": "Which risks did these controls address, and which still need other protections?", "action": "I separated observed test results from assumptions, recorded remaining risks, and connected each gap to further safeguards. The lesson: a working data filter is one layer of protection, not a complete security program.", "proof": "Risk register, control plan, and documented test limitations", "file": "outputs/reviewer_documents/05-risk-treatment-and-project-lessons.docx", "skill": "Evidence and limitations"},
]
