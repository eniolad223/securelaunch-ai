# LindenArc Signal PASTA Threat Model

**Status:** Complete; all seven PASTA stages approved September 9, 2026  
**Method:** Process for Attack Simulation and Threat Analysis (PASTA)  
**Scope:** Simulated security readiness review of LindenArc Signal inside the fictional LindenArc SaaS platform

## How decisions are represented

This case study does not pretend that real LindenArc stakeholders were interviewed. Eniola acts as the security analyst and records reasonable simulated stakeholder inputs as assumptions.

- Fictional business and product leaders define the desired business outcome.
- Data, support, engineering, security, privacy, and third-party owners supply requirements and evidence.
- The security analyst challenges assumptions, models threats, recommends safeguards, and advises whether launch conditions are satisfied.
- A designated executive risk owner—not the analyst or an individual developer—accepts material residual risk and authorizes release.

## PASTA Stage 1 — Define objectives

### 1.1 Business objectives

| ID | Simulated LindenArc objective | How success would be demonstrated |
|---|---|---|
| BO-01 | Reduce the time support agents spend understanding lengthy tickets | Establish a pre-launch baseline and demonstrate a meaningful reduction in median initial-triage time during a controlled pilot; the exact target remains a product decision |
| BO-02 | Help agents locate approved starting steps without allowing AI to invent or execute procedures | Signal returns an approved category or `unknown`; LindenArc retrieves a versioned, human-authored playbook and no step executes automatically |
| BO-03 | Preserve human judgment and customer trust | The original ticket remains authoritative, the AI result is clearly labeled as a draft, and an authorized agent reviews it |
| BO-04 | Keep ordinary customer support available when Signal or its provider fails | Ticket creation, reading, assignment, and manual troubleshooting continue while new Signal calls can be disabled |
| BO-05 | Launch a useful feature without turning LindenArc into a bank, autonomous financial agent, or unrestricted AI platform | Signal remains isolated from payment, tenant administration, account changes, customer messaging, attachments, tools, and autonomous decisions |
| BO-06 | Maintain useful Signal quality over time without silently training on production customer data | Versioned configuration, synthetic evaluation, structured corrections, sampled review, monitoring, rollback, and change gates show whether quality remains acceptable |

### 1.2 Security objectives

| ID | Security objective | Plain-language meaning |
|---|---|---|
| SO-01 | Preserve tenant isolation | One customer and one support assignment cannot expose another tenant's records |
| SO-02 | Minimize external AI disclosure | Only the approved, inspected DATA-06 payload may leave AWS; attachments, secrets, payment data, and unrelated records are excluded |
| SO-03 | Protect identities and privileged capabilities | Strong authentication, trusted tenant context, least privilege, and separate workforce/AWS administration paths are required |
| SO-04 | Treat model output as untrusted | Validate structure and category, reject unsafe output, retrieve only approved playbooks, make source checking practical, and measure whether human oversight actually occurs |
| SO-05 | Isolate Signal from financial action | Signal has no credentials, IAM role, database role, queue permission, tool, or network path capable of initiating or changing a payment |
| SO-06 | Maintain safe failure and recovery | Provider or component failure produces a controlled manual workflow, bounded retries, alerts, reconciliation, backup, and tested restoration—not guessed success |
| SO-07 | Preserve investigation evidence without logging sensitive content | Sanitized events support detection and response while ticket bodies, prompts, credentials, tokens, and banking data stay out of routine logs |
| SO-08 | Control data and provider lifecycles | Retention, deletion verification, restores, AI-provider terms, payment-provider due diligence, and incident coordination must pass their release gates |
| SO-09 | Maintain measurable AI quality and sustainable oversight | Test before release, monitor after release, track corrections and material omissions, reevaluate changes, and address automation bias rather than relying on a review label alone |

### 1.3 Assets and business consequences

| Critical asset or outcome | If confidentiality fails | If integrity fails | If availability fails |
|---|---|---|---|
| Customer and tenant data | Cross-tenant or provider disclosure | Records or tenant context may be altered | Customers and agents cannot access needed cases or records |
| Identities, sessions, secrets, and signing material | Credentials enable impersonation | Attackers may forge trusted requests or events | Revocation or recovery may interrupt service |
| Support tickets, Signal results, and approved playbooks | Customer details or internal guidance leak | Agents receive manipulated, inaccurate, or stale guidance | Agents return to slower manual review |
| Financial workflow and provider references | Sensitive business relationships or references leak | Payment approvals, destinations, amounts, or status may be corrupted | Payments may be delayed or remain uncertain |
| Logs, findings, and recovery evidence | Investigation details expose sensitive context | Attackers erase or falsify evidence | LindenArc cannot investigate or restore confidently |
| Customer trust and LindenArc operations | Privacy and contractual harm | Incorrect decisions or reports damage confidence | Support disruption and payment delays affect customers |

### 1.4 Risk acceptance boundaries

“Not acceptable” does not mean LindenArc claims that risk can become zero. It means the feature does not launch while the known condition remains.

#### Launch-blocking conditions

| ID | Condition that blocks launch |
|---|---|
| LB-01 | Tenant-isolation or object-authorization testing shows that one tenant can access another tenant's data |
| LB-02 | Restricted data, attachments, credentials, access tokens, payment references, or unapproved fields can reach the external AI provider or ordinary logs |
| LB-03 | Signal output can trigger a payment, account change, customer message, support action, or knowledge publication without an authorized human-controlled application decision |
| LB-04 | Model output validation, approved-category enforcement, human-review labeling, or safe `unknown` behavior is missing or can be bypassed |
| LB-05 | The Signal worker has excessive data, IAM, secret, queue, or outbound-network access |
| LB-06 | Required TP-AI-01 model/service provenance, retention, training-use, encryption, location, subprocessor, incident, deletion, change-notice, availability, or exit evidence and terms are missing |
| LB-07 | Critical TP-PAY-01 due diligence is unresolved or the Signal/payment isolation boundary fails |
| LB-08 | The Signal kill switch, failure alerts, dead-letter handling, incident ownership, or manual support fallback has not been tested |
| LB-09 | Required retention, S3-version deletion, backup expiration, restore-deletion replay, or provider-deletion controls cannot be verified |
| LB-10 | A Critical or High residual risk lacks remediation or written acceptance by the designated LindenArc executive risk owner |
| LB-11 | No approved synthetic evaluation, predeclared quality thresholds, usable source-review interface, structured correction process, sampled quality review, change reevaluation, or rollback trigger exists |

#### Conditions LindenArc may tolerate with controls

- Signal may occasionally return `unknown` or an unusable draft because the original ticket remains available for manual work.
- Signal or the AI provider may be temporarily unavailable because core ticket handling remains independent.
- A low-severity finding may remain open when it has an owner, evidence-based rationale, target date, monitoring, and approval at the correct authority level.
- A model classification may be imperfect only within approved and monitored quality thresholds. Lack of autonomous authority limits impact, but it does not replace accuracy testing or sustainable human oversight.

### 1.5 Decision authority

| Decision | Accountable fictional role |
|---|---|
| Define product value and pilot success measurement | Product owner with Support Operations lead |
| Define customer-data use and retention | Customer-data owner with LindenArc privacy/legal and service owners |
| Specify and evaluate safeguards | Security and engineering owners |
| Provide implementation and test evidence | Engineering, Security Operations, Support Operations, and third-party owners |
| Recommend approve, approve with conditions, or delay | Security analyst performing this simulated review |
| Accept material residual risk and authorize launch | Designated LindenArc executive risk owner |

### 1.6 Known assumptions and evidence gaps

- No real LindenArc system, customer, employee, transaction, provider, contract, security report, test result, or usage baseline exists.
- Exact legal and regulatory requirements depend on customer location, data, payment method, contract, and jurisdiction and are not determined by this portfolio case study.
- TP-AI-01 and TP-PAY-01 remain fictional and vendor-neutral; their controls are release requirements to verify, not existing facts. CSP-01 is AWS, but no complete AWS deployment or provider audit is claimed.
- The production architecture remains a design. A narrow LindenArc-controlled security gateway will be prototype-tested, and one Amazon Bedrock Guardrail will be AWS-lab-tested with synthetic data. Neither result proves the complete architecture or a real AI provider.
- The PASTA attack-modeling stage will use safe tabletop scenarios and synthetic evidence rather than exploitation of a live target.
- The initial Signal release uses a pretrained external model for inference only. No production ticket or agent feedback is automatically used for training or fine-tuning.

### Stage 1 outcome

Stage 1 authorizes the simulated analysis to continue; it does **not** authorize product launch. BO-01 through BO-06 explain why Signal matters, SO-01 through SO-09 define what must be protected, and LB-01 through LB-11 provide measurable conditions that later threats, risks, safeguards, and evidence must address.

**Decision status:** Approved by Eniola for continued analysis on September 7, 2026. Later PASTA findings may trace back to or refine an objective, but changes must be recorded rather than made silently.

## PASTA Stage 2 — Define the technical scope

### What this stage does

Stage 1 established why LindenArc wants Signal and which outcomes are unacceptable. Stage 2 now draws the technical boundary around what will be examined. It does not yet identify attackers or simulate attacks; it prevents important connected systems from being overlooked and prevents the project from expanding into a threat model of all LindenArc operations.

### 2.1 Scope rule

A component, person, provider, or data flow is in the primary Signal scope when it can do at least one of the following:

- receive, store, transform, transmit, or display Signal-related data;
- authenticate or authorize access to a Signal ticket or result;
- change Signal's prompts, categories, playbooks, DLP rules, model selection, provider settings, or kill switch;
- provide a credential, network path, log, alert, backup, or recovery capability used by Signal; or
- allow Signal to reach a prohibited financial or administrative capability if isolation fails.

### 2.2 Primary in-scope system

| Scope unit | What is included | Existing traceability |
|---|---|---|
| TS-01 — Ticket intake and access | Customer ticket submission, support-agent authentication, tenant context, object authorization, application API, and original ticket storage | DF-04 through DF-08 and DF-15; TB-03 and TB-05 |
| TS-02 — Signal job creation and retrieval | Transactional outbox, dispatcher, encrypted Signal queue, dead-letter queue, worker, tenant-scoped ticket retrieval, retries, and duplicate-safe processing | DF-15 through DF-18 and DF-24; TB-09 |
| TS-03 — Data minimization and external request | Field allow-list, normalization, deterministic sensitive-data checks, Amazon Bedrock Guardrail, masking/blocking policy, final outbound-payload gate, prompt construction, provider credential, controlled egress, and TP-AI-01 request | DF-19; TB-10, TB-11; RC-01; LAB-DF-01 through LAB-DF-03 |
| TS-04 — AI response and human use | TP-AI-01 response, output inspection and validation, approved-category enforcement, summary storage, playbook lookup, support interface, agent review, correction, and manual-handling path | DF-20 through DF-23; TB-12 and TB-13; RC-02 and RC-05; LAB-DF-04 |
| TS-05 — Configuration and lifecycle control | Versioned prompts, schemas, categories, playbooks, DLP rules, model/service versions, synthetic evaluation, change approval, rollback, and AppConfig kill switch | BO-06, SO-09, LB-08 and LB-11; RC-05 and RC-06 |
| TS-06 — Monitoring, evidence, and recovery | Sanitized application events, provider errors, security findings, alerting, protected audit records, backups, restore tests, and incident actions | DF-14 and DF-34 through DF-38; TB-16 and TB-17; LAB-DF-05 and LAB-DF-06 |
| TS-07 — Payment-isolation boundary | Proof that Signal has no payment IAM role, database role, queue permission, credential, tool, or network route; focused TP-PAY-01 dependency review | SO-05, LB-03 and LB-07; DF-25 through DF-33 and TB-14/TB-15 only as boundary evidence; RC-03 |

### 2.3 People and external organizations in scope

| Actor or provider | Why included |
|---|---|
| Customer user submitting a ticket | Supplies untrusted free-form text and may accidentally or deliberately include sensitive or manipulative content |
| Authorized LindenArc support agent | Views the original ticket, Signal draft, and approved playbook; may correct, overtrust, or misuse the result |
| Support Operations lead | Approves issue categories and human-authored troubleshooting playbooks |
| LindenArc engineering, security, privacy, operations, and administrators | Build, configure, monitor, investigate, recover, and approve changes to Signal and its safeguards |
| CSP-01 — Amazon Web Services | Hosts the simulated architecture and supplies managed security, compute, data, network, logging, and recovery services under shared responsibility |
| TP-AI-01 — External AI Model Service Provider | Receives DATA-06, runs the hosted model, returns DATA-07, and creates security, privacy, model-change, availability, and supply-chain dependencies |
| TP-PAY-01 — Licensed Payment Execution Provider | Included only for focused dependency risk and proof that Signal cannot enter or alter the payment path |

### 2.4 Technology groups in scope

| Technology group | Main services or mechanisms | Why it matters to threats later |
|---|---|---|
| Public entry and identity | Route 53, CloudFront, AWS WAF, Amazon Cognito, API Gateway, HTTPS, short-lived signed access tokens, and multi-factor authentication | A failure may permit impersonation, bypass, abuse, or access to another tenant's ticket |
| Application and data | AWS Lambda, Amazon RDS Proxy, Aurora PostgreSQL, row-level security, parameterized queries, AWS KMS, and private S3 where relevant to excluded attachments | These components enforce tenant access and keep original records separate from the minimized AI payload |
| Asynchronous Signal processing | Transactional outbox, EventBridge, encrypted SQS queue, DLQ, duplicate-safe worker, bounded retries, and AppConfig | Queue manipulation, replay, excessive retrying, or unsafe failure could expose data or disrupt support |
| AI protection and provider connection | Deterministic DLP rules, Amazon Bedrock Guardrails `ApplyGuardrail`, AWS PrivateLink VPC endpoint, Secrets Manager, Network Firewall, NAT Gateway, TLS, and TP-AI-01 API | These controls govern what can leave AWS, where it can go, and how the external dependency is trusted |
| Output and human decision | Structured response schema, plain-text rendering, allowed category list, versioned Aurora playbooks, source comparison, and human review | Untrusted or inaccurate output must not become trusted instructions or autonomous action |
| Security operations and recovery | CloudWatch, CloudTrail, AWS Config, GuardDuty, Security Hub CSPM, EventBridge, SNS, protected S3 logs, AWS Backup, and restore testing | These provide detection, evidence, containment, and recovery but must avoid creating new sensitive-data copies |
| Portfolio prototype and evidence | Python, Streamlit, fixed DATA-17 scenarios, HTTPX `MockTransport`, automated tests, GitHub Actions, and Amazon Bedrock Guardrails `ApplyGuardrail` from AWS CloudShell | These produce narrow, repeatable evidence for the gateway and one Guardrail configuration; they do not represent the complete production stack or a real provider |

### 2.5 Primary trust boundaries

The deepest analysis will focus on five Signal-specific crossings:

1. **TB-09:** the saved ticket becomes asynchronous background work;
2. **TB-10:** raw customer text becomes a minimized, inspected working payload;
3. **TB-11:** approved content crosses from LindenArc's AWS environment to TP-AI-01;
4. **TB-12:** untrusted model output returns to the LindenArc application; and
5. **TB-13:** an AI draft and approved playbook reach the human support agent.

Supporting analysis also includes the customer/workforce identity boundary, application/data boundary, runtime/secret boundary, workload/security-account boundary, workload/log-and-backup boundary, and the one-way isolation requirement between Signal and payment capabilities.

### 2.6 Portfolio validation boundary

The threat model covers the fictional production design, but later evidence is intentionally narrower. Every risk treatment will state which of these labels applies:

| Evidence label | Meaning in this project |
|---|---|
| Design-only | A recommended production safeguard is documented and traced but not deployed. Examples include Cognito, Aurora row-level security, Lambda, PrivateLink, Network Firewall, NAT Gateway, centralized logging, and AWS Backup. |
| Prototype-tested | The integrated Python/Streamlit application and automated tests exercise LindenArc-controlled gateway behavior with fixed synthetic data and SIM-AI-01, a local HTTP mock transport. |
| AWS-lab-tested | A versioned Amazon Bedrock Guardrail is exercised with selected synthetic text through `ApplyGuardrail`. No foundation model is called. |
| Provider-evidence-required | A conclusion depends on a real TP-AI-01 or TP-PAY-01 contract, assurance report, control configuration, or operational test that this case study cannot supply. |

SIM-AI-01 targets the reserved fictional host `tp-ai-01.invalid` and has no live-network fallback. `provider_invoked = true` means only that an HTTP request constructed by the prototype reached the local mock transport. The public Streamlit deployment accepts fixed reviewed scenarios only, not unrestricted text or file uploads.

### 2.7 Explicitly out of scope

- A full threat model of every invoice, expense, vendor, accounting, or reporting feature in the LindenArc platform
- A full assessment of TP-PAY-01's internal infrastructure or regulated operations
- A real AWS deployment, penetration test, provider audit, or contract review
- Deployment of Cognito, Aurora, Lambda, queues, PrivateLink, Network Firewall, NAT Gateway, centralized logging, backups, or a real TP-AI-01 connection
- A live foundation-model call, unrestricted public input or file upload, real customer data, real provider credentials, or AWS credentials in the public application or GitHub Actions
- TP-AI-01 source code, proprietary training datasets, model weights, and internal systems that LindenArc cannot inspect directly; these become evidence and contract requirements instead
- Signal processing of attachments, conversation history, multiple tickets, customer knowledge bases, retrieval-augmented generation, tools, or autonomous actions
- Fine-tuning or training with LindenArc production data
- Exact jurisdiction-specific legal conclusions or any claim of certification or compliance

### 2.8 Stage 2 decision test

The scope is sufficient only if every later threat can be tied to one or more scope units, data flows, boundaries, assets, actors, or providers above. A newly discovered component that can materially change Signal data, behavior, access, evidence, or financial isolation must be added through a recorded scope change.

### Stage 2 working outcome

The primary target is not “all of AWS” or “the AI model alone.” It is the complete LindenArc-controlled Signal workflow plus the external and supporting boundaries that can change its confidentiality, integrity, availability, safety, or financial isolation. The complete architecture is analyzed as a design; the most important AI input/output checkpoint receives prototype evidence and a narrow AWS Guardrail lab. Stage 3 will decompose these scope units into exact processes, data stores, actors, permissions, and trust-boundary crossings before threats are named.

**Decision status:** Approved by Eniola on September 7, 2026. The scope is locked for the initial analysis; a newly discovered material component requires a recorded scope change.

## PASTA Stage 3 — Decompose the application

### What this stage does

Stage 2 drew the boundary around Signal. Stage 3 opens that boundary and identifies the exact actors, components, data stores, permissions, and movements inside it. This creates a reliable map for Stage 4 threat analysis. It does not yet claim that an attack will occur.

### 3.1 Actors

| Actor ID | Actor | Intended authority | Important restriction |
|---|---|---|---|
| ACT-01 | Customer user | Submit a ticket and access records permitted for that user's tenant and role | Cannot choose or override server-controlled tenant context or access another tenant |
| ACT-02 | LindenArc support agent | Access assigned tenant-scoped tickets, compare the original with the Signal draft, correct the draft, and use an approved playbook | Cannot publish reusable knowledge automatically, administer AWS, change Signal controls, or perform a payment through Signal |
| ACT-03 | Support Operations lead | Approve issue categories and versioned troubleshooting playbooks | Cannot silently change security inspection rules or accept material security risk alone |
| ACT-04 | Engineering and Signal administrators | Deploy approved code and configuration changes | Must use separate workforce identity, least privilege, review, logging, and change gates; cannot erase protected evidence |
| ACT-05 | Security, privacy, and incident personnel | Review safeguards, findings, data handling, provider evidence, incidents, and launch gates | Receive only the records required for the assigned role; risk acceptance remains with the executive owner |
| ACT-06 | TP-AI-01 | Process one approved DATA-06 request and return one DATA-07 response | Has no direct VPC, database, attachment, playbook, customer-action, or payment access |
| ACT-07 | TP-PAY-01 | Collect banking details directly, execute approved payments, and return authoritative status | Has no Signal or support-ticket access and supplies no authority to Signal |

### 3.2 Production-reference components

| Component ID | Component or group | Main responsibility | Key data and flows | Portfolio evidence status |
|---|---|---|---|---|
| CMP-01 | Route 53, CloudFront, AWS WAF, and private S3 web origin | Provide the controlled public entrance and static interface | DF-01 through DF-03 | Design-only |
| CMP-02 | Amazon Cognito and protected managed sign-in | Authenticate customer and workforce users and issue limited signed tokens | DATA-01, DATA-11; DF-04 and DF-05 | Design-only |
| CMP-03 | CloudFront/WAF-protected API Gateway | Validate the approved API path and token before application code runs | DF-06 and DF-07 | Design-only |
| CMP-04 | Ticket application Lambda functions | Enforce role, tenant, object, and business authorization; save tickets and serve authorized views | DATA-04; DF-07, DF-08 and DF-15 | Design-only |
| CMP-05 | RDS Proxy and Aurora PostgreSQL | Store tenant-scoped tickets, outbox rows, Signal drafts, review state, categories, and approved playbooks | DATA-04, DATA-07, DATA-08, DATA-14; DF-08, DF-15, DF-16, DF-18 and DF-21/22 | Design-only |
| CMP-06 | Outbox dispatcher and encrypted Signal queue | Move a committed ticket identifier into reliable asynchronous processing without putting the ticket body on the queue | DATA-14; DF-16 and DF-17 | Design-only |
| CMP-07 | Signal worker Lambda | Retrieve one authorized ticket, invoke the inspection chain, construct the provider request, validate the response, and store the safe result | DATA-04, DATA-06, DATA-07; DF-17 through DF-21 | Partially represented by the prototype; Lambda, IAM, queue, and database behavior remain design-only |
| CMP-08 | Deterministic inspection and Amazon Bedrock Guardrail | Normalize, detect, mask or block sensitive content, and fail closed | DATA-06; DF-19; TB-10 | Deterministic portion will be prototype-tested; one Guardrail configuration will be AWS-lab-tested; production integration is design-only |
| CMP-09 | Secrets Manager, Network Firewall, NAT Gateway, PrivateLink, and provider adapter | Protect credentials and restrict outbound destinations to the approved services | DATA-12; DF-19; TB-11 | Local adapter behavior is prototype-tested through SIM-AI-01; production secrets and networking are design-only |
| CMP-10 | TP-AI-01 external model service | Perform hosted inference and return structured untrusted output | DATA-06 and DATA-07; DF-19/20 | Provider-evidence-required; SIM-AI-01 is only a local test double |
| CMP-11 | Output validator, category validator, and playbook lookup | Reject malformed or unsafe output and retrieve only a versioned human-authored playbook for an allowed category | DATA-07 and DATA-08; DF-20 through DF-22; TB-12 | Prototype-tested for selected synthetic responses; production database integration is design-only |
| CMP-12 | Support interface and manual workflow | Show the original ticket, labeled draft, approved starting steps, correction state, and manual fallback | DF-23; TB-13 | Prototype-tested with fixed synthetic scenarios; authentication and production workflow remain design-only |
| CMP-13 | AppConfig, versioned configuration, and Signal kill switch | Control approved prompts, schemas, rules, categories, model version, rollout, rollback, and emergency disablement | DATA-08, DATA-17, DATA-18 | Design-only except for versioned local configuration and tested fallback behavior |
| CMP-14 | CloudWatch, CloudTrail, AWS Config, GuardDuty, Security Hub CSPM, EventBridge, SNS, and protected log archive | Produce sanitized monitoring, findings, alerts, and durable investigation evidence | DATA-13; DF-14 and DF-34 through DF-37 | Design-only; sanitized prototype events and CI results are prototype-tested |
| CMP-15 | AWS Backup locked vault and isolated restore test | Preserve and verify recoverability without silently restoring previously deleted records | DATA-15; DF-38 | Design-only |
| CMP-16 | Payment services and TP-PAY-01 boundary | Execute the separate financial workflow while proving Signal has no route or permission to it | DATA-09 and DATA-10; DF-25 through DF-33; TB-14/TB-15 | Focused design and provider-evidence-required review only |

### 3.3 Data stores and durable state

| Store ID | Store | What belongs there | What must not be placed there |
|---|---|---|---|
| DS-01 | Cognito identity store | User identity, tenant membership, role, MFA and account state | Support tickets, banking data, provider prompts, or model responses |
| DS-02 | Aurora PostgreSQL | Original tickets, tenant-scoped business records, outbox rows, validated Signal drafts, review state, categories, and playbooks | Raw banking credentials or unvalidated external output treated as trusted guidance |
| DS-03 | Private S3 document and attachment buckets | Approved invoices, receipts, and support attachments under separate tenant and malware controls | Attachments in DATA-06 or direct public objects |
| DS-04 | Signal queue and dead-letter queue | Job, ticket and tenant identifiers, retry count, and sanitized failure category | Ticket bodies, attachments, credentials, prompts, responses, or payment details |
| DS-05 | Secrets Manager, KMS, and trust material | Provider credentials, database credentials, encryption and signing material | Secrets in application code, fixtures, logs, screenshots, or GitHub Actions |
| DS-06 | Monitoring and protected log archive | Sanitized actor, request, rule, action, timing, finding, and investigation metadata | Raw ticket text, detected values, credentials, full prompts, raw model responses, or banking details |
| DS-07 | Backup vault and restore environment | Encrypted recovery points and restore-test evidence | Indefinite copies that bypass retention, legal-hold, or deletion-ledger rules |
| DS-08 | TP-AI-01 processing boundary | The approved DATA-06 request and generated DATA-07 response for bounded processing | Original tickets, attachments, other tenants, payment data, AWS credentials, tools, or durable training data |

### 3.4 Minimum permissions

| Principal | Minimum required access | Explicitly prohibited access |
|---|---|---|
| Ticket application function | Validate the caller and read/write the authorized tenant's ticket and outbox records | Choosing tenant identity from an untrusted request, unrestricted table access, or provider/payment credentials |
| Outbox dispatcher | Read committed unsent outbox identifiers, send identifier-only jobs, and update dispatch state | Reading ticket bodies or invoking TP-AI-01 |
| Signal worker | Consume one Signal job, retrieve one tenant-scoped ticket, inspect DATA-06, call approved Guardrail/provider destinations, and store one validated result | S3 attachments, other tickets, tenant administration, customer messaging, knowledge publication, or any payment capability |
| Support agent | Read assigned tickets, drafts, and approved playbooks; submit corrections | AWS administration, DLP or model configuration changes, cross-tenant browsing, or automatic execution of suggestions |
| Signal/configuration administrator | Change only the specifically assigned configuration through reviewed deployment paths | Unreviewed production changes, executive risk acceptance, or deletion of protected evidence |
| TP-AI-01 | Receive the approved request through its authenticated API and return a response | Initiating connections into LindenArc or accessing any other LindenArc store or action |

### 3.5 Normal Signal sequence

1. CMP-04 writes the original ticket and outbox job to DS-02 in one tenant-scoped transaction (`DF-15`).
2. CMP-06 sends only identifiers and retry metadata to DS-04 (`DF-16/17`).
3. CMP-07 retrieves that one ticket through tenant-scoped database access (`DF-18`).
4. CMP-08 allow-lists fields, normalizes text, performs deterministic and Guardrail inspection, and masks or blocks according to policy.
5. CMP-07 builds the final JSON and CMP-08 inspects that exact serialized payload again.
6. If either inspection fails or is unavailable, Signal stops and ordinary manual support continues; TP-AI-01 is not called.
7. If the payload passes, CMP-09 sends DATA-06 to CMP-10 through the approved external path (`DF-19`).
8. CMP-11 treats the returned DATA-07 response as untrusted, validates it, and rejects unsafe or invalid output (`DF-20`).
9. CMP-07 stores the validated draft, and CMP-11 retrieves an approved playbook only for an allowed category (`DF-21/22`).
10. CMP-12 shows the original ticket, labeled draft, approved starting steps or manual state, and correction controls to ACT-02 (`DF-23`). Failed background jobs follow the bounded retry and dead-letter path (`DF-24`).

### 3.6 Attack surfaces carried into Stage 4

These are reachable or changeable surfaces, not yet final threats:

- free-form customer ticket text and API parameters;
- access tokens, tenant claims, record identifiers, and object keys;
- queue messages, retries, duplicate jobs, and dead-letter handling;
- DLP rules, prompts, schemas, category lists, playbooks, provider settings, and the kill switch;
- provider credentials and permitted outbound destinations;
- the TP-AI-01 request and untrusted response;
- the support interface and the agent's human-review behavior;
- logs, alerts, security findings, backups, deletion records, and restore procedures; and
- the isolation boundary between Signal and payment capabilities.

### 3.7 Stage 3 completeness test

Stage 3 is sufficient if every important Signal movement in DF-15 through DF-24 has a source, destination, data type, responsible component, required permission, trust boundary, and safe-failure path. Supporting identity, data, monitoring, recovery, and payment-isolation components remain connected through their existing DF, DATA, TB, BO, SO, LB, and RC identifiers.

### Stage 3 working outcome

The decomposition identifies seven actors, sixteen component groups, eight stores, six minimum-permission profiles, the ten-step Signal sequence, and the main attack surfaces. It preserves the distinction between the fictional production design, the working security-gateway prototype, the limited Guardrail lab, and evidence that only a real provider could supply. Stage 4 can now identify threats against specific components and flows instead of producing a generic AI-risk list.

**Decision status:** Approved by Eniola on September 8, 2026. Changes to an actor, component, store, permission, or normal flow must be recorded before later threat conclusions rely on them.

## PASTA Stage 4 — Analyze threats

### What this stage does

Stage 4 asks what harmful event could affect the system, who or what could cause it, which component or trust boundary it would target, and what security property could be lost. A threat is not yet proof of a weakness, a successful attack, or an unacceptable risk. Stage 5 will examine the weaknesses that could make these events possible, Stage 6 will build realistic attack paths, and Stage 7 will score and prioritize the resulting risks.

### 4.1 Threat-source groups

| Source ID | Threat source | Intent or condition |
|---|---|---|
| TA-01 | External attacker or automated bot | Steal access, expose data, disrupt service, increase cost, or hide activity |
| TA-02 | Malicious or curious customer user | Manipulate identifiers or ticket content to access another tenant, influence Signal, or abuse processing |
| TA-03 | Compromised customer or support identity | Use a stolen session or token with the victim's apparent authority |
| TA-04 | Malicious, compromised, or mistaken privileged insider | Change rules, permissions, providers, playbooks, logging, or evidence outside the approved process |
| TA-05 | Compromised dependency, build workflow, or deployment artifact | Introduce unsafe code, exfiltrate secrets, or alter the security gateway and its evidence |
| TA-06 | Compromised, unsafe, unavailable, or materially changed TP-AI-01 or subprocessor | Expose or misuse data, return unsafe output, change behavior, or stop service |
| TA-07 | Compromised or unavailable TP-PAY-01 ecosystem | Expose banking data, forge status, disrupt payment processing, or damage customers through the dependency |
| TA-08 | Accidental user action, software defect, configuration error, or service failure | Cause disclosure, incorrect output, lost evidence, unsafe retrying, incomplete deletion, or outage without malicious intent |

### 4.2 Threat inventory

| Threat ID | Threat event | Likely sources | Primary targets and paths | Potential consequence | Coverage anchors |
|---|---|---|---|---|---|
| T-01 | A caller accesses or changes another tenant's ticket, Signal result, document, or related record by manipulating an identifier or tenant context | TA-01, TA-02, TA-03 | CMP-03 through CMP-05 and CMP-12; DS-02/03; DF-06 through DF-13 and DF-21 through DF-23 | Cross-tenant disclosure, alteration, loss of trust, and contractual or privacy harm | STRIDE information disclosure/elevation of privilege; OWASP API1/API3; SO-01; LB-01 |
| T-02 | An attacker impersonates a customer, support agent, administrator, worker, or service and uses the stolen authority to access data or change Signal | TA-01, TA-03, TA-04, TA-05 | CMP-02 through CMP-04, CMP-07, CMP-09 and CMP-13/14; DS-01/05/06; DF-04 through DF-08 and DF-34 through DF-37 | Unauthorized access, control changes, secret theft, evidence tampering, or wider privilege escalation | STRIDE spoofing/elevation of privilege; OWASP API2/API5; SO-03; LB-05 |
| T-03 | Restricted or unnecessary information reaches TP-AI-01, routine logs, test evidence, or another unapproved destination | TA-02, TA-04, TA-05, TA-06, TA-08 | CMP-07 through CMP-10 and CMP-14; DS-02, DS-06 and DS-08; DF-18 through DF-20, DF-24 and DF-34; TB-10/TB-11 | External disclosure, secondary use, retention violations, incident response, and customer harm | STRIDE information disclosure; OWASP LLM02/API3/API10; RC-01; LB-02 |
| T-04 | Malicious or misleading ticket text manipulates the model into ignoring instructions, omitting facts, exposing prompt material, or selecting an unsafe category | TA-02, TA-03 | CMP-07, CMP-10 through CMP-12; DF-18 through DF-23; TB-10 through TB-13 | Misleading summary, wrong approved playbook, unsafe support handling, or reduced trust | STRIDE tampering; OWASP LLM01/LLM07/LLM09; RC-02 and RC-05; SO-04 |
| T-05 | Malformed, manipulated, sensitive, oversized, or unsupported provider output is treated as trusted data or executable presentation content | TA-05, TA-06, TA-08 | CMP-10 through CMP-12; DS-02/06; DF-20 through DF-23; TB-12/TB-13 | Stored unsafe content, interface injection, sensitive-data propagation, incorrect guidance, or application failure | STRIDE tampering/information disclosure/denial of service; OWASP LLM05/LLM09 and API10; RC-02; LB-04 |
| T-06 | An unauthorized or unreviewed change weakens DLP rules, prompts, schemas, categories, playbooks, dependencies, destination restrictions, monitoring, rollback, or the kill switch | TA-04, TA-05, TA-08 | CMP-08, CMP-09, CMP-11 and CMP-13/14; DS-05/06; configuration and deployment paths | A previously blocked payload passes, unsafe guidance appears approved, traffic reaches the wrong destination, or detection and rollback fail | STRIDE tampering/repudiation/elevation of privilege; OWASP LLM03/API8/API9; RC-04 and RC-05; LB-05/LB-08/LB-11 |
| T-07 | TP-AI-01 or its supply chain retains, exposes, reuses, corrupts, or materially changes the handling of LindenArc requests and responses | TA-06 | CMP-09/10; DS-08; DF-19/20; TB-11/TB-12 | Confidentiality loss, cross-customer exposure, quality regression, inability to delete or investigate, or forced provider exit | STRIDE information disclosure/tampering/denial of service; OWASP LLM02/LLM03/LLM09 and API10; RC-06; LB-06 |
| T-08 | Automated traffic, repeated Signal jobs, poison messages, retry storms, oversized inputs, provider limits, or outages exhaust processing capacity or create unexpected cost | TA-01, TA-02, TA-06, TA-08 | CMP-01, CMP-03, CMP-06 through CMP-10 and CMP-13/14; DS-04; DF-02, DF-06 and DF-15 through DF-24; TB-09/TB-11 | Delayed support, queue growth, cost escalation, repeated processing, or Signal outage | STRIDE denial of service; OWASP LLM10/API4/API6; RC-06; SO-06; LB-08 |
| T-09 | Logs, findings, deletion evidence, or backups expose sensitive data, are erased or altered, fail to capture material activity, or restore information that should remain deleted | TA-04, TA-05, TA-08 | CMP-14/15; DS-06/07; DF-14, DF-24 and DF-34 through DF-38; TB-16/TB-17 | Inability to investigate or prove deletion, hidden attacker activity, sensitive log disclosure, failed recovery, or data reappearance | STRIDE repudiation/tampering/information disclosure/denial of service; SO-07/SO-08; LB-09 |
| T-10 | Signal or a compromised Signal identity gains a credential, permission, tool, queue path, database role, or network route capable of initiating or changing a payment | TA-01, TA-03, TA-04, TA-05, TA-08 | CMP-07, CMP-09, CMP-13 and CMP-16; DATA-09; Signal/payment isolation boundary | Unauthorized or manipulated financial action caused by excessive Signal authority | STRIDE tampering/elevation of privilege; OWASP LLM06/API5; SO-05; LB-03 |
| T-11 | TP-PAY-01 or its integration is compromised, unavailable, replayed, or inconsistent and supplies exposed, fraudulent, delayed, or conflicting payment information | TA-01, TA-04, TA-05, TA-07, TA-08 | CMP-16; DATA-09/10; DF-25 through DF-33; TB-14/TB-15 | Exposed banking information and unauthorized, duplicated, delayed, misdirected, or incorrectly reported payments | STRIDE spoofing/tampering/information disclosure/denial of service; OWASP API10; RC-03; LB-07 |

### 4.3 How a third-party compromise reaches LindenArc

A provider compromise does not automatically give an attacker access to LindenArc's AWS account, VPC, Aurora database, or Signal. Harm can still cross a properly separated boundary in four ways: information the provider already holds is exposed; LindenArc accepts a trusted but false provider response; an integration credential or signing key is abused; or the provider becomes unavailable and LindenArc cannot complete or verify an important service.

| Compromised dependency | Direct effect outside LindenArc | How harm can cross into LindenArc | Specific effect on Signal | Important limit in the design |
|---|---|---|---|---|
| TP-AI-01 or its subprocessor | DATA-06 may be exposed, retained, reused, altered, or processed by an unsafe or changed model; the service may also fail | The legitimate provider endpoint can return malicious, misleading, sensitive, malformed, or changed output using otherwise valid TLS and credentials; outage, rate limiting, and cost also cross through the dependency | Signal may produce no result, a false summary, or the wrong category and playbook. Even minimized DATA-06 remains Confidential and detection can miss context-dependent information | TP-AI-01 has no inbound VPC, database, attachment, tool, customer-action, or payment access. Output validation, approved playbooks, human review, provider monitoring, manual fallback, and the kill switch limit—but do not eliminate—the harm |
| TP-PAY-01 or its subprocessor | Banking details held by the provider may be exposed; payments, onboarding, or authoritative status may be manipulated or unavailable | Stolen provider signing material can make a fraudulent webhook appear authentic; false or missing status can corrupt LindenArc's payment records; provider outage creates unknown transactions and reconciliation failures; customers still associate the incident with LindenArc | Signal should not be technically compromised because it has no payment credential, queue, database role, tool, or provider route. Indirectly, support volume can surge and agents may receive tickets describing false or uncertain payment states. Payment-related cases may therefore require incident-mode manual handling rather than ordinary Signal guidance | A dedicated payment API path, mutual TLS, message signatures, timestamps, replay protection, idempotency, reconciliation, anomaly alerts, dispatch kill switch, and provider incident terms reduce the harm. They cannot prevent a breach inside TP-PAY-01 or erase LindenArc's responsibility to customers |

Provider-side security claims therefore remain **provider-evidence-required**. The portfolio can design and tabletop-test LindenArc's response to a compromised provider, but a local mock transport or AWS Guardrail lab cannot prove that either fictional provider is secure.

### 4.4 Trust-boundary coverage check

| Boundary | Threats carried forward | Why the coverage is sufficient for Stage 4 |
|---|---|---|
| Customer and workforce identity boundaries | T-01, T-02 and T-08 | Covers object access, impersonation, privilege misuse, and automated abuse |
| TB-09 — saved ticket to background job | T-06 and T-08 | Covers queue/configuration tampering, duplicate work, poison messages, retries, and loss of availability |
| TB-10 — original to minimized data | T-03 and T-04 | Covers sensitive-data escape and manipulative content before the external request |
| TB-11 — LindenArc to TP-AI-01 | T-03, T-07 and T-08 | Covers disclosure, provider dependency, destination trust, availability, and cost |
| TB-12 — TP-AI-01 response to application | T-05 and T-07 | Covers unsafe output and provider-controlled behavior entering LindenArc |
| TB-13 — Signal result to support agent | T-04 and T-05 | Covers misinformation, unsafe presentation, and human reliance on an untrusted draft |
| TB-14/TB-15 — payment provider and Signal/payment isolation | T-10 and T-11 | Separates prohibited Signal agency from provider-originated payment harm |
| TB-16/TB-17 — security evidence and recovery | T-06 and T-09 | Covers control tampering, evidence loss, disclosure, deletion failure, and unsafe recovery |

### 4.5 Relevant and excluded framework categories

STRIDE is used as a completeness check: spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege are all represented. STRIDE does not score risk and does not replace the business impact analysis in Stage 7.

The current OWASP lists are also coverage aids, not automatic findings. Relevant AI categories include prompt injection, sensitive-information disclosure, supply-chain risk, improper output handling, excessive agency, system-prompt leakage, misinformation, and unbounded consumption. Relevant API categories include object- and property-level authorization, authentication, function-level authorization, resource consumption, security misconfiguration, inventory management, and unsafe consumption of external APIs.

The following categories are intentionally not modeled as primary initial-release paths:

- vector and embedding weaknesses, because Signal uses no retrieval-augmented generation or vector database;
- LindenArc training-data or model poisoning, because LindenArc does not train or fine-tune the model with production data; provider model provenance remains inside T-07;
- attachment-based model attacks, because attachments never enter DATA-06; ordinary attachment malware remains part of the wider platform reference design; and
- autonomous tool chaining, because Signal has no tools or action permissions. Failure of that isolation is still covered by T-10.

### 4.6 Stage 4 completeness test

The inventory passes Stage 4 only if every primary Signal trust boundary has at least one credible confidentiality, integrity, or availability threat; every STRIDE category is represented; relevant OWASP AI and API categories are either mapped or explicitly excluded; and every threat points to named components, flows, sources, consequences, and existing project objectives or risk candidates.

### Stage 4 working outcome

The analysis identifies eleven focused threat groups rather than treating every framework entry as a separate finding. They cover tenant isolation, identity, sensitive-data disclosure, prompt injection, unsafe output, control and supply-chain tampering, AI-provider dependency, resource exhaustion, evidence and recovery failure, Signal/payment isolation, and payment-provider dependency. Stage 5 will now examine the specific weaknesses and preconditions that could allow each threat to succeed.

**Decision status:** Approved by Eniola on September 8, 2026 after adding the explicit third-party-compromise propagation analysis. The addition records how provider-held data, trusted API responses, integration credentials, and operational dependence can harm LindenArc without implying automatic access to LindenArc's AWS environment.

## PASTA Stage 5 — Analyze candidate weaknesses

### What this stage does

Stage 4 identified what could go wrong. Stage 5 asks what weakness, unsafe assumption, missing safeguard, or unverified dependency could allow each threat to succeed.

Because LindenArc is fictional, this case study cannot honestly claim that the reference architecture contains confirmed exploitable vulnerabilities. Each item below is therefore one of three things:

- a **candidate implementation weakness** that a real build must prevent and test;
- a **process or human-factor weakness** that requires operational evidence; or
- an **evidence gap** that blocks confidence until a real provider or system owner supplies proof.

### 5.1 Candidate weakness inventory

| Weakness ID | Candidate weakness or precondition | Type | Enables threats | Why it is plausible | Evidence needed to close or confirm it |
|---|---|---|---|---|---|
| W-01 | An API or database operation trusts a client-supplied tenant, ticket, document, or result identifier without independently verifying the caller's access to that exact object | Implementation | T-01 | Authentication can be valid while object authorization is still missing; pooled SaaS records share infrastructure | Negative cross-tenant tests at the API and database layers, including changed identifiers and row-level-security tests; design-only until a real application exists |
| W-02 | Customer, support, or administrator access is excessive, stale, shared, or insufficiently separated | Design, configuration, and process | T-01, T-02 and T-06 | Support work, administration, incident response, and risk acceptance require different authority; convenience can create broad roles | Role matrix, joiner/mover/leaver evidence, multifactor-authentication and session configuration, privileged-access review, separation-of-duties test, and access-review records |
| W-03 | Tokens, service credentials, signing material, or worker permissions are long-lived, exposed, reusable, or broader than one required task | Implementation and configuration | T-02, T-03 and T-10 | A stolen identity or overprivileged worker can turn one compromise into data disclosure or financial reach | IAM and database-role policy review, secret scan, credential-rotation evidence, token tests, and explicit denial of attachment, administration, customer-action, and payment permissions |
| W-04 | Field allow-listing, text normalization, deterministic detection, or contextual Guardrail rules are incomplete, inconsistent, bypassable, or unavailable | Implementation and configuration | T-03 and T-04 | Free-form text can contain unexpected encodings, disguised identifiers, unsupported languages, context-dependent confidential information, or customer mistakes | Prototype and AWS-lab cases for approved, masked, blocked, obfuscated, ambiguous, unsupported, and detector-failure conditions; documented false-positive and false-negative limits |
| W-05 | The application checks an intermediate text value but fails to inspect the exact final serialized request, excludes the wrong fields, or records raw detected values in logs and evidence | Implementation | T-03 | Sensitive data can be reintroduced during payload construction, error handling, debugging, or telemetry even when an earlier scan passed | Prototype proof that unapproved fields and attachments never enter DATA-06, a reintroduced value is blocked at the final gate, blocked cases never reach SIM-AI-01, and logs contain only sanitized rule and outcome metadata |
| W-06 | Ticket content is not strongly separated from system instructions, or prompts contain secrets or treat customer text as trusted commands | Design and implementation | T-04 | The model processes instructions and untrusted ticket prose together; prompt wording alone cannot create a security boundary | Prompt-template and delimiter review, proof that prompts contain no credentials, confirmation that the model has no tools or action permissions, and direct/indirect prompt-injection evaluation against the selected real model before production use; the local mock cannot measure model resistance |
| W-07 | Provider output lacks strict schema, type, size, category, sensitive-data, and safe-rendering validation before storage or display | Implementation | T-05 | A valid HTTPS response can still be malformed, malicious, sensitive, misleading, or unsafe to render | Prototype tests for malformed JSON, missing or extra fields, wrong types, invalid category, oversized output, markup or script-like text, sensitive-looking content, timeout, and safe manual fallback |
| W-08 | Human review becomes a routine confirmation, the original evidence is hard to compare, corrections are not captured, or quality thresholds and rollback triggers are undefined | Human factor and process | T-04 and T-05 | Busy support agents may gradually trust a usually-correct draft without meaningful verification | Usability evidence, visible source comparison, correction workflow, predeclared quality thresholds, sampled review, workload analysis, agent training, override metrics, rollback and kill-switch exercises; not provable by the prototype alone |
| W-09 | Prompts, rules, categories, playbooks, model or provider versions, dependencies, deployment workflows, or the kill switch can change without provenance, review, testing, approval, or rollback | Design, supply chain, and process | T-02, T-05 and T-06 | An administrator mistake or compromised dependency can silently weaken several safeguards at once | Version inventory, protected branch and review settings, dependency and secret scanning, pinned dependencies and actions, change approval, regression tests, deployment evidence, rollback test, and protected configuration audit trail |
| W-10 | A support resolution or playbook can be published, retained, or broadly reused without de-identification, technical validation, owner approval, versioning, or retirement | Process and data governance | T-06 and T-09 | Useful troubleshooting knowledge can accidentally preserve customer data, malicious ticket content, or obsolete instructions | Structured knowledge template, prohibited-field rules, DLP test, designated human approval, publication-role test, source-deletion test, version history, owner and annual-review evidence; AI closure drafting remains out of the initial release |
| W-11 | TP-AI-01's data use, retention, training prohibition, deletion, tenant isolation, model provenance, subprocessors, change notice, security controls, incident response, availability, or exit terms are unknown or inadequate | Third-party evidence gap | T-03, T-05, T-07 and T-08 | LindenArc cannot inspect the hosted model or assume that an API agreement provides every required security property | Completed provider assessment, relevant independent assurance and remediation evidence, signed security and privacy terms, model and subprocessor inventory, synthetic evaluation, change notice, incident exercise, service levels, deletion evidence, and exit test |
| W-12 | Input size, rate, concurrency, timeout, retry, queue-retention, duplicate-processing, provider-spend, or kill-switch limits are absent or ineffective | Design, implementation, and operations | T-08 | A simple request, poison message, outage, or retry loop can multiply cloud work and provider cost | Boundary and load tests, maximum-size tests, per-tenant rate limits, bounded exponential retry, idempotency tests, queue and dead-letter-queue configuration, cost alerts or caps, manual fallback, and kill-switch test |
| W-13 | Security events are incomplete, overly sensitive, alterable by workload administrators, poorly correlated, unavailable to responders, or not connected to actionable alerts | Design and operations | T-02, T-03, T-06 and T-09 | Logging can either leak the protected data or fail to explain what happened; the same administrator should not be able to create and erase the evidence | Logging schema and prohibited-field tests, alert tests, clock and identifier correlation, least-privilege access, centralized protected retention, investigation exercise, and evidence that production administrators cannot silently delete protected records |
| W-14 | Retention, S3 version expiration, provider deletion, backup aging, deletion-ledger replay, legal holds, or restore validation are incomplete or untested | Data governance and operations | T-09 | Deleting a live record does not remove older object versions, provider copies, or recovery points; restoration can resurrect properly deleted data | Aurora and S3 synthetic deletion tests, noncurrent-version lifecycle evidence, backup expiration, provider confirmation, legal-hold procedure, exception tracking, restore test, and proof that the identifier-only deletion ledger is reapplied |
| W-15 | Signal shares a role, credential, database permission, queue, tool, network destination, or administrator path with the payment workflow | Architecture and configuration | T-10 | A convenient shared service or future feature expansion could convert an advisory AI function into a financially capable one | Architecture and policy review proving explicit denial or absence across IAM, database, queues, secrets, tools, and egress; negative integration test and change gate for any future action capability |
| W-16 | TP-PAY-01 due diligence, licensing, credential protection, webhook authentication, replay controls, immutable approvals, idempotency, reconciliation, anomaly detection, incident coordination, dispatch pause, or restart approval is missing or ineffective | Third-party, implementation, and operations | T-11 | A valid-looking provider message can be false if signing material is stolen, and a provider outage or compromise can leave payment state uncertain | Licensing and assurance evidence, provider assessment, contract terms, certificate, signature, timestamp and replay tests, duplicate and timeout tests, reconciliation records, key rotation, incident tabletop, kill-switch test, and controlled pause and restart evidence |

### 5.2 Threat-to-weakness traceability

| Threat | Candidate weaknesses carried forward |
|---|---|
| T-01 — Cross-tenant access | W-01, W-02 and W-03 |
| T-02 — Identity or privilege compromise | W-02, W-03, W-09 and W-13 |
| T-03 — Sensitive-data disclosure | W-03, W-04, W-05, W-11 and W-13 |
| T-04 — Prompt injection and misleading input | W-04, W-06 and W-08 |
| T-05 — Unsafe provider output | W-07, W-08, W-09 and W-11 |
| T-06 — Security-control tampering | W-02, W-09, W-10 and W-13 |
| T-07 — AI-provider or supply-chain failure | W-11 |
| T-08 — Resource exhaustion and unexpected cost | W-11 and W-12 |
| T-09 — Evidence, deletion, or recovery failure | W-10, W-13 and W-14 |
| T-10 — Signal reaches payment capabilities | W-03 and W-15 |
| T-11 — Payment-provider or integration compromise | W-16 |

### 5.3 What this portfolio can actually verify

| Evidence route | Weaknesses addressed | Honest limitation |
|---|---|---|
| Python and Streamlit prototype plus automated tests | The deterministic portion of W-04, W-05, structural containment in W-06, W-07, and selected safe-failure and logging parts of W-12/W-13 | Proves only the implemented logic and named synthetic cases. It can show instruction/data separation, no tools, and safe handling of a controlled mock response, but cannot measure a real model's prompt-injection resistance |
| Amazon Bedrock Guardrails lab | A narrow portion of W-04 | Proves only the recorded Guardrail version, configuration, Region, date, and synthetic cases; it does not prove the full gateway or AI provider |
| Design and test requirements | W-01 through W-03, W-08 through W-10, and W-12 through W-15 | Shows that the control and evidence are understood; does not prove they operate in a real LindenArc environment |
| Real-model evaluation plus provider evidence and contractual verification | Model-behavior portions of W-06/W-08 plus W-11 and W-16 | Cannot be completed against fictional TP-AI-01 or TP-PAY-01; these remain model- or provider-evidence-required launch conditions |

### 5.4 Deliberate limits

- No Common Vulnerabilities and Exposures (CVE) identifier is assigned because no real LindenArc software inventory or vulnerable deployed version exists.
- A missing fictional artifact is recorded as an evidence gap, not proof that a provider lacks the underlying control.
- Existing proposed safeguards do not automatically close a weakness; implementation and operating evidence are still required.
- The local mock transport tests LindenArc-controlled behavior and supplies no assurance about TP-AI-01.
- The later risk register will prioritize approximately eight to ten material risks; it does not need a separate risk row for every candidate weakness.

### 5.5 Stage 5 completeness test

Stage 5 passes only if every T-01 through T-11 threat maps to at least one explicit weakness or evidence gap, every candidate has a named verification route, prototype-testable items are separated from design-only and provider-dependent claims, and no untested fictional weakness is presented as a confirmed vulnerability.

### Stage 5 working outcome

The analysis identifies sixteen candidate weaknesses across authorization, identity, data minimization, prompt handling, output validation, human oversight, configuration and supply chain, knowledge governance, provider assurance, availability and cost, evidence and recovery, and payment isolation. Five core gateway areas can receive hands-on prototype evidence, one selected managed safeguard can receive narrow AWS-lab evidence, and the remaining conditions require design or provider evidence. Stage 6 can now combine related threats and weaknesses into realistic end-to-end attack scenarios.

**Decision status:** Approved by Eniola on September 9, 2026. The approved version preserves the distinction between a candidate weakness and a confirmed vulnerability, and it does not treat the local mock transport as evidence of real-model prompt-injection resistance or provider security.

## PASTA Stage 6 — Model attack and failure scenarios

### What this stage does

Stage 6 combines a threat source, reachable component, candidate weakness, trust-boundary crossing, and business consequence into a realistic chain. These are safe tabletop scenarios using the fictional design and synthetic data. They are not instructions to attack a live service and are not claims that exploitation occurred.

Each scenario follows the same structure:

`Starting condition → weakness used → boundary crossed → harmful result → control or evidence that should break the chain`

### 6.1 Scenario inventory

| Scenario ID | Scenario | Threats and weaknesses | Evidence route |
|---|---|---|---|
| AS-01 | Cross-tenant ticket identifier manipulation | T-01/T-02; W-01/W-02/W-03 | Design and negative authorization tests required |
| AS-02 | Sensitive-data evasion and external disclosure | T-03/T-04; W-04/W-05 | Prototype-tested plus narrow AWS Guardrail lab; provider terms still required |
| AS-03 | Prompt injection produces believable but misleading support guidance | T-04/T-05; W-06/W-07/W-08 | Structural prototype tests plus real-model and human-oversight evidence required |
| AS-04 | Compromised AI provider returns trusted-looking malicious output | T-03/T-05/T-07; W-07/W-08/W-11 | Provider-evidence-required with LindenArc output/fallback design tests |
| AS-05 | Privileged identity or software-supply-chain change weakens safeguards | T-02/T-03/T-06; W-02/W-03/W-09/W-13 | Design, repository, deployment, access, audit, and rollback evidence required |
| AS-06 | Automated use and retry amplification cause outage or excessive cost | T-08; W-11/W-12 | Prototype boundary tests plus design and provider operational evidence |
| AS-07 | Sensitive or incomplete logging creates exposure and an investigation blind spot | T-03/T-06/T-09; W-05/W-13 | Prototype log tests plus production monitoring and access evidence required |
| AS-08 | Deletion appears complete but backup restoration revives the record | T-09; W-14 | Design-only deletion and restore test requirement |
| AS-09 | A future change gives Signal a path to payment capability | T-02/T-06/T-10; W-03/W-09/W-15 | Design, explicit-denial, negative integration, and change-gate evidence required |
| AS-10 | Compromised payment-provider signing material produces a false status event | T-11; W-16 | Provider and production integration evidence required |
| AS-11 | Customer-derived content becomes unsafe reusable support knowledge | T-06/T-09; W-10 | Governance, DLP, publication-role, review, and retention evidence required |

### 6.2 AS-01 — Cross-tenant ticket identifier manipulation

**Starting condition:** TA-02 has a valid customer account or TA-03 controls a valid customer or support session.

**Attack chain:**

1. The caller observes or guesses another ticket, result, or document identifier.
2. The caller substitutes that identifier in an otherwise valid API request.
3. CMP-03 validates the token, but CMP-04 trusts the submitted object identifier without checking access to that exact object.
4. DS-02 lacks effective row-level enforcement or receives unsafe tenant context.
5. Another tenant's DATA-04 or DATA-07 record is returned or altered.

**Chain-breaking controls and evidence:** derive tenant context on the server, perform object-level authorization on every request, enforce database row-level security, use separate support-assignment checks, log denied attempts, and run negative tests using valid identities with another tenant's identifiers.

### 6.3 AS-02 — Sensitive-data evasion and external disclosure

**Starting condition:** A customer accidentally or deliberately places prohibited information in free-form ticket text.

**Attack chain:**

1. The value uses spacing, alternate characters, an unexpected format, or context that the current rule set does not recognize.
2. The first detector passes or masks only part of the value.
3. Payload construction reintroduces an excluded field, or the exact final JSON is not reinspected.
4. CMP-09 sends DATA-06 to TP-AI-01 through the legitimate API path.
5. The provider now holds confidential or restricted information; debugging may also copy it into DS-06.

**Chain-breaking controls and evidence:** strict field allow-list, normalization, deterministic rules, contextual Guardrail, block-versus-mask policy, final serialized-payload gate, fail-closed behavior, prohibited-log-field tests, provider retention/deletion terms, and incident handling for any detected escape. The portfolio will demonstrate selected parts with synthetic cases and will document detection limits rather than claim perfect redaction.

### 6.4 AS-03 — Prompt injection produces believable but misleading guidance

**Starting condition:** TA-02 writes a ticket containing instructions directed at the model.

**Attack chain:**

1. Untrusted ticket prose tells the model to ignore LindenArc's instructions, omit a fact, reveal prompt material, or select a particular category.
2. Weak instruction/data separation allows the content to influence the model.
3. TP-AI-01 returns valid JSON containing a plausible summary and an allowed—but incorrect—category.
4. Schema validation passes because the response is structurally valid.
5. CMP-11 retrieves the wrong approved playbook, and a busy ACT-02 accepts it without meaningful comparison.

**Chain-breaking controls and evidence:** clear instruction/data separation, no secrets in prompts, no model tools or action permissions, allowed category or `unknown`, source comparison, easy correction, mandatory manual handling for risk signals, real-model synthetic evaluation, sampled agent review, quality thresholds, and rollback. The mock prototype can show containment and response handling but cannot prove model resistance.

### 6.5 AS-04 — Compromised AI provider returns malicious output

**Starting condition:** An attacker compromises TP-AI-01 or one of its subprocessors while its endpoint and credentials remain technically valid.

**Attack chain:**

1. The attacker can inspect provider-held DATA-06 or influence the generated response.
2. TLS succeeds because LindenArc is communicating with the legitimate but compromised service.
3. The provider returns malformed or sensitive content, or a structurally valid false summary and category.
4. Weak output validation stores unsafe data, or semantic misinformation passes structural validation.
5. The support agent receives misleading information; LindenArc may also be unable to verify deletion or incident scope.

**Chain-breaking controls and evidence:** data minimization, strict output validation, plain-text rendering, human review, provider-change monitoring, quality sampling, manual fallback, kill switch, incident and deletion terms, model/subprocessor inventory, assurance evidence, and exit planning. Provider security itself remains provider-evidence-required.

### 6.6 AS-05 — Privileged or supply-chain change weakens safeguards

**Starting condition:** TA-04 controls an administrator identity, or TA-05 compromises a dependency or deployment workflow.

**Attack chain:**

1. The attacker modifies a detector rule, prompt, schema, category, playbook, provider destination, logging behavior, or dependency.
2. Weak review or deployment protection allows the change into the approved environment.
3. Sensitive content begins passing, unsafe output appears valid, traffic reaches an unintended destination, or security events disappear.
4. Inadequate configuration evidence prevents responders from identifying when and how the control changed.
5. Missing rollback or kill-switch testing extends the exposure.

**Chain-breaking controls and evidence:** phishing-resistant administrator MFA where practical, least privilege, separate duties, protected branches, peer review, exact dependency and action versions, automated tests, secret/dependency scanning, signed or attributable deployment records, configuration monitoring, alerting, protected logs, rollback, and kill-switch exercises.

### 6.7 AS-06 — Resource and retry amplification

**Starting condition:** TA-01/TA-02 submits many permitted tickets, or TP-AI-01 repeatedly times out.

**Attack chain:**

1. Large or frequent requests create many Signal jobs.
2. Missing per-tenant rate, size, and concurrency limits allow the queue to grow.
3. Provider timeouts trigger immediate or excessive retries.
4. Missing idempotency causes duplicate processing and repeated provider charges.
5. Support results are delayed, costs increase, and ordinary ticket handling may be affected.

**Chain-breaking controls and evidence:** maximum input/output size, per-tenant rate and concurrency limits, bounded exponential retry with jitter, stable idempotency, dead-letter handling, cost and queue alarms, provider spending controls, isolation from core ticket handling, manual fallback, and the Signal kill switch.

### 6.8 AS-07 — Logging exposure and investigation blind spot

**Starting condition:** An error path records raw ticket or detector content, or a compromised workload administrator can alter the same evidence used to investigate that activity.

**Failure chain:**

1. Raw DATA-04, DATA-06, credentials, or detected values enter routine logs.
2. Broad log access creates a second disclosure path.
3. Important actor, configuration, rule, request, and result identifiers are missing or cannot be correlated.
4. The same administrator can remove or alter local evidence.
5. LindenArc cannot determine the incident's scope, data, actor, timing, or required response.

**Chain-breaking controls and evidence:** defined sanitized event schema, prohibited-field tests, restricted log access, protected cross-account copies, consistent timestamps and identifiers, alert tests, retention monitoring, and a tabletop investigation using sanitized evidence.

### 6.9 AS-08 — Deleted information returns after restoration

**Starting condition:** A restricted ticket is removed from the live system after its approved security and legal handling.

**Failure chain:**

1. The live database row is deleted, but older S3 versions, provider copies, or backups remain.
2. The request is marked complete without verifying every required location.
3. LindenArc later restores a recovery point created before the deletion.
4. The restore process does not replay the identifier-only deletion ledger.
5. The deleted record silently returns to ordinary service.

**Chain-breaking controls and evidence:** location-specific deletion workflow, noncurrent S3 version expiration, provider confirmation, backup aging, scoped legal holds, exception tracking, verified completion, and a restore test that reapplies later deletions before production access.

### 6.10 AS-09 — Signal gains a payment path after a change

**Starting condition:** A future developer reuses a payment-capable role, library, credential, database connection, queue, or network path to add convenience to Signal.

**Attack chain:**

1. The change gives CMP-07 or CMP-13 access to a financial capability.
2. The architecture or change review fails to recognize the new authority.
3. Prompt-manipulated output, a compromised worker, or an administrator mistake invokes that capability.
4. Signal changes a payment or payment-related state even though it was intended only to advise a human.

**Chain-breaking controls and evidence:** no tools, separate roles and functions, explicit IAM/database/queue/network denials, separate credentials and deployment ownership, negative tests, architecture-drift detection, and a mandatory new threat/privacy/release review before any action capability is proposed.

### 6.11 AS-10 — Compromised payment-provider key creates a false status

**Starting condition:** An attacker compromises TP-PAY-01 or steals valid provider signing or mutual-TLS material.

**Attack chain:**

1. The attacker sends a correctly signed and mutually authenticated status event.
2. LindenArc validates the cryptography but lacks effective freshness, replay, state-transition, or anomaly checks.
3. The status worker records a false success, failure, payee, or transaction state in Aurora.
4. Missing reconciliation allows the false state to remain authoritative.
5. Customers and support personnel act on incorrect financial information; payments may be duplicated, delayed, misdirected, or uncertain.

**Chain-breaking controls and evidence:** unique event IDs, timestamps, narrow acceptance windows, replay cache, monotonic state rules, immutable approved payment snapshot, stable idempotency, reconciliation, anomaly alerts, credential rotation, provider incident notice, payment-dispatch pause, and controlled restart approval. Cryptographic validity alone is not treated as proof that the provider is uncompromised.

### 6.12 AS-11 — Unsafe support knowledge publication

**Starting condition:** A customer ticket contains sensitive data, malicious instructions, or a plausible but incorrect resolution.

**Failure chain:**

1. An agent copies the ticket or Signal draft into a reusable article.
2. The publication process lacks structured fields, DLP inspection, designated technical review, or de-identification approval.
3. The article becomes broadly available after the source ticket should have been deleted.
4. Future agents follow incorrect steps or receive another tenant's information.

**Chain-breaking controls and evidence:** separate structured DATA-16 record, prohibited-field rules, DLP and human review, restricted publication role, provenance without copied ticket text, versioning, owner, product applicability, annual review, immediate retirement, and proof that source deletion does not leave source prose embedded in the article.

### 6.13 Scenario coverage audit

| Coverage requirement | Result |
|---|---|
| Every T-01 through T-11 threat appears in at least one scenario | Pass |
| Every W-01 through W-16 candidate weakness appears in at least one scenario | Pass |
| TB-09 through TB-17 and the identity/data boundaries receive a scenario | Pass |
| Malicious, accidental, third-party, human, supply-chain, and availability sources are represented | Pass |
| Prototype, AWS-lab, design-only, real-model, and provider evidence remain separated | Pass |
| No scenario assumes that a mock provider, Guardrail lab, signature, or proposed control proves end-to-end security | Pass |

### Stage 6 working outcome

The attack model contains eleven focused scenarios with explicit starting conditions, weakness chains, boundary crossings, consequences, chain-breaking controls, and evidence routes. The scenarios are detailed enough to support risk scoring without expanding into live exploitation or a full assessment of every LindenArc feature. Stage 7 will consolidate overlapping scenarios into approximately eight to ten material business risks, score inherent and residual risk, assign treatment and ownership, and produce the launch recommendation.

**Decision status:** Approved by Eniola on September 9, 2026. No live system was attacked; the approved scenarios remain defensive tabletop models and synthetic test requirements.

## PASTA Stage 7 — Analyze and prioritize risk

### What this stage does

Stage 7 translates technical attack scenarios into business decisions. Related threats and weaknesses are consolidated so that leadership receives a focused risk list rather than one row for every possible failure.

### 7.1 Scoring method

Likelihood and impact each use a project-defined five-point scale. This is a transparent decision aid, not a statistically validated forecast or a universal NIST, ISO, or SOC scoring formula.

| Value | Likelihood | Impact |
|---:|---|---|
| 1 | Rare under the stated assumptions | Negligible operational or data effect |
| 2 | Unlikely but credible | Limited, recoverable harm |
| 3 | Possible | Material customer, operational, contractual, or investigation harm |
| 4 | Likely without the proposed safeguards | Major multi-customer, financial, privacy, or service harm |
| 5 | Expected or repeatedly occurring without safeguards | Severe cross-tenant, restricted-data, financial, legal, or sustained operational harm |

`Risk score = Likelihood × Impact`

| Score | Rating |
|---:|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

**Inherent risk** estimates exposure before the proposed safeguards. **Projected residual risk** estimates the target after every listed safeguard is implemented and verified. It is not the current risk and is not achieved merely because a safeguard appears in a design.

### 7.2 Prioritized risk register

| Risk ID | Cause–event–impact statement | Traceability | Inherent L×I | Required treatment | Projected residual L×I | Accountable role | Release decision |
|---|---|---|---:|---|---:|---|---|
| R-01 | If tenant context or object authorization is weak, a valid or compromised user may access another customer's ticket, document, or Signal result, causing cross-tenant disclosure or alteration | T-01/T-02; W-01/W-02/W-03; AS-01 | 4×5 = **20 Critical** | Mitigate with server-controlled tenant context, object authorization, database row-level security, least privilege, assignment checks, and negative cross-tenant tests | 1×5 = **5 Medium** | Application Engineering owner | Block launch until LB-01 and LB-05 evidence passes |
| R-02 | If privileged identities, credentials, dependencies, or change workflows are insufficiently controlled, an attacker or mistake may weaken Signal safeguards or evidence, causing broad unauthorized access or silent control failure | T-02/T-06; W-02/W-03/W-09/W-13; AS-05 | 3×5 = **15 High** | Mitigate through strong administrator authentication, separated roles, short-lived credentials, protected review/deployment, pinned dependencies, automated tests, configuration monitoring, protected evidence, rollback, and kill-switch testing | 2×4 = **8 Medium** | Platform Security owner | Block launch until LB-05, LB-08 and applicable change evidence passes |
| R-03 | If data minimization, detection, final-payload inspection, logging, or AI-provider handling fails, confidential or restricted ticket information may reach an unauthorized destination, causing privacy, contractual, incident, and trust harm | T-03; W-03/W-04/W-05/W-11/W-13; AS-02/AS-07 | 4×5 = **20 Critical** | Mitigate through allow-listing, normalization, layered detection, block/mask policy, exact-payload reinspection, fail-closed behavior, sanitized logging, provider retention/deletion terms, and incident response | 2×4 = **8 Medium** | Signal service owner | Block launch until LB-02 and LB-06 evidence passes |
| R-04 | If ticket instructions influence the model, output validation is incomplete, or human review becomes superficial, Signal may provide a believable false summary or wrong playbook, causing incorrect support handling and customer harm | T-04/T-05; W-06/W-07/W-08; AS-03 | 4×4 = **16 High** | Mitigate with instruction/data separation, no tools, strict output/category validation, `unknown`, source comparison, correction and escalation, real-model evaluation, sampled review, quality thresholds, training, rollback, and kill switch | 2×3 = **6 Medium** | Support Operations owner | Block launch until LB-04 and LB-11 evidence passes |
| R-05 | If TP-AI-01 or its supply chain exposes data, changes model behavior, returns unsafe output, or becomes unavailable, Signal may disclose information, mislead agents, or stop functioning | T-05/T-07/T-08; W-07/W-08/W-11; AS-04 | 3×4 = **12 High** | Mitigate LindenArc's exposure and contractually transfer limited obligations through minimization, validation, provider due diligence, assurance review, model/subprocessor inventory, change notice, incident/deletion terms, monitoring, fallback, exit, and reevaluation | 2×4 = **8 Medium** | Third-Party Risk owner for TP-AI-01 | Block launch until LB-06, LB-08 and applicable LB-11 evidence passes |
| R-06 | If size, rate, concurrency, timeout, retry, duplicate, queue, or spending limits are ineffective, abuse or failure may amplify processing and provider calls, causing backlog, outage, or unexpected cost | T-08; W-11/W-12; AS-06 | 4×3 = **12 High** | Mitigate with per-tenant limits, bounded input/output, concurrency control, timeout, exponential retry with jitter, idempotency, dead-letter handling, alarms, spending controls, manual fallback, and kill switch | 2×2 = **4 Low** | Signal Operations owner | Block launch until LB-08 operational tests pass |
| R-07 | If logs, deletion, provider erasure, backup expiration, or restore procedures are incomplete, LindenArc may expose sensitive evidence, fail to investigate, fail to prove deletion, or restore data that should remain deleted | T-03/T-09; W-05/W-13/W-14; AS-07/AS-08 | 3×4 = **12 High** | Mitigate with sanitized event schemas, prohibited-field tests, protected centralized logs, deletion verification, S3-version expiration, provider confirmation, backup aging, legal-hold exceptions, deletion-ledger replay, and restore testing | 2×3 = **6 Medium** | Data Governance owner | Block launch until LB-09 and required logging evidence passes |
| R-08 | If customer-derived resolution material is reused without de-identification, review, ownership, versioning, and retirement, confidential or unsafe content may become long-lived support guidance | T-06/T-09; W-10; AS-11 | 3×3 = **9 Medium** | Avoid automated AI publication in the initial release and mitigate the manual process with a separate structured record, prohibited fields, DLP, designated approval, restricted publishing, provenance, ownership, review dates, and retirement | 1×2 = **2 Low** | Support Knowledge owner | Block automatic publication under LB-03; manual process requires its evidence before use |
| R-09 | If Signal gains a payment role, credential, tool, queue, database permission, or network path, manipulated output or a compromised worker may initiate or alter financial activity | T-10; W-03/W-15; AS-09 | 2×5 = **10 High** | Avoid the capability: keep Signal advisory-only with separate roles, credentials, services, queues, database permissions, egress, administration, explicit denials, negative tests, architecture-drift detection, and a mandatory new review for any action proposal | 1×5 = **5 Medium** | LindenArc Chief Technology Officer | Block launch until LB-03, LB-05 and Signal/payment-isolation evidence passes |
| R-10 | If TP-PAY-01, its signing material, or its integration is compromised or unavailable, false or missing provider information may corrupt LindenArc payment state, expose banking data, or cause unauthorized, duplicated, delayed, or misdirected payments | T-11; W-16; AS-10 | 3×5 = **15 High** | Mitigate and contractually transfer limited obligations through provider due diligence, licensing and assurance review, narrow credentials, mutual TLS, signatures, freshness/replay checks, immutable approvals, idempotency, reconciliation, anomaly alerts, incident coordination, dispatch pause, recovery, and controlled restart | 2×5 = **10 High** | Payment Service owner | Block launch if LB-07 evidence fails; remaining High risk requires written executive acceptance under LB-10 |

### 7.3 Risk-profile summary

| Rating | Inherent count | Projected count if every safeguard is verified |
|---|---:|---:|
| Critical | 2 | 0 |
| High | 7 | 1 |
| Medium | 1 | 7 |
| Low | 0 | 2 |

R-01 was raised from 3×5 High to 4×5 Critical during Eniola's review. Its impact was already scored at the maximum value of 5. The correction raises inherent likelihood from Possible to Likely because, before the proposed tenant-context, object-authorization, assignment, and database row-level safeguards, a pooled multi-tenant application repeatedly exposes tenant-addressable objects to authenticated users and support workflows. The score does not say a breach is inevitable; it says that the untreated architecture would create a likely path to severe harm.

The projected profile does not mean the feature is safe today. The current evidence state is incomplete, so the projected scores are conditional targets. R-01 remains Medium after safeguards because the controls sharply reduce likelihood but cannot reduce the severe impact if cross-tenant access nevertheless occurs. R-10 remains High because strong LindenArc controls can reduce likelihood but cannot remove the severe potential impact of a compromised payment provider.

### 7.4 Risk-treatment rules

- **Avoid:** Do not introduce the risky capability. This applies to autonomous payment authority and automatic knowledge publication in the initial release.
- **Mitigate:** Reduce likelihood or impact with safeguards and verify them through appropriate evidence.
- **Transfer:** Use contracts, insurance, indemnification, or provider obligations for limited consequences. Accountability and customer impact cannot be completely transferred.
- **Accept:** A designated executive may knowingly accept remaining risk with rationale, conditions, monitoring, and review date. The security analyst recommends but does not accept material risk.

No Critical residual risk may proceed. A High residual risk requires explicit written acceptance by the designated LindenArc executive risk owner after all required controls and evidence are complete. Missing evidence is not a reason to lower a score.

### 7.5 Current launch recommendation

**Current recommendation: DELAY.** The design is promising, but Signal is not ready for launch at the present evidence state because:

1. the Python/Streamlit gateway and automated tests have not yet produced prototype evidence;
2. the Amazon Bedrock Guardrail lab has not yet produced AWS evidence;
3. cross-tenant authorization, production IAM, logging, kill-switch, deletion, and restoration safeguards remain design-only;
4. real-model prompt-injection, quality, omission, and category behavior has not been evaluated;
5. TP-AI-01 and TP-PAY-01 assurance, contractual, incident, retention, and operational evidence is unavailable; and
6. the remaining projected High payment-provider risk has not been accepted by the designated executive owner.

This is not a recommendation to abandon Signal. It is a recommendation to complete the defined release gates before exposing customer-derived data to a model service.

### 7.6 Target decision after evidence

Signal may become eligible for an **approve-with-conditions controlled pilot** only when:

- R-01 through R-09 meet their mapped launch gates and no target residual score remains Critical or unapproved High;
- every prototype and AWS-lab claim has passing, reproducible, sanitized evidence;
- real-model evaluation meets predeclared quality and safety thresholds;
- required provider evidence and terms have been reviewed and approved;
- manual support, incident response, rollback, and kill-switch procedures are tested;
- R-10's remaining High residual risk is remediated further or formally accepted by the correct executive owner; and
- monitoring, review frequency, owners, thresholds, and pilot exit criteria are recorded.

The pilot should begin with limited users or ticket categories and no autonomous actions. Broader release requires review of pilot results, agent corrections and overrides, security events, provider behavior, support outcomes, and any material architecture or model change.

### 7.7 Complete PASTA traceability chain

The stable identifier chain is now:

`Business/security objective → DATA/DF/TB → Threat → Weakness → Attack scenario → Risk → Safeguard/evidence → Launch blocker`

Example:

`SO-02 → DATA-06/DF-19/TB-11 → T-03 → W-04/W-05 → AS-02 → R-03 → prototype + AWS lab + provider terms → LB-02/LB-06`

### 7.8 Stage 7 completeness test

Stage 7 passes only if every AS-01 through AS-11 scenario is represented in the ten-risk register, scores use the documented method, projected residual risk is not confused with achieved risk, treatments and accountable roles are named, missing provider evidence remains visible, and the launch recommendation follows the launch blockers rather than the desired project outcome.

### Stage 7 working outcome

The ten material risks produce two Critical, seven High, and one Medium inherent rating. If every safeguard and evidence requirement is completed, the target profile becomes one High, seven Medium, and two Low risks. The current decision is Delay; the target decision is eligibility for an approve-with-conditions controlled pilot after all required evidence, provider gates, human-oversight conditions, and executive acceptance are satisfied.

**Decision status:** Approved by Eniola on September 9, 2026 after raising R-01 cross-tenant access from 3×5 High to 4×5 Critical. The seven-stage PASTA analysis is complete; later evidence may update risk status but must not silently rewrite the approved reasoning or historical scores.

## Source anchors

- [VerSprite PASTA methodology](https://versprite.com/cybersecurity-listings/devsecops/pasta-threat-modeling/): PASTA is a seven-stage, risk-centric method; Stage 1 defines business and security objectives and business-impact considerations.
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html): threat modeling is a structured process for understanding a system, identifying applicable threats, determining responses, and reviewing whether the work is sufficient.
- [Microsoft STRIDE threat model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats): STRIDE provides the six threat categories used here as a coverage check.
- [OWASP Top 10 for LLM and GenAI](https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/): the current AI-application categories are used to check relevance and document intentional exclusions, not to declare automatic findings.
- [OWASP API Security Top 10 — 2023](https://owasp.org/API-Security/editions/2023/en/0x10-api-security-risks/): the current published API categories are used to check tenant/object authorization, authentication, resource consumption, configuration, inventory, and external-API consumption paths.
- Project inputs: `work/01_scenario_charter.md`, `work/02_aws_architecture_design_brief.md`, `work/02b_risk_candidate_log.md`, and `work/03_data_inventory_and_lifecycle.md`.
