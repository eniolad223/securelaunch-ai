# LindenArc Third-Party Provider Register

**Status:** Provider baseline reconciled to the evidence-backed portfolio scope on September 7, 2026; formal risk scoring remains pending  
**Scope:** Focused simulated due diligence; not a real provider audit, certification, or endorsement

## Why this register exists

LindenArc depends on three external provider organizations. Two are application-specific integrations, while AWS supplies the underlying cloud platform. Permanent identifiers prevent the words “the provider” from hiding which relationship is being discussed.

| Provider ID | Provider role | What it supplies to LindenArc | What it receives or holds | What it does not receive or control | Primary review focus |
|---|---|---|---|---|---|
| CSP-01 | Amazon Web Services, cloud service provider | Managed cloud infrastructure and services used by the reference architecture | LindenArc data placed in approved AWS services under the selected configurations | Ownership of LindenArc's business decisions, application authorization, tenant rules, prompts, or risk acceptance | Shared responsibility, service configuration, region, resilience, logging, encryption, recovery, assurance evidence, subprocessors, incident and exit considerations |
| TP-AI-01 | External AI Model Service Provider | Authenticated access to a hosted pretrained language-model inference API, provider-operated model hosting and compute, identified model/service version, response and technical usage metadata | Only the approved DATA-06 minimized Signal request and the generated response under contracted retention and no-training terms | Direct access to LindenArc's VPC, Aurora, S3 buckets, AWS identities, attachments, payment systems, playbooks, tools, or customer-action APIs | Model/service provenance, training-use prohibition, retention and deletion, encryption, location, subprocessors, access control, secure development, vulnerability management, model changes, evaluation support, incident response, availability and exit |
| TP-PAY-01 | Licensed Payment Execution Provider | Provider-hosted banking onboarding, tokenized funding/payee references, payment execution, authoritative status and reconciliation API | Raw funding/payee details collected directly plus tokenized LindenArc payment instructions | Direct access to LindenArc's VPC, database administration, Signal, customer-support content, or approval authority | Licensing, transaction integrity, token protection, identity and privileged access, separation of duties, tenant isolation, webhook trust, incident response, continuity, recovery, subprocessors, reconciliation and exit |

## Exact AI-provider boundary

TP-AI-01 supplies a managed service, not a copy of a model that LindenArc downloads and owns. The pretrained model and its computing environment remain under the provider's control. LindenArc sends an approved request through an API and receives a response.

The provider may have developed the model itself or may rely on an upstream model developer or hosting subprocessor. The fictional scenario does not assume which. TP-AI-01 remains contractually accountable to LindenArc for disclosing relevant subprocessors and model/service provenance.

LindenArc does not train TP-AI-01's model. It builds Signal around the service by controlling data minimization, prompts, synthetic examples, schemas, categories, output validation, playbook lookup, the support interface, monitoring, evaluation, rollback, and the kill switch.

## Portfolio simulation and lab identifiers

Two technical elements appear in the portfolio but must not be mistaken for additional providers:

| Identifier | What it is | What it proves | What it does not prove |
|---|---|---|---|
| SIM-AI-01 | An in-process HTTPX `MockTransport` that receives the prototype's constructed HTTP request for `https://tp-ai-01.invalid` and returns a controlled response | The LindenArc-controlled gateway invokes its provider adapter only after the payload passes, and it handles expected, malformed, unsafe, failed, and timed-out responses safely | No real network request, real model inference, provider security, provider accuracy, retention, deletion, availability, or contract term |
| LAB-GR-01 | A versioned Amazon Bedrock Guardrail created temporarily in Eniola's AWS account and tested from AWS CloudShell with synthetic text through `ApplyGuardrail` | The recorded Guardrail configuration produces the captured action and assessment for the selected synthetic cases without invoking a foundation model | The full production AWS path, a private endpoint, Lambda, Network Firewall, NAT Gateway, TP-AI-01, or production data handling |

The public Streamlit demonstration uses SIM-AI-01 only. It has no AWS credentials, TP-AI-01 credentials, live-provider setting, or unrestricted user-input path. In the interface, `provider_invoked = true` means the locally intercepted simulated HTTP request reached SIM-AI-01; it never means TP-AI-01 received data.

## Assessment depth

The later risk work will perform a focused, risk-based provider assessment:

- **CSP-01:** evaluate shared-responsibility assumptions and relevant public assurance evidence; do not pretend to audit AWS.
- **TP-AI-01:** evaluate the AI service's security, privacy, model lifecycle, supply chain, operational resilience, and contract requirements.
- **TP-PAY-01:** evaluate the payment service's licensing, security, transaction integrity, resilience, incident coordination, and contract requirements.

The depth is proportional to what each provider can expose or disrupt. This avoids both extremes: ignoring provider risk and expanding the portfolio into three full enterprise vendor audits.

## Traceability

| Entity | Main data flows and boundaries | Existing risk candidates, gates, or evidence status |
|---|---|---|
| CSP-01 | All approved AWS-hosted components; AWS/LindenArc shared-responsibility boundary | Architecture shared-responsibility decisions; LAB-GR-01 supplies narrow Guardrail evidence only; the rest is design-only or provider-evidence-required |
| TP-AI-01 | DF-19, DF-20 and TB-11 | RC-01, RC-02, RC-05, RC-06; LB-02, LB-04, LB-06, LB-08 and LB-11; no real provider is used |
| TP-PAY-01 | DF-25 through DF-33, TB-14 and TB-15 | RC-03; LB-07 |
| SIM-AI-01 | LAB-DF-03 and LAB-DF-04 inside the local prototype boundary | Prototype-tested behavior only; not a third-party assessment |
| LAB-GR-01 | Selected DATA-17 synthetic text submitted to `ApplyGuardrail` inside CSP-01 | AWS-lab-tested Guardrail behavior only; not a foundation-model or provider test |
