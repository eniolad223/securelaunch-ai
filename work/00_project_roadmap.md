# SecureLaunch AI Project Roadmap

**Status:** Foundation, seven-stage PASTA analysis, risk/control package, and Signal Security Gateway prototype approved; AWS Guardrails lab is now in progress  
**Target:** A medium-scope, interview-defensible cloud-security case study supported by a working security-control prototype and limited AWS lab  
**Estimated focused time remaining after the risk/control package:** Approximately 10–14 hours  
**Python decision:** The former risk-report automation extension is retired. Python now implements and tests the Signal security gateway as a core deliverable.

## Project outcome

SecureLaunch AI will determine whether the fictional LindenArc Signal feature is ready to launch within the LindenArc multi-tenant financial-operations SaaS platform.

The final recommendation will combine documented analysis with reproducible evidence from a small Python application, automated tests, and a limited Amazon Bedrock Guardrails experiment using synthetic data. The project remains a simulation: it is not a real audit, production deployment, compliance claim, or client engagement.

## Three evidence layers

| Layer | What it proves | What it does not prove |
|---|---|---|
| Reference design | Eniola can design and reason about an AWS-hosted multi-tenant system, its data flows, providers, threats, and safeguards | That the full architecture was deployed, audited, or operated in production |
| Python validation application | Selected gateway controls behave as designed against repeatable synthetic cases | That a prototype detector or local mock transport is production-grade or represents a real provider |
| AWS Guardrails lab | Eniola can configure and test a real managed AWS guardrail through `ApplyGuardrail` | That the fictional production VPC, PrivateLink, Network Firewall, external AI provider, or end-to-end system was deployed |

These are three sources of portfolio evidence. The separate label **provider-evidence-required** is not a fourth test layer; it marks claims that cannot be proven without a real provider's records, contract, or operational evidence.

## Working sequence

| Phase | Work product | Estimated focused time | Status |
|---|---|---:|---|
| 1 | Scenario charter and scope boundaries | 0.5 hour | Complete |
| 2 | AWS architecture and numbered data flows | 1.5–2 hours | Complete |
| 3 | Data inventory and lifecycle | 1 hour | Complete, audited and corrected |
| 4 | Reconcile all existing artifacts to the evidence-backed scope | 0.75–1 hour | Complete, September 7, 2026 |
| 5 | Complete PASTA Stages 2–7 | 2–3 hours | Complete, September 9, 2026 |
| 6 | Focused 10-risk register, heatmap, safeguards, and prototype test requirements | 1–1.5 hours | Complete, approved September 9, 2026 |
| 7 | Build the integrated Python/Streamlit Signal Security Gateway Lab | 4–5 hours | Complete and visually approved September 13, 2026 |
| 8 | Add a compact automated suite covering approximately 12–15 security scenarios and a least-privilege GitHub Actions workflow | 1.5–2 hours | Local suite complete with 43 passing tests; GitHub Actions remains |
| 9 | Configure and test one Amazon Bedrock Guardrail with synthetic inputs | 1–1.5 hours | In progress; lab design re-audited September 13, 2026 |
| 10 | Connect test results to safeguards, evidence, release gates, secure-SDLC gates, responsible-AI review, and the limited readiness crosswalk | 1.5–2 hours | Not started |
| 11 | Produce the executive launch decision, public README, Streamlit deployment, LinkedIn presentation, and final QA | 2–3 hours | Not started |

## Final technical product

The repository will contain one integrated application, not several disconnected Python projects:

1. A Streamlit screen using a fixed set of synthetic scenarios in the public deployment.
2. A reusable Python gateway that allow-lists fields, normalizes text, detects sensitive patterns, masks permitted identifiers, blocks prohibited data, builds the final payload, and runs the final outbound gate.
3. A mock HTTP transport that captures requests for the reserved fictional host `tp-ai-01.invalid` locally and returns controlled TP-AI-01-style responses without contacting a real provider or offering a live-network fallback.
4. An output validator enforcing schema, size, plain-text treatment, and the approved category list or `unknown`.
5. Automated tests covering pass, mask, block, prompt manipulation, payload reintroduction, invalid output, timeout, safe logging, and manual fallback.
6. Sanitized evidence records connecting risk, safeguard, test, result, and release gate.
7. A separate AWS lab script or command file that submits the same synthetic cases to Amazon Bedrock `ApplyGuardrail` through AWS CloudShell.

The September 11 technical-design audit also locked five focused implementation features: a versioned security-policy file, LindenArc-owned versioned playbook lookup, a stage-by-stage visual security trace, fail-closed and kill-switch demonstrations, and downloadable sanitized evidence receipts. A separate model-grounding or hallucination-detection system is not being added. The prototype will perform the already-required strict response validation, while real-model quality remains a separate evaluation and provider-evidence requirement.

The public Streamlit application will not accept unrestricted free text, file uploads, real credentials, or real customer data. It will use fixed reviewed scenarios and a local mock transport only. No AWS credential or provider secret will be placed in the repository, GitHub Actions, or Streamlit deployment.

Before the AWS lab runs, the current AWS price will be checked, a small case limit and spend ceiling will be recorded, and billing/resource cleanup will be reviewed after evidence is captured. The project will not rely on an assumed free tier or subscription.

## Controlled wow-factor features

### 1. End-to-end decision traceability

Important items will receive simple identifiers so a reviewer can follow the reasoning:

`Data flow → Threat → Risk → Safeguard → Evidence → Release gate`

Example: `DF-07 → T-04 → R-03 → SG-06 → EV-07 → RG-03`.

This demonstrates that the project is a connected security analysis rather than a collection of unrelated documents.

### 2. Inherent-versus-residual risk heatmap

The portfolio will visually compare risk before safeguards with expected risk after safeguards. It will remain a small, explainable matrix rather than a complex quantitative model.

### 3. Interactive evidence-backed demonstration

The public Streamlit screen will demonstrate multiple reviewed synthetic cases, including sensitive-data masking, prohibited-data blocking, a harmless prompt-injection attempt, invalid provider output, and provider failure. Technical reviewers can inspect and rerun the same cases in the automated test suite.

### 4. Executive and technical views of the same decision

The one-page executive brief will explain the launch decision in business language, while the supporting artifacts will show the technical evidence behind it.

### 5. Real but bounded AWS evidence

The Bedrock Guardrails lab will use a real AWS account and real `ApplyGuardrail` evaluations with synthetic data. It will not invoke a foundation model or deploy the fictional production architecture. Sanitized configuration and results will be retained as evidence.

### 6. Public interactive access

The tested Streamlit application will be deployed from the public GitHub repository so a nontechnical reviewer can understand the control flow while a technical reviewer can inspect the same underlying code and tests.

## Scope controls

The project will not expand into:

- a production SaaS application;
- a live payment integration;
- a live TP-AI-01 integration or real model inference;
- a full AWS deployment;
- deployment of Aurora, Cognito, Lambda, Network Firewall, NAT Gateway, PrivateLink, or the fictional multi-account environment;
- a penetration test;
- hundreds of framework controls;
- a claim of audit, certification, or compliance;
- a production AI model evaluation program; or
- a second Python risk-reporting project or a large portfolio website.

If time becomes tight, the number of risks, mappings, and cosmetic features will be reduced. The integrated visual, core gateway, automated tests, limited AWS lab, source traceability, honest evidence labels, and Eniola's understanding will not be cut.

## Completion criteria

The project is complete only when:

- every public claim is labeled as design-only, prototype-tested, AWS-lab-tested, or provider-evidence-required;
- all synthetic fixtures are reviewed to exclude real personal, employer, school, customer, and credential data;
- blocked cases demonstrably cause no mock HTTP provider invocation;
- the final serialized payload and returned response are both validated;
- automated tests pass locally and through GitHub Actions with read-only repository permissions and no secrets;
- AWS evidence identifies the guardrail version, Region, test case, expected result, actual result, date, and limitations;
- the AWS lab records the price check, case limit, approved spend ceiling, and cleanup result;
- the public Streamlit deployment exposes only fixed synthetic scenarios and contains no external-provider or AWS credentials;
- the final launch recommendation traces material risks to safeguards, evidence, and release gates; and
- the responsible-AI verification log records at least one AI error, omission, or changed recommendation and Eniola's final decision;
- Eniola can explain and defend every public artifact.

## Current reference baseline

- WGU D320 course knowledge and the assigned third-edition study guide for course-derived concepts
- AWS SaaS Architecture Fundamentals and AWS Well-Architected Security guidance
- NIST Cybersecurity Framework 2.0
- NIST AI Risk Management Framework 1.0 and the Generative AI Profile, NIST AI 600-1
- OWASP Top 10 for LLM Applications for current AI abuse cases
- ISO/IEC 27017:2026 for current cloud-control themes, with the textbook's 2015 edition clearly distinguished
- AICPA Trust Services Criteria for a limited SOC 2 readiness mapping

These references support a readiness analysis. They do not establish compliance.
