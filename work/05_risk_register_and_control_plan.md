# LindenArc Signal Risk Register and Control Plan

**Status:** Working draft prepared September 9, 2026 for Eniola's review  
**Basis:** Approved seven-stage PASTA analysis in `work/04_pasta_threat_model.md`  
**Current simulated launch decision:** Delay until the mapped release gates are satisfied  
**Scope:** Focused security readiness analysis for the fictional LindenArc Signal feature; not a real audit, certification, penetration test, or production risk acceptance

## 1. Purpose

This document turns the detailed PASTA analysis into an actionable decision package. It connects each material risk to safeguards, evidence, ownership, and a release gate.

The stable decision chain is:

`Objective → data/flow/boundary → threat → weakness → attack scenario → risk → safeguard → evidence → release gate`

## 2. Scoring method

Likelihood and impact each use a project-defined five-point scale. The score is a transparent prioritization aid, not a statistical forecast or a universal NIST, ISO, or SOC formula.

`Risk score = Likelihood × Impact`

| Score | Rating |
|---:|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

- **Inherent risk:** exposure before the proposed safeguards.
- **Projected residual risk:** the target after every mapped safeguard is implemented and verified.
- **Current evidence rule:** because implementation and provider evidence are incomplete, a projected score is not treated as achieved or accepted.

## 3. Focused risk register

| Risk | Cause–event–impact statement | Primary assets | Inherent risk | Treatment | Projected residual | Accountable owner | Current status |
|---|---|---|---:|---|---:|---|---|
| R-01 — Cross-tenant access | If tenant context or object authorization is weak, a valid or compromised user may access another customer's ticket, document, or Signal result, causing severe cross-tenant disclosure or alteration | DATA-04, DATA-05, DATA-07; customer trust | 4×5 = **20 Critical** | Mitigate | 1×5 = **5 Medium** | Application Engineering owner | Open; design-only controls and production negative tests required |
| R-02 — Privileged identity or control compromise | If identities, credentials, dependencies, or deployment controls are weak, an attacker or mistake may change Signal safeguards or evidence, causing broad unauthorized access or silent control failure | DATA-11 through DATA-13; configurations and evidence | 3×5 = **15 High** | Mitigate | 2×4 = **8 Medium** | Platform Security owner | Open; production identity, repository, deployment, and audit evidence required |
| R-03 — Sensitive-data disclosure | If minimization, detection, final-payload inspection, logging, or provider handling fails, Confidential or Restricted information may reach an unauthorized destination, causing privacy, contractual, incident, and customer harm | DATA-04, DATA-06, DATA-13 | 4×5 = **20 Critical** | Mitigate | 2×4 = **8 Medium** | Signal service owner | Open; prototype, AWS-lab, production, and provider evidence required |
| R-04 — Misleading Signal output | If ticket instructions influence the model, validation is incomplete, or human review becomes superficial, Signal may provide a believable false summary or wrong playbook, causing incorrect support handling | DATA-04, DATA-07, DATA-08; support quality | 4×4 = **16 High** | Mitigate | 2×3 = **6 Medium** | Support Operations owner | Open; prototype, real-model, usability, and operating evidence required |
| R-05 — AI-provider dependency | If TP-AI-01 or its supply chain exposes data, changes behavior, returns unsafe output, or becomes unavailable, Signal may disclose information, mislead agents, or stop functioning | DATA-06, DATA-07; Signal availability | 3×4 = **12 High** | Mitigate; transfer limited contractual obligations | 2×4 = **8 Medium** | Third-Party Risk owner for TP-AI-01 | Open; provider-evidence-required |
| R-06 — Resource exhaustion and cost | If size, rate, concurrency, timeout, retry, duplicate, queue, or spending limits are ineffective, abuse or failure may cause backlog, outage, or unexpected cost | Signal processing, queue, provider usage, support availability | 4×3 = **12 High** | Mitigate | 2×2 = **4 Low** | Signal Operations owner | Open; prototype boundary tests and production operational evidence required |
| R-07 — Evidence, deletion, and recovery failure | If logging, deletion, provider erasure, backup expiration, or restore procedures are incomplete, LindenArc may expose evidence, fail to investigate or prove deletion, or restore data that should remain deleted | DATA-04, DATA-06, DATA-13, DATA-15 | 3×4 = **12 High** | Mitigate | 2×3 = **6 Medium** | Data Governance owner | Open; prototype logging and production lifecycle/recovery evidence required |
| R-08 — Unsafe reusable support knowledge | If customer-derived material is reused without de-identification, review, ownership, versioning, and retirement, confidential or unsafe content may become long-lived guidance | DATA-16; customer confidentiality and support integrity | 3×3 = **9 Medium** | Avoid automated publication; mitigate manual publication | 1×2 = **2 Low** | Support Knowledge owner | Open; AI publication excluded and manual-process evidence required |
| R-09 — Signal obtains payment authority | If Signal gains a payment credential, role, tool, queue, database permission, or network path, manipulated output or a compromised worker may initiate or alter financial activity | DATA-09, payment workflow, customer funds | 2×5 = **10 High** | Avoid | 1×5 = **5 Medium** | LindenArc Chief Technology Officer | Open; design and negative isolation evidence required |
| R-10 — Payment-provider compromise | If TP-PAY-01, its signing material, or its integration is compromised or unavailable, false or missing information may expose banking data or cause unauthorized, duplicated, delayed, or misdirected payments | DATA-09, DATA-10; payment integrity and availability | 3×5 = **15 High** | Mitigate; transfer limited contractual obligations | 2×5 = **10 High** | Payment Service owner | Open; provider/integration evidence required and target High risk needs executive acceptance |

## 4. Risk-score rationale

| Risk | Why the inherent likelihood and impact are reasonable | Why the projected score changes |
|---|---|---|
| R-01 | A pooled service repeatedly exposes tenant-addressable objects to authenticated users and support workflows; untreated cross-tenant access is Likely and its impact is Severe | Layered server, application, assignment, and database enforcement makes access Rare, but the impact remains Severe if it occurs |
| R-02 | Privileged accounts and software changes can affect multiple controls; compromise is Possible with Severe reach | Separation, review, short-lived access, testing, monitoring, and rollback reduce likelihood and contain some impact |
| R-03 | Free-form tickets make prohibited content Likely without effective inspection; external disclosure can cause Severe harm | Layered minimization and provider restrictions reduce likelihood and the amount exposed, but detection is not perfect |
| R-04 | Models and busy humans can misinterpret plausible content; misleading output is Likely without validation and sustainable oversight | No tools, strict validation, source comparison, measured review, and rollback reduce both occurrence and consequence |
| R-05 | A critical external service can change, fail, or be compromised; occurrence is Possible and impact Major | Minimization, due diligence, monitoring, fallback, and exit reduce likelihood but cannot remove external dependency impact |
| R-06 | Requests and retries are easy to multiply without limits, while the main harm is operational and financial rather than direct payment authority | Limits, idempotency, alarms, fallback, and isolation make severe amplification Unlikely and limited |
| R-07 | Complex copies, logs, providers, backups, and restores make lifecycle failure Possible with Major investigation or privacy consequences | Sanitized logs, protected evidence, deletion verification, backup aging, and restore testing reduce likelihood and scope |
| R-08 | Knowledge reuse is a plausible manual process with material but bounded harm | Excluding automatic publication and requiring a separate approved record makes occurrence Rare and impact limited |
| R-09 | The approved design has no payment path, but future privilege expansion is credible and the possible impact is Severe | Avoidance, separation, explicit denial, drift detection, and negative tests make the path Rare; financial impact remains Severe |
| R-10 | Provider or integration compromise is Possible and financial/data consequences are Severe | Layered integration and provider controls reduce likelihood, but severe financial impact remains, leaving a High target risk |

### 4.1 Before-and-after risk heatmap

Each risk appears at the intersection of its likelihood and impact. The first matrix shows untreated exposure. The second shows the conditional target **only after** every mapped safeguard and evidence requirement passes.

**Inherent risk — before safeguards**

| Impact ↓ / Likelihood → | 1 Rare | 2 Unlikely | 3 Possible | 4 Likely | 5 Expected |
|---|---|---|---|---|---|
| 5 Severe | — | R-09 (High) | R-02, R-10 (High) | R-01, R-03 (Critical) | — |
| 4 Major | — | — | R-05, R-07 (High) | R-04 (High) | — |
| 3 Material | — | — | R-08 (Medium) | R-06 (High) | — |
| 2 Limited | — | — | — | — | — |
| 1 Negligible | — | — | — | — | — |

**Projected residual risk — after verified safeguards**

| Impact ↓ / Likelihood → | 1 Rare | 2 Unlikely | 3 Possible | 4 Likely | 5 Expected |
|---|---|---|---|---|---|
| 5 Severe | R-01, R-09 (Medium) | R-10 (High) | — | — | — |
| 4 Major | — | R-02, R-03, R-05 (Medium) | — | — | — |
| 3 Material | — | R-04, R-07 (Medium) | — | — | — |
| 2 Limited | R-08 (Low) | R-06 (Low) | — | — | — |
| 1 Negligible | — | — | — | — | — |

The visual movement is meaningful, but it is not proof that risk has already fallen. Today, every risk remains Open. R-10 remains the only projected High risk because LindenArc can reduce the chance of a payment-provider failure but cannot remove its potentially severe financial impact.

## 5. Safeguard register

| Safeguard | Plain-language requirement | Primary risks | Main evidence class |
|---|---|---|---|
| SG-01 — Trusted tenant and object authorization | Derive tenant context on the server and verify that the caller may perform the requested action on the exact object | R-01 | Design and production test |
| SG-02 — Database tenant enforcement | Use transaction-scoped tenant context, PostgreSQL row-level security, parameterized queries, and separate assignment checks | R-01 | Design and production test |
| SG-03 — Strong identity and least privilege | Use MFA, separate workforce and service roles, short-lived credentials, access reviews, secret protection, and explicit denial of unnecessary capabilities | R-01, R-02, R-03, R-09 | Design and production evidence |
| SG-04 — Controlled change and software supply chain | Version prompts/rules/configuration, require review and tests, pin dependencies and workflow actions, scan for secrets/dependencies, log changes, and test rollback | R-02, R-04, R-08, R-09 | Repository, CI, design, and production evidence |
| SG-05 — Input minimization | Allow-list only required ticket fields and exclude attachments, payment references, other tickets, credentials, and unnecessary tenant details | R-03 | Prototype and design evidence |
| SG-06 — Layered sensitive-data detection | Normalize text and combine deterministic rules with a versioned Amazon Bedrock Guardrail; record limitations and fail closed when required checks fail | R-03 | Prototype, AWS-lab, and design evidence |
| SG-07 — Mask/block policy and final outbound gate | Mask only approved lower-risk identifiers, block prohibited data, build the final JSON, reinspect that exact payload, and prevent provider invocation on failure | R-03 | Prototype and automated-test evidence |
| SG-08 — Safe observability | Record identifiers, rule versions, decisions, timing, and errors without raw tickets, prompts, detected values, credentials, or model content; protect evidence from alteration | R-02, R-03, R-07 | Prototype plus design/production evidence |
| SG-09 — Prompt containment and no agency | Separate instructions from untrusted ticket text, keep secrets out of prompts, give the model no tools, and prohibit autonomous actions | R-04, R-09 | Prototype structure, design, and real-model evaluation |
| SG-10 — Strict response validation | Enforce schema, types, size, approved category or `unknown`, sensitive-data checks, plain-text rendering, timeout handling, and rejection before storage/display | R-04, R-05 | Prototype and automated-test evidence |
| SG-11 — Sustainable human oversight | Display the original and draft together, support correction/escalation, define quality thresholds, sample reviews, monitor overrides and omissions, train agents, and test rollback | R-04, R-05 | Prototype interface plus real-model/human operating evidence |
| SG-12 — AI-provider governance | Verify data use, no training, retention, deletion, encryption, location, tenant isolation, provenance, subprocessors, changes, incidents, availability, assurance, and exit | R-03, R-05, R-06 | Provider-evidence-required |
| SG-13 — Reliability, abuse, and cost controls | Enforce size/rate/concurrency limits, timeout, bounded retry with jitter, idempotency, queue/DLQ limits, spending controls, fallback, alarms, and kill switch | R-05, R-06 | Prototype subset plus design/provider/production evidence |
| SG-14 — Monitoring and incident readiness | Alert on DLP blocks, provider errors, abnormal volume/cost, queue growth, configuration changes, isolation failures, and evidence/lifecycle exceptions; test incident roles and shutdown | R-02, R-03, R-05, R-06, R-07, R-10 | Design, production, tabletop, and provider evidence |
| SG-15 — Verified retention, deletion, and recovery | Apply schedules to primary data, S3 versions, logs, queues, providers, and backups; track exceptions; verify deletion; replay the deletion ledger after restore | R-07 | Design and production lifecycle/recovery evidence |
| SG-16 — Safe reusable knowledge | Use a separate structured record, prohibited fields, DLP and technical review, restricted publishing, provenance, owner, version, review date, and retirement | R-08 | Process, role, DLP, and lifecycle evidence |
| SG-17 — Signal/payment isolation | Maintain separate roles, credentials, services, queues, database permissions, egress, administration, and explicit denials; review any proposed action capability as a new scope | R-09 | Design and negative production test |
| SG-18 — Payment-provider and integration integrity | Verify licensing and assurance; use narrow credentials, mutual TLS, signatures, freshness/replay checks, immutable approvals, idempotency, reconciliation, anomaly alerts, incident coordination, pause, and restart controls | R-10 | Provider-evidence-required plus production integration tests |

## 6. Evidence register

| Evidence | Evidence item | Status and honest claim |
|---|---|---|
| EV-01 | Negative API tests using valid identities with other tenants' ticket, result, and object identifiers | Required production/design evidence; not produced by the portfolio prototype |
| EV-02 | Database row-level-security and support-assignment tests | Required production/design evidence; not produced by the portfolio prototype |
| EV-03 | Role matrix, IAM/database policy review, MFA/session configuration, access review, secret scan, and credential-rotation record | Required design/production evidence |
| EV-04 | Protected change workflow, peer-review record, pinned dependency/action versions, automated CI result, secret/dependency scans, configuration history, and rollback test | CI subset can be prototype-tested; full deployment evidence remains design-only |
| EV-05 | Prototype test proving only allow-listed fields enter DATA-06 and attachments/unapproved fields are excluded | Planned prototype evidence |
| EV-06 | Synthetic local tests for clean, masked, blocked, obfuscated, ambiguous, unsupported, and detector-failure cases | Planned prototype evidence; limited to named cases |
| EV-07 | Versioned Amazon Bedrock Guardrail configuration and sanitized `ApplyGuardrail` expected-versus-actual results | Planned AWS-lab evidence; no foundation model or full AWS deployment |
| EV-08 | Exact serialized-payload test proving reintroduced prohibited data is blocked and `provider_invoked = false` | Planned prototype evidence using SIM-AI-01 only |
| EV-09 | Prohibited-log-field test and sanitized event examples containing no raw detected values | Planned prototype evidence; protected production logging remains design-only |
| EV-10 | Prompt template, instruction/data separation, no-secret/no-tool review, and selected real-model prompt-injection evaluation | Structural portion planned for prototype; model behavior remains real-model evidence required |
| EV-11 | Response-validation tests for malformed schema, extra/missing fields, wrong types, invalid category, oversized/sensitive/markup-like output, timeout, and failure | Planned prototype evidence using controlled mock responses |
| EV-12 | Interface proof of original/draft comparison, correction, `unknown`, escalation and manual fallback; predeclared quality thresholds, sampled reviews, override/omission metrics, training, and workload review | Interface subset planned for prototype; quality and human behavior require a real pilot |
| EV-13 | TP-AI-01 assessment, assurance/remediation evidence, data and training terms, retention/deletion, model/subprocessor inventory, change/incident terms, service levels, and exit test | Provider-evidence-required; unavailable in the fictional case study |
| EV-14 | Size/rate/concurrency boundaries, timeout/retry/idempotency tests, queue/DLQ settings, cost controls, alarms, fallback, and kill-switch result | Selected cases planned for prototype; production/provider evidence also required |
| EV-15 | Monitoring schema, alert tests, protected log access/retention, configuration alerts, incident tabletop, and shutdown/restart responsibilities | Prototype supplies sanitized-event examples only; production/tabletop evidence required |
| EV-16 | Synthetic deletion across primary/S3 versions, provider confirmation, backup expiration, legal-hold handling, exception report, and restore test that reapplies the deletion ledger | Required production/design and provider evidence |
| EV-17 | Knowledge template, prohibited-field/DLP test, publication-role test, human approval, provenance, version/owner/review evidence, and source-deletion test | Required process/design evidence; automatic AI publication remains excluded |
| EV-18 | IAM, database, queue, secret, tool, egress and administrator-path review plus negative test proving Signal cannot reach payment functions | Required design/production evidence |
| EV-19 | TP-PAY-01 licensing/assurance/contract evidence; certificate/signature/timestamp/replay/duplicate/timeout tests; reconciliation, rotation, incident, pause and restart records | Provider-evidence-required plus production integration tests |

## 7. Release-gate register

| Gate | Pass requirement | Automatic failure condition | Risks | Existing launch blockers |
|---|---|---|---|---|
| RG-01 — Tenant isolation | EV-01 and EV-02 pass every approved cross-tenant negative case | Any tenant or assignment bypass succeeds | R-01 | LB-01, LB-05 |
| RG-02 — Identity, privilege, and change integrity | EV-03 and EV-04 show least privilege, separated roles, reviewed changes, protected evidence, and tested rollback | Excessive Signal/admin access, unreviewed change path, exposed secret, or missing rollback | R-02 | LB-05, LB-08, LB-10 |
| RG-03 — AI input protection | EV-05 through EV-09 pass; EV-13 supplies approved external data terms | Prohibited data or field reaches SIM-AI-01/TP-AI-01 or raw values enter ordinary evidence; required check fails open | R-03 | LB-02, LB-06 |
| RG-04 — Output and human oversight | EV-10 through EV-12 meet predeclared validation, quality, correction, escalation, and review thresholds | Invalid/unsafe output bypasses validation, `unknown` fails unsafely, or meaningful human review is not operationally supported | R-04 | LB-04, LB-11 |
| RG-05 — AI-provider readiness | EV-13 is reviewed and approved; relevant EV-11/EV-12/EV-14/EV-15 tests pass | Required provider, model, subprocessor, incident, retention, deletion, change, availability, or exit evidence is missing | R-05 | LB-06, LB-08, LB-11 |
| RG-06 — Reliability and cost | EV-14 demonstrates bounded work, safe failure, manual fallback, alerts, and shutdown | Unbounded retry/concurrency/cost, unsafe duplicate behavior, failed fallback, or ineffective kill switch | R-06 | LB-08 |
| RG-07 — Evidence and lifecycle | EV-09, EV-15 and EV-16 show sanitized durable evidence, verified deletion, controlled exceptions, and safe restoration | Raw sensitive logs, erasable/incomplete evidence, unverified deletion, or deleted data returns after restore | R-07 | LB-09 |
| RG-08 — Reusable knowledge | EV-17 passes before any article is broadly available; automatic publication remains disabled | Signal/ordinary agent self-publishes, customer data remains, or accuracy/ownership/review evidence is absent | R-08 | LB-03 |
| RG-09 — Payment isolation | EV-18 proves Signal lacks payment capability and architecture-drift/change gates are active | Any Signal role, code, credential, tool, queue, database permission, egress, or administrator path can affect payment | R-09 | LB-03, LB-05, LB-07 |
| RG-10 — Payment-provider readiness | EV-19 is approved, incident/pause/restart controls work, and remaining High residual risk is formally accepted or reduced | Provider evidence or integration testing fails, authoritative status is unavailable, or High residual risk lacks executive acceptance | R-10 | LB-07, LB-10 |

## 8. Risk-to-control decision map

| Risk | Safeguards | Evidence | Release gate | Current evidence classification |
|---|---|---|---|---|
| R-01 | SG-01, SG-02, SG-03 | EV-01, EV-02, EV-03 | RG-01 | Design-only / production evidence required |
| R-02 | SG-03, SG-04, SG-08, SG-14 | EV-03, EV-04, EV-09, EV-15 | RG-02 | Prototype supplies limited CI/log examples; production evidence required |
| R-03 | SG-03, SG-05, SG-06, SG-07, SG-08, SG-12, SG-14 | EV-03, EV-05 through EV-09, EV-13, EV-15 | RG-03 | Prototype-tested and AWS-lab-tested portions plus provider/design evidence |
| R-04 | SG-09, SG-10, SG-11, SG-14 | EV-10, EV-11, EV-12, EV-15 | RG-04 | Prototype structure/UI/validation plus real-model and human evidence |
| R-05 | SG-10 through SG-14 | EV-11 through EV-15 | RG-05 | Provider-evidence-required with selected prototype behavior |
| R-06 | SG-13, SG-14 | EV-14, EV-15 | RG-06 | Prototype subset plus production/provider evidence |
| R-07 | SG-08, SG-14, SG-15 | EV-09, EV-15, EV-16 | RG-07 | Prototype logging subset; lifecycle/recovery design and provider evidence required |
| R-08 | SG-04, SG-16 | EV-04, EV-17 | RG-08 | Design/process evidence required; automatic AI publication avoided |
| R-09 | SG-03, SG-04, SG-09, SG-17 | EV-03, EV-04, EV-10, EV-18 | RG-09 | Design-only / negative production evidence required |
| R-10 | SG-14, SG-18 | EV-15, EV-19 | RG-10 | Provider and production integration evidence required |

## 9. Current decision and acceptance boundary

All ten risks remain **Open** because their complete evidence packages do not yet exist. The current simulated recommendation therefore remains **Delay**.

- No Critical projected residual risk may proceed.
- A High projected residual risk requires remediation or explicit written acceptance by the designated LindenArc executive risk owner.
- The analyst recommends treatment but does not accept risk.
- Provider contracts may transfer limited financial or legal obligations; they do not transfer LindenArc's accountability to customers.
- Missing evidence never counts as a passing result or a reason to lower a risk score.

After RG-01 through RG-10 pass, Signal may become eligible for an approve-with-conditions controlled pilot. Broader release requires review of pilot security events, quality results, corrections, overrides, provider behavior, support outcomes, and material changes.

## 10. Immediate prototype requirements derived from risk

The first build must demonstrate the parts of SG-05 through SG-10, SG-13, and SG-14 that are safely testable without a real provider or customer system:

1. fixed reviewed synthetic scenarios only;
2. explicit input-field allow-list and attachment exclusion;
3. Unicode/text normalization before detection;
4. deterministic high-risk detection with documented limits;
5. policy-based masking versus blocking;
6. exact final-JSON reinspection;
7. no SIM-AI-01 invocation after a block or failed required check;
8. HTTP request capture through `MockTransport` at `tp-ai-01.invalid`, with no network fallback;
9. strict response schema/type/size/category/sensitive-data validation and plain-text display;
10. controlled `unknown`, invalid-output, timeout, and provider-failure paths;
11. original-versus-draft comparison, approved playbook or manual state, correction/escalation, and human-review warning;
12. sanitized events that exclude raw detected values, tickets, prompts, and responses;
13. automated tests and a least-privilege GitHub Actions workflow; and
14. a separate bounded AWS Guardrail lab using selected synthetic DATA-17 cases without a foundation-model call.

## 11. Review questions

Before this package is approved, verify:

1. Do the ten risk statements describe the correct business consequences?
2. Are the inherent and projected scores reasonable, including R-01's corrected Critical score and R-10's remaining High target score?
3. Is one accountable fictional role named for every risk?
4. Does each safeguard directly reduce a mapped risk rather than merely sounding secure?
5. Does every evidence item state what it proves and what it cannot prove?
6. Does every release gate contain an objective failure condition?
7. Are the prototype requirements limited to evidence the portfolio can honestly produce?

## 12. Internal source record

- `work/01_scenario_charter.md`
- `work/02_aws_architecture_design_brief.md`
- `work/02b_risk_candidate_log.md`
- `work/02c_third_party_provider_register.md`
- `work/03_data_inventory_and_lifecycle.md`
- `work/04_pasta_threat_model.md`

Framework and service sources remain linked in the architecture, data-lifecycle, and PASTA artifacts. This package does not turn a framework mapping or proposed control into proof of compliance.
