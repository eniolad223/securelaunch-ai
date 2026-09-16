# SecureLaunch AI Preliminary Risk Candidate Log

**Purpose:** Preserve risks and design questions discovered before the formal PASTA threat model and risk register  
**Status:** Working record reconciled to the evidence-backed portfolio scope on September 7, 2026; entries are not yet scored or assigned final risk IDs

## How evidence will be described

The portfolio will not treat a design idea as proof. Every later safeguard and claim will use one of four labels:

- **Design-only:** shown in the fictional AWS production reference architecture but not deployed.
- **Prototype-tested:** exercised by the local Python/Streamlit security gateway, local HTTP mock transport, and automated tests.
- **AWS-lab-tested:** exercised against a versioned Amazon Bedrock Guardrail with synthetic text through `ApplyGuardrail`; no foundation model or TP-AI-01 is involved.
- **Provider-evidence-required:** dependent on a real provider's contract, assurance report, configuration, or test evidence that does not exist in this fictional case study.

These labels prevent the prototype from being mistaken for a production audit or a full AWS implementation.

## RC-01 — Sensitive information in free-form ticket text may reach the external AI provider

**Raised by:** Eniola during Signal architecture review on September 4, 2026

### Why this is credible

Customer instructions and separate structured fields reduce mistakes but cannot guarantee correct behavior. A customer may paste personally identifiable information, payment details, credentials, private business identifiers, or other confidential content into the ticket-description field. Signal must retrieve that original text to summarize it, so an incomplete inspection step could send sensitive content across the external-provider boundary.

### Potential consequences

- Disclosure of personal or confidential business information to an unintended processor
- Violation of customer expectations, provider terms, retention requirements, or privacy obligations
- Sensitive values appearing in provider, application, or diagnostic logs
- Reputational harm and the need for incident investigation and notification

### Locked architecture safeguards; formal effectiveness review remains pending

1. Place clear just-in-time warnings beside the free-form ticket field and provide appropriate structured fields, while treating this as guidance rather than a security boundary.
2. Allow-list the structured fields that Signal may use; ignore all other request fields and every attachment.
3. Normalize supported text and encodings before inspection so basic formatting or representation changes are less likely to bypass pattern rules.
4. Run deterministic server-side checks for predictable formats such as Social Security numbers, payment-card candidates with checksum validation, bank-routing patterns, credentials, API keys, and LindenArc-specific customer or payment identifiers.
5. Apply a versioned Amazon Bedrock Guardrail through its independent `ApplyGuardrail` API and, in the production reference design, a private VPC endpoint. Use built-in contextual PII detection plus approved custom regular expressions without invoking a Bedrock foundation model. The portfolio lab tests the Guardrail itself from AWS CloudShell; it does not deploy the private endpoint.
6. Block the Signal request entirely for prohibited high-risk data such as authentication secrets, Social Security numbers, or payment credentials. Route the ticket to ordinary manual support instead.
7. Mask lower-risk direct identifiers such as names, email addresses, phone numbers, and addresses with typed placeholders when the remaining text is still useful.
8. Build the final provider request and have a separate outbound gate inspect the exact serialized payload. It allow-lists keys, enforces size limits, rejects attachments and forbidden identifiers, and reruns the highest-risk checks.
9. Inspect the external model's response again before storage or display because outputs can repeat or invent sensitive-looking content.
10. Keep the original ticket in Aurora. Process the minimized working copy in memory and do not place raw text, detector traces, prompts, or model responses in ordinary logs.
11. If the two inspections disagree, or either is unavailable, unsupported, malformed, timed out, or uncertain above the approved threshold, fail closed: do not call the external provider and leave the original ticket available for manual handling.
12. Limit egress to the approved TP-AI-01 endpoint and require provider terms for no training, bounded retention and deletion, controlled subprocessors, and incident notice. These measures reduce the impact of a missed detection but do not replace content inspection.

**Architecture decision recorded:** September 5, 2026. These controls are now part of the proposed design, not evidence that RC-01 is resolved. Automated detection can still miss context-dependent confidential information, so residual risk, test performance, and release acceptability remain for PASTA and the focused risk register.

### Evidence to require later

- **Prototype-tested:** approved field allow-list, normalization and sensitive-data rule catalog implemented in Python.
- **Prototype-tested:** fixed synthetic cases for email masking and for blocking Social Security number candidates, payment-card candidates, bank references, API keys, and LindenArc-specific identifiers.
- **Prototype-tested:** attachments and unapproved fields never enter the provider payload; a high-risk value reintroduced during serialization is caught by the final gate.
- **Prototype-tested:** blocked cases show `provider_invoked = false`, meaning the local HTTP mock transport was not reached. The portfolio never calls a real provider.
- **Prototype-tested:** sample minimized payload, controlled mock response, response-validation result, and sanitized event record contain no raw detected value.
- **AWS-lab-tested:** Guardrail identifier, version, Region, configuration summary, synthetic input, expected result, actual `ApplyGuardrail` result, and test date.
- **Design-only:** PrivateLink, Network Firewall, NAT Gateway, Lambda, production IAM, and provider-endpoint restrictions remain reference-architecture controls rather than lab evidence.
- **Provider-evidence-required:** TP-AI-01 retention, training-use, deletion, subprocessor, incident, and endpoint-control evidence.
- Recorded limitations, including context-dependent data the deterministic rules can miss, false positives, unsupported input, and Guardrail or gateway failure behavior.

### Later traceability work

This candidate will be connected to the relevant data flow, PASTA threat, risk-register entry, safeguards, evidence, and release gate. Likelihood and impact will be scored only after the formal threat analysis.

## RC-02 — Incorrect issue classification or troubleshooting guidance may mislead a support agent

**Raised by:** Eniola during Signal product-scope review on September 4, 2026

### Why this is credible

Troubleshooting suggestions could save support-agent time, but a language model can misunderstand the issue, invent a procedure, recommend an excessive action, or present an uncertain answer confidently. This is especially important in a financial-operations platform.

### Approved controlled design

Signal would not invent troubleshooting instructions. Instead:

1. The model may select one value from a small, approved issue-category list and return uncertainty when no category fits.
2. LindenArc validates that the returned category is on the allow-list.
3. The application retrieves a versioned, human-authored troubleshooting checklist for that category from Aurora.
4. The support agent sees the checklist as **Suggested approved starting steps** and remains responsible for deciding what applies.
5. No checklist step executes automatically, changes data, grants access, or initiates a payment.
6. An unknown, invalid, or low-confidence category produces no troubleshooting suggestion.

This approach adds practical value without adding retrieval-augmented generation, a vector database, or unrestricted generative advice.

### Evidence to require later

- Approved issue-category list and owner
- Versioned troubleshooting playbooks and review dates
- **Prototype-tested:** controlled mock responses for an approved category, `unknown`, invalid category, malformed schema, oversized output, sensitive-looking output, and simulated timeout or provider failure.
- **Prototype-tested:** the interface shows the selected synthetic ticket, validated draft, approved checklist or safe manual-handling state, and human-review warning.
- **Prototype-tested:** no code path or credential capable of calling an application, customer-message, or payment API exists in the portfolio application.
- **Provider-evidence-required:** real model accuracy, factuality, category performance, and change behavior. A deterministic mock response does not prove those qualities.

### Decision status

Approved by Eniola on September 4, 2026. The scenario charter and Signal architecture now specify allow-listed issue classification followed by a versioned, human-authored playbook. The risk remains open for formal PASTA analysis, scoring, safeguards, evidence, and release-gate treatment.

## RC-03 — A critical payment-provider failure or compromise may harm LindenArc customers

**Raised by:** Eniola during payment-provider boundary review on September 5, 2026

### Why this is credible

The licensed payment provider is a separate third party, but LindenArc depends on it to collect banking details, safeguard provider tokens, execute payments, and report authoritative status. Outsourcing those functions reduces the sensitive data inside LindenArc; it does not remove LindenArc's third-party, operational, contractual, or reputational risk.

A provider incident would not automatically compromise LindenArc's AWS account, VPC, or Aurora database because the provider has no direct access to them. Harm could still cross the boundary through the trusted API and webhook connection, incorrect or unavailable provider information, exposed data held by the provider, compromised provider credentials or signing keys, or LindenArc's dependence on the provider for customer-facing service.

### Candidate incident scenarios

- A provider breach exposes customer funding or payee information held outside LindenArc.
- A compromised provider account, API, signing key, or client certificate produces fraudulent instructions, false status events, or misleading onboarding references.
- Weak provider access control, tenant isolation, separation of duties, or insider controls permits unauthorized activity.
- A provider or one of its subprocessors becomes unavailable, leaving payments delayed or in an unknown state.
- The provider's records and LindenArc's records disagree, creating a risk of duplicate, misdirected, or incorrectly reported payments.
- The provider responds slowly or incompletely to an incident, preventing LindenArc from investigating, notifying customers, or recovering promptly.

### Potential consequences

- Fraudulent, duplicated, delayed, or misdirected payments
- Exposure of customer banking or business information
- Incorrect payment status displayed to customers
- Business interruption, investigation, notification, recovery, and contractual costs
- Loss of customer trust even when LindenArc's own AWS environment was not breached

### Candidate layered safeguards

1. Classify the payment provider as a critical third party and complete risk-based due diligence before launch, at least annually, and after a material service, ownership, subprocessor, or security change.
2. Verify the provider's applicable authorization or licensing rather than relying on marketing language.
3. Review appropriate independent evidence such as a current SOC 2 Type II report, any bridge letter, penetration-test summary, material findings and remediation status, and business-continuity or disaster-recovery test evidence. PCI DSS evidence is required only if cardholder data is actually in scope.
4. Require evidence addressing multi-factor authentication, role-based and privileged access, separation of duties, encryption, token protection, tenant isolation, secure development, vulnerability management, logging, incident response, key rotation, backups, recovery objectives, and subprocessor governance.
5. Put data use, retention, deletion, subprocessor notice, breach notification, investigation cooperation, service levels, evidence or audit rights, termination, portability, and secure deletion requirements into the contract.
6. Preserve LindenArc's technical boundary: no provider access to the VPC or database, least-privilege provider credentials, controlled outbound destinations, mutual TLS, message signatures, timestamps, replay protection, stable idempotency, immutable approvals, reconciliation, anomaly alerts, and a payment-dispatch kill switch.
7. Include the provider in incident-response and recovery exercises and define who pauses payment dispatch, communicates with customers, preserves evidence, and authorizes restart.
8. Do not launch—or pause new payment dispatch—when critical evidence is missing, a serious unresolved weakness exists, provider trust material is compromised, or authoritative status cannot be established.

### Evidence to require later

- Completed provider risk assessment, risk owner, approval decision, and reassessment date
- Licensing verification and provider/subprocessor inventory
- Current independent assurance evidence with exceptions and remediation tracked
- Signed security, privacy, incident-notification, recovery, service-level, and exit terms
- Integration tests for invalid certificates, signatures, timestamps, replayed events, duplicate requests, conflicting statuses, timeouts, and provider outages
- Reconciliation records, provider-credential rotation evidence, incident tabletop result, and payment-dispatch pause/restart procedure

### Later traceability work

This candidate may be separated into confidentiality, integrity, availability, and incident-coordination risks during the formal PASTA analysis. Likelihood, impact, risk ownership, and residual risk acceptance will be decided only after that analysis. The project will describe simulated due diligence and launch requirements; it will not claim that LindenArc audited or certified a real provider.

## RC-04 — Reusable support knowledge may retain sensitive, inaccurate, or unsafe ticket information

**Raised by:** Eniola during data-retention review on September 5, 2026

### Why this is credible

Deleting every useful lesson with a sensitive support ticket can force future agents to repeat lengthy investigations. However, retaining an agent's free-form closing note or an AI-generated summary for broad reuse could preserve customer identifiers, confidential business facts, credentials, payment references, inaccurate troubleshooting steps, prompt-injected content, or tenant-specific details long after the original case should have been deleted.

### Candidate safe design for Phase 3 review

The original ticket, case-closing note, and reusable knowledge record remain separate:

1. The original ticket and its attached closing note remain Confidential and follow the support-case retention schedule.
2. A useful resolution may be nominated for a new, structured knowledge record containing only generalized symptoms, validated steps, resolution, limitations, applicable product version, owner, and review date.
3. Customer and tenant names, user identifiers, ticket prose, attachments, exact customer amounts, payment references, secrets, and other unnecessary case facts are prohibited.
4. Server-side DLP inspection and a designated human reviewer both check the draft. An ordinary agent or Signal cannot publish it automatically.
5. The record becomes Internal only after accuracy, de-identification, and publication approval. A failed check leaves it blocked as Confidential or Restricted.
6. Articles are versioned, reviewed at least annually, and retired when outdated or unsafe.
7. Signal-assisted closure drafting is outside the initial release. Adding it later requires a new data flow, focused threat review, and test evidence.

### Potential consequences

- Cross-tenant disclosure or unnecessary long-term retention of customer information
- Exposure of credentials, payment references, or internal technical details
- Incorrect or outdated steps causing support errors or unsafe changes
- Malicious ticket content influencing material later treated as trusted guidance
- Loss of provenance, ownership, or accountability for troubleshooting instructions

### Evidence to require later

- Structured closing-note and knowledge-record templates
- Prohibited-field and de-identification rules
- Synthetic DLP tests, including context-dependent and intentionally disguised identifiers
- Role test proving ordinary agents and Signal cannot publish directly
- Human approval record, source-case provenance control, version history, and annual-review result
- Test proving that deleting the source ticket does not leave its text or attachments embedded in the knowledge record

### Later traceability work

This candidate will be evaluated during PASTA and may become separate confidentiality and integrity risks. The Phase 3 data inventory records the proposed DATA-16 knowledge family and RS-10 retention schedule; final approval remains with Eniola after review.

## RC-05 — Automation bias may cause support agents to rely on inaccurate Signal output

**Raised by:** Eniola during PASTA Stage 1 objective review on September 5, 2026

### Why this is credible

A statement that “the human reviews the output” does not prove meaningful oversight. As Signal becomes familiar, busy agents may stop comparing its summary and selected category with the original ticket. A confirmation control can become a routine click, especially when the model is usually correct or workloads are high. This is automation bias: excessive reliance on an automated recommendation.

The model does not generate troubleshooting steps, but an incorrect category can cause LindenArc to display the wrong approved playbook. A summary may also omit a critical fact or state something unsupported. The absence of autonomous payment or account permissions limits the maximum technical effect but does not eliminate support-quality, privacy, integrity, or customer-trust harm.

### Initial model lifecycle decision

LindenArc will use a pretrained external foundation model for inference. It will not train or fine-tune the model with production customer tickets in the initial release, and the provider must not use LindenArc inputs or outputs for its own model training.

LindenArc improves the system through versioned prompts, schemas, category definitions, DLP and validation rules, synthetic test cases, human-approved playbooks, model-version selection, structured corrections, and monitored release changes. Production feedback does not automatically become training data.

### Candidate layered safeguards

1. Build a human-reviewed synthetic evaluation set covering ordinary, long, ambiguous, contradictory, incomplete, sensitive-data, prompt-injection, and `unknown` cases.
2. Declare quality and safety thresholds before running the release evaluation so results are not reinterpreted after the fact.
3. Measure material omissions, unsupported facts, category corrections, `unknown` behavior, DLP leakage, validation failures, and agent overrides—not merely whether the response had valid JSON.
4. Display the original ticket beside the draft and make correction simple. Show only source excerpts that the application verifies occur in the minimized source text; never accept invented evidence.
5. Require full manual handling for defined risk signals such as DLP intervention, conflicting or missing facts, `unknown`, failed validation, or a security-sensitive case. Do not rely only on the model's own confidence statement.
6. Use risk-based sampled quality review and periodically measure whether agents are actually checking, correcting, or overriding Signal.
7. Train agents on Signal's limits and automation bias, but do not treat training as the only control. Monitor workload so meaningful review is operationally possible.
8. Pin and record the model and configuration versions. Reevaluate before changing the model, prompt, schema, categories, DLP rules, validation, or playbooks.
9. Define thresholds that trigger investigation, increased sampling, rollback, or the Signal kill switch.
10. Keep structured feedback and quality telemetry free of raw ticket text; future customer-data fine-tuning requires a separate privacy and security approval.

### Evidence to require later

- Synthetic evaluation cases, expected results, reviewer identities, and predeclared thresholds
- Results by failure type and issue category rather than one misleading overall accuracy number
- **Prototype-tested:** user-interface evidence showing fixed synthetic source text, controlled draft, verified source support, correction, and manual-handling states.
- Structured feedback fields, sampled-review plan, agent training, workload review, and oversight-effectiveness metrics
- Model/configuration inventory, change-evaluation result, rollback test, and kill-switch test
- Provider term prohibiting training on LindenArc input/output and proof that no automatic production-training flow exists

The prototype can prove that these interface and fail-safe states exist. It cannot prove that real support agents will resist automation bias over time; that requires a controlled pilot, operational metrics, and human-factors evidence in a real organization.

### Later traceability work

This candidate will feed PASTA threat, weakness, attack-scenario, and risk analysis. It may separate into summary factuality, category misclassification, automation-bias, and model-change risks when final risks are prioritized.

## RC-06 — The external AI model service may expose data, change behavior, fail, or depend on an unsafe supply chain

**Raised by:** Eniola during PASTA Stage 1 provider-boundary clarification on September 5, 2026

### Why this is credible

LindenArc does not download or operate the underlying model. TP-AI-01 hosts the model and inference service, processes the approved Signal payload, returns the response, and controls important parts of the service lifecycle. TP-AI-01 may also rely on an upstream model developer, cloud host, or other subprocessor. A weakness or unannounced change in that chain can affect LindenArc even when LindenArc's AWS controls work as designed.

### Candidate incident scenarios

- TP-AI-01 retains LindenArc input or output longer than approved or uses it for provider training.
- A provider breach, insider, logging error, or subprocessor exposes minimized ticket content or generated responses.
- A model or safety configuration changes without sufficient notice, causing new omissions, unsupported statements, classification errors, or prompt-injection behavior.
- Provider access control, API credentials, tenant isolation, encryption, deletion, or vulnerability management is inadequate.
- A provider outage, rate limit, regional failure, contract termination, or sudden service change interrupts Signal or creates unexpected cost.
- Model/service provenance or subprocessor use is unclear, preventing LindenArc from understanding where data travels and who can access it.
- Provider-generated identifiers, telemetry, or responses contain unexpected sensitive information that LindenArc logs or stores improperly.

### Potential consequences

- Unauthorized external disclosure or secondary use of customer-derived information
- Cross-customer exposure inside the provider service
- Declining Signal accuracy or safety after a provider/model change
- Inability to investigate, delete, recover, or notify customers promptly
- Signal outage, cost escalation, emergency rollback, or delayed support work
- Contractual, privacy, operational, and customer-trust harm

### Candidate layered safeguards

1. Classify TP-AI-01 as a critical third party and perform due diligence before use, at least annually, and after material model, service, ownership, location, or subprocessor changes.
2. Obtain appropriate independent assurance evidence, penetration-test summary, material findings and remediation status, secure-development and vulnerability-management evidence, incident-response and recovery evidence, and access/tenant-isolation information.
3. Contractually define permitted data use, no training on LindenArc inputs/outputs, bounded retention, deletion, encryption, location, subprocessor notice, incident notification, investigation cooperation, service levels, model/change notice, evidence rights, portability, and exit.
4. Require relevant model/service provenance and version identification without assuming TP-AI-01 created the underlying model itself.
5. Send only DATA-06 through controlled egress, use least-privilege credentials, exclude attachments/tools/payment data, validate all output, and keep raw content out of telemetry.
6. Pin or record the approved model and Signal configuration version, rerun evaluation before material changes, monitor production quality, and roll back when thresholds fail.
7. Use bounded timeouts, retries, rate and cost limits, a dead-letter queue, manual support fallback, and the Signal kill switch.
8. Maintain an exit plan that can disable TP-AI-01 without disabling ticket handling; a replacement provider cannot be used until separately assessed and evaluated.

### Evidence to require later

- Completed TP-AI-01 assessment, accountable owner, approval and reassessment date
- Provider architecture/supply-chain disclosure and relevant subprocessor list
- Current independent security evidence, exceptions and remediation status
- Signed data-use, training, retention, deletion, incident, change, availability and exit terms
- Model/service version inventory and change notifications
- Synthetic evaluation before launch and after material provider changes
- Egress, credential, logging, failover, rate-limit, rollback and kill-switch tests

The local HTTP mock transport is not TP-AI-01 and supplies none of this third-party evidence. It only proves how LindenArc-controlled prototype code behaves when a simulated API request succeeds, returns an unsafe response, times out, or fails.

### Later traceability work

This candidate will be analyzed separately from TP-PAY-01. PASTA may divide it into confidentiality, supply-chain/change, availability, and cost risks. The portfolio will perform focused simulated due diligence, not claim a real audit of an AI provider.

## Portfolio-lab safety controls

These controls protect people who view or run the portfolio; they are not claims about LindenArc's fictional production environment:

1. The public Streamlit deployment provides only fixed, reviewed synthetic scenarios. It accepts no unrestricted text, file upload, credential, or customer record.
2. The provider adapter targets the reserved fictional host `tp-ai-01.invalid` and is constructed only with HTTPX `MockTransport`. There is no live-provider mode or network fallback.
3. Test and demonstration logs store rule identifiers and outcomes, never the raw value that triggered a rule.
4. AWS credentials and provider secrets are absent from the repository, GitHub Actions, fixtures, screenshots, and Streamlit deployment.
5. GitHub Actions uses least-privilege read-only repository permissions, exact dependency versions, and actions pinned to full commit identifiers.
6. The limited AWS lab uses only reviewed synthetic text and records sanitized configuration and result evidence. It does not call a foundation model.
7. Any accidentally submitted real or sensitive value is excluded from public evidence and handled as an incident rather than converted into a test fixture.
