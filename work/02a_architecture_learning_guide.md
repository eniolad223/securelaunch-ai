# SecureLaunch AI Architecture Learning Guide

**Status:** Reconciled to the evidence-backed portfolio scope on September 7, 2026  
**Purpose:** Help Eniola understand and explain the reference architecture in an interview  
**Writing rule:** The first use of an uncommon abbreviation must show the complete term followed by the abbreviation in parentheses.

## The whole idea in one sentence

AWS supplies managed technology building blocks, while LindenArc combines and configures those blocks to operate its own SaaS product.

AWS is not supplying the finished LindenArc application. LindenArc's developers write the business rules and decide how the AWS services work together.

## Three different things in this portfolio

### The reference architecture

This is the complete fictional production design. It explains how LindenArc could use AWS services, TP-AI-01, and TP-PAY-01. It is designed and threat-modeled, not deployed.

### The Signal Security Gateway Lab

This is the real Python and Streamlit application Eniola will build. It implements only the security checkpoint around a proposed AI request and response. It uses fixed synthetic cases rather than a real ticket database, login system, payment service, or customer data.

### The Amazon Bedrock Guardrails lab

This is a small real AWS experiment. Synthetic text is submitted through `ApplyGuardrail` to prove that Eniola can configure and evaluate the selected managed safeguard. It does not deploy the full reference architecture or call a foundation model.

## Prototype terms

### Streamlit

Streamlit is a Python framework for creating a visual application. The screen and the security engine are part of the same project: the screen presents a fixed scenario, calls the gateway, and displays the gateway's real result. It is not a picture or a separate mockup.

### API request and mock HTTP transport

An **Application Programming Interface (API)** request is a structured message one program sends to another. In the fictional production design, Signal would send an HTTPS API request to TP-AI-01.

The portfolio application constructs that request for `tp-ai-01.invalid`, a special-use fictional address, but uses HTTPX `MockTransport` to intercept it locally and return a prepared response. The public/demo build has no real-network option. Therefore, `provider_invoked = true` means the simulated request reached the local provider adapter. It does not mean a real provider or internet endpoint received data.

The mock transport belongs to the test project; it is not another provider or another application. It lets automated tests inspect the exact payload and prove that a blocked case never reached the outbound adapter.

### Fixed synthetic scenario

A synthetic scenario is a made-up ticket containing only reviewed fictional values. The public application provides a dropdown of these cases and does not accept unrestricted visitor text or uploads. This keeps the portfolio from collecting real personal or confidential information.

### Automated test and continuous integration

An automated test gives the program an input and checks the actual result against an expected result. **Continuous integration (CI)** means GitHub Actions reruns those tests when the code changes. A passing test proves only the tested behavior and case; it does not prove that the entire fictional production system is secure.

### Evidence status

Every material claim receives one of four labels:

- **Design-only:** proposed in the reference architecture but not implemented.
- **Prototype-tested:** exercised through the local or public synthetic Python application.
- **AWS-lab-tested:** exercised against the recorded Amazon Bedrock Guardrail configuration.
- **Provider-evidence-required:** cannot be proven by our code and requires real provider or contractual evidence.

## The most important services

### AWS Lambda

**Lambda is not an abbreviation.** It is the name of an AWS computing service and is spelled L-A-M-B-D-A.

Lambda runs a piece of LindenArc code when an event occurs. LindenArc does not reserve or maintain a permanent application server for that task; AWS starts the needed computing environment, runs the code, and manages the underlying servers.

Example: an approver clicks **Approve expense**. Amazon API Gateway sends the request to a Lambda function. The function checks the user's identity, role, tenant, and the expense's current status. If the action is permitted, the function updates the database.

Real organizations use Lambda for short, event-driven work such as processing an API request, resizing an uploaded image, reacting to a security alert, or starting a background workflow. “Serverless” does not mean that servers do not exist. It means AWS manages those servers instead of the customer managing them directly.

### API Gateway

**API** means **Application Programming Interface**. An API is a controlled way for one program to request something from another program.

Amazon API Gateway is the reception desk for LindenArc's backend. It receives requests such as “show this invoice” or “create this ticket,” checks required access-token information, rejects invalid requests, and forwards an accepted request to the correct Lambda function.

The browser does not connect directly to Lambda or the database.

### Amazon Aurora PostgreSQL-Compatible Edition

Aurora is a managed relational database created by AWS. It is part of the **Amazon Relational Database Service (Amazon RDS)** family.

**SQL** means **Structured Query Language**, the language used to create, read, update, and organize relational database records. **PostgreSQL** is a widely used open-source relational database system; PostgreSQL is a product name, not an abbreviation. “Aurora PostgreSQL-Compatible” means Aurora works with many of the same tools, drivers, and SQL features used with PostgreSQL while AWS manages much of the underlying database infrastructure.

A relational database is similar to a collection of connected spreadsheets with much stronger rules. A tenant record can be connected to its users, vendors, invoices, expenses, approvals, and tickets. The database can enforce valid relationships and complete several related changes as one transaction.

Example: when an expense is approved, Aurora can save the approval, approver, time, and new expense status together. If one required part fails, the transaction rolls back instead of leaving a half-completed approval.

Companies use relational databases for systems where records have important relationships and accuracy matters: orders, subscriptions, inventory, financial workflows, customer accounts, and support cases.

### Amazon RDS Proxy

**RDS** means **Relational Database Service**.

RDS Proxy is not a web-browsing proxy. It is a database connection manager positioned between Lambda and Aurora.

Opening a new database connection takes time and consumes database capacity. Lambda may create many short-lived function instances during a traffic spike. If every instance repeatedly opens its own fresh connection, the database can become overloaded even when the actual queries are small. RDS Proxy keeps a managed pool of reusable connections and shares them safely with the application.

Analogy: Aurora is an office with a limited number of doors. Lambda requests are visitors. RDS Proxy is the coordinator who reuses the available doors instead of attempting to construct a new door for every visitor.

### Amazon S3

**S3** means **Simple Storage Service**.

S3 is object storage. An object is a file plus information describing that file. LindenArc uses S3 for invoice PDFs, receipt images, and support attachments rather than placing large files inside Aurora.

Real organizations use S3 for documents, images, videos, backups, log archives, data exports, and static website files. An S3 bucket is a top-level container for objects; it is not automatically public.

LindenArc uses temporary presigned requests. These allow one approved upload or download without giving a user general AWS credentials or general access to the bucket.

### Amazon VPC and Availability Zones

**VPC** means **Virtual Private Cloud**. It is a logically isolated network that LindenArc configures inside AWS. It is not a separate physical cloud or LindenArc-owned data center.

An **Availability Zone (AZ)** is a distinct AWS infrastructure location inside an AWS Region. Using private subnets across two Availability Zones reduces dependence on a single location.

Aurora and its database access path are private. “Private” here means they do not accept direct connections from the public internet. API Gateway can invoke the approved Lambda function, and the function reaches the database through the controlled private path.

### IAM

**IAM** means **Identity and Access Management**.

IAM controls what AWS identities and AWS services may do. A Lambda function receives an IAM role containing limited permissions—for example, permission to write application logs and use one database proxy, but not permission to administer every AWS service.

IAM protects access to AWS resources. LindenArc's application authorization separately decides whether a particular customer user may approve an expense or read a ticket.

### AWS KMS and SSE-KMS

**KMS** means **Key Management Service**. It manages encryption keys and controls which approved identities or services may use them.

**SSE-KMS** means **Server-Side Encryption with AWS Key Management Service keys**. S3 or Aurora encrypts stored data using protected key material managed through KMS.

An encryption key is not the same as a password. It is cryptographic material used to transform readable information into an unreadable form and back again for an authorized use.

### AWS Secrets Manager

Secrets Manager protects secret values such as database credentials or an external provider's API credential. It allows controlled access and rotation without writing those values directly into source code.

KMS and Secrets Manager have different jobs: KMS manages encryption keys; Secrets Manager stores and rotates secret application values and uses KMS-backed encryption to protect them.

### Amazon GuardDuty Malware Protection for S3

GuardDuty is an AWS threat-detection service. Its Malware Protection for S3 capability can inspect newly uploaded S3 objects and report a result.

LindenArc treats a new upload as untrusted. Only a `NO_THREATS_FOUND` result makes the file available. A threat, failed scan, unsupported file, or missing result leaves it quarantined. This is called **failing closed**: uncertainty does not silently become permission.

Malware scanning reduces risk but cannot prove that a document is harmless or truthful. It is one defensive layer.

### Amazon EventBridge

EventBridge routes events between services. An event is a structured message saying that something happened.

Example: GuardDuty finishes scanning an uploaded receipt. It publishes a result event. EventBridge routes that result to the scan-status Lambda function, which updates the object's status in Aurora.

### Amazon CloudWatch

CloudWatch collects operational logs, measurements, and alarms. LindenArc could use it to answer questions such as: Did an API function fail? Has latency increased? Are file scans failing unusually often?

CloudWatch is not the main business database. Its logs should contain enough metadata to investigate an event without copying ticket bodies, receipts, passwords, or access tokens into the logs.

## One realistic LindenArc example

An employee uploads a $128 travel receipt:

1. The user signs in and selects the correct LindenArc tenant.
2. The browser sends an API request to create an expense.
3. API Gateway validates the access token and forwards the request to Lambda.
4. Lambda verifies that this user may create expenses for that tenant.
5. Lambda uses RDS Proxy to write the expense metadata to Aurora.
6. Lambda gives the browser a short-lived presigned S3 upload request for a unique object key.
7. The browser uploads the receipt to the private business-documents bucket.
8. GuardDuty scans the receipt and EventBridge routes the result to a scan-status Lambda function.
9. If the result is clean, the receipt becomes available to an authorized approver. Otherwise, it stays quarantined.
10. CloudWatch receives sanitized operational events, while KMS-backed encryption protects stored data.

## Supporting terms from the entry and identity path

| Term | Complete name | Simple meaning |
|---|---|---|
| AWS | Amazon Web Services | The public cloud provider hosting LindenArc's reference architecture |
| DNS | Domain Name System | Translates a human-friendly application name into the destination used by computers |
| HTTPS | Hypertext Transfer Protocol Secure | Encrypts web traffic while it travels across a network |
| TLS | Transport Layer Security | The security protocol that protects an HTTPS connection |
| CDN | Content Delivery Network | Delivers web content through distributed edge locations; CloudFront is AWS's CDN |
| WAF | Web Application Firewall | Filters web requests for configured abusive patterns and excessive rates |
| MFA | Multi-Factor Authentication | Requires more than one type of proof during sign-in |
| OAuth 2.0 | Open Authorization 2.0 | A standard framework for granting limited application access with tokens |
| PKCE | Proof Key for Code Exchange | Protects an OAuth authorization code from being reused by an interceptor |
| CORS | Cross-Origin Resource Sharing | Browser rules controlling which web origins may call an API |
| OAC | Origin Access Control | Lets CloudFront retrieve approved private S3 content without making the bucket public |
| ACM | AWS Certificate Manager | Creates and manages certificates used for HTTPS |

## Signal AI processing terms

### LLM

**LLM** means **Large Language Model**. It is a model trained to process and generate language. Signal asks an external LLM to transform one support ticket into a draft summary. It is not given access to LindenArc's database or application controls.

### Pretraining, inference, in-context guidance, and fine-tuning

**Pretraining** is the large, expensive process that teaches a foundation model broad language patterns from a very large dataset. LindenArc does not perform this.

**Inference** is using an already trained model to answer one request. Signal sends the current minimized ticket and receives one response through TP-AI-01's API. The model uses that ticket as temporary context; the request does not automatically change the model or make it remember the ticket.

**In-context guidance** means placing instructions, category definitions, or synthetic examples inside the request. It is similar to giving an experienced worker a task sheet and examples for the assignment in front of them. It can improve the current answer without retraining the worker's underlying general ability.

**Fine-tuning** changes a pretrained model's internal parameters using a specialized dataset. LindenArc does not fine-tune the initial Signal release. A future fine-tuning proposal would create a new sensitive dataset and require separate privacy, security, quality, provider, retention, poisoning, and release analysis.

**Evaluation** does not teach the model. It measures whether the entire Signal configuration meets predefined expectations. LindenArc can use evaluation errors to revise prompts, categories, validation, playbooks, or model selection even though it does not modify the model itself.

The external model does not need to memorize LindenArc's product to perform the initial narrow task. The current ticket contains the facts to summarize, the request supplies the permitted category definitions, and LindenArc—not the model—supplies product-specific troubleshooting knowledge through approved playbooks.

### SQS and a queue

**SQS** means **Simple Queue Service**. A queue is a waiting line for background work.

When a ticket is saved, a small message saying “Signal job 123 is ready” enters the queue. A worker processes it when capacity is available. The customer does not have to wait for the summary before the ticket is accepted.

### Asynchronous

**Asynchronous** means work can continue without waiting for another task to finish immediately. LindenArc saves the ticket first and processes the Signal summary in the background.

### DLQ

**DLQ** means **Dead-Letter Queue**. It is a separate holding area for a message that repeatedly failed. “Dead letter” does not mean the ticket is deleted. It means the failed job is removed from normal retries so people can investigate it.

### Transactional outbox

A transactional outbox is a database table containing durable notes about background work that must happen.

LindenArc saves the ticket and its outbox note in one database transaction. If both save successfully, a dispatcher can always find the work later. If the transaction fails, neither is saved. This prevents a ticket from being stored while its Signal job is silently lost.

### Idempotent

Idempotent means repeating the same operation produces the same intended result instead of creating duplicate effects. If SQS delivers one Signal job twice, LindenArc still keeps one active result for that job.

### PII and data minimization

**PII** means **Personally Identifiable Information**. It includes information that can identify a person, such as a name or email address.

Data minimization means sending only information required for a task. Signal sends minimized ticket text and limited context—not attachments, tenant names, access tokens, payment data, or other tickets. Because people can type unexpected information into free text, automated PII masking reduces risk but cannot guarantee perfect removal.

### Prompt injection

Prompt injection occurs when untrusted text attempts to make a language model ignore its intended instructions. A customer might put “ignore your instructions” inside a ticket.

Signal treats the ticket as data, validates the output, and gives the model no tools or action permissions. Therefore, even if manipulation affects the wording of a summary, the model still cannot approve an expense, retrieve another tenant's records, or reset an account.

### System instructions and structured output

System instructions tell the model its narrow job and rules. The untrusted ticket is placed in a separate labeled field rather than blended into those instructions.

Structured output means requiring predictable named fields, such as `summary`, `key_facts`, and `uncertainty`. LindenArc rejects a response that has the wrong structure or exceeds the approved length.

### Human in the loop

Human in the loop means a person remains responsible for reviewing or approving the result. The support agent sees both the original ticket and a clearly labeled AI-generated draft. Signal does not act by itself.

### Egress and NAT Gateway

Egress means network traffic leaving LindenArc's AWS environment. **NAT** means **Network Address Translation**.

A NAT Gateway lets a worker in a private subnet make an outbound connection without making that worker publicly reachable. AWS Network Firewall restricts that outbound route to approved provider destinations.

### Feature flag and kill switch

A feature flag is a configuration value that turns a feature on or off without changing the application's code. The Signal flag in AWS AppConfig acts as a kill switch: LindenArc can stop new AI-provider calls while the normal support-ticket system continues working.

### Two different meanings of token

An access token is signed proof used for application access. An LLM token is a small unit of text used to measure model input and output. They share the word “token” but serve completely different purposes. Signal may record LLM token counts for cost monitoring, but an access token must never be included in an AI request.

### DLP, regex, and contextual detection

**DLP** means **Data Loss Prevention**. It describes controls intended to detect or stop sensitive information from leaving an approved boundary.

**Regex** means **regular expression**. A regular expression is a pattern used to find text with a predictable structure. For example, a rule can look for nine digits arranged like a United States Social Security number. A payment-card candidate can also be checked with a checksum so every long number is not automatically treated as a valid card number.

Regex is useful but incomplete. People add spaces, punctuation, words, or typing mistakes, and some information is sensitive only because of its context. LindenArc therefore combines exact patterns with contextual PII detection.

Amazon Bedrock Guardrails can perform this inspection without using a Bedrock foundation model. Its `ApplyGuardrail` API can detect or mask supported PII types and apply LindenArc's custom regular expressions. High-risk findings block the external AI call; lower-risk direct identifiers may be replaced with placeholders such as `{NAME}` or `{EMAIL}`.

The inspection result is also sensitive. Detector traces can contain the original matched value, so LindenArc does not copy those traces into ordinary logs.

### Defense in depth, normalization, and the outbound gate

**Defense in depth** means using several protective layers so one failure does not immediately expose data. Signal does not depend on one “perfect” DLP filter.

**Normalization** means putting text into a consistent supported form before inspection—for example, standardizing Unicode, line breaks, and spacing. This helps rules recognize values that were formatted in unusual ways. It improves detection but cannot reveal every disguised or context-dependent secret.

After minimization and contextual inspection, Signal builds the exact JSON request for TP-AI-01. A separate **outbound gate** inspects that final request, confirms that only approved fields exist, and reruns the highest-risk checks. Checking the final object matters because a later programming mistake could otherwise reintroduce a forbidden field after an earlier scan.

**Fail closed** means that uncertainty or control failure results in no external AI call. The backup is the ordinary manual-support process—not a weaker filter and not an attempt to send the ticket anyway. Network Firewall then limits the allowed destination, but it cannot decide whether the text itself is confidential.

### Controlled troubleshooting assistance

A troubleshooting playbook is a human-written, approved checklist for a known support issue. Signal may select one issue category from a small allow-list, but it does not invent the checklist.

Example: if Signal returns the valid category `receipt-upload-error`, the LindenArc application retrieves the current approved checklist for that category from Aurora. The agent sees suggested starting checks such as confirming the supported file type and file-size limit. The model cannot edit the playbook or execute a step.

This is a simple database lookup, not retrieval-augmented generation. An unknown or invalid category produces no suggestion.

## Payment-provider and security-operations terms

### Tokenization and an opaque reference

Tokenization replaces sensitive payment information with a reference that has no useful meaning outside the provider's system. Here, “token” means a provider reference—not an application access token or an LLM text token.

The licensed payment provider collects the customer's banking details on its own hosted page. It returns an opaque reference to LindenArc. LindenArc stores and later sends that reference with an approved amount and currency, while the provider retains the underlying bank information and moves the money.

### Separation of duties

Separation of duties means one identity should not control every important part of a sensitive process. A user may prepare a payable, another authorized user approves it when policy requires, and a narrowly permitted application worker sends the instruction. The payment worker cannot create its own approval.

### Idempotency key

Idempotency means that repeating the same request does not repeat its financial effect. An idempotency key is the stable unique identifier attached to one payment instruction.

If LindenArc sends a payment and the network connection times out, it reuses the same key when checking or retrying. It does not create a new key, because the provider might already have accepted the first instruction.

### Webhook

A webhook is an inbound message sent automatically when something changes. The payment provider uses a webhook to tell LindenArc that a payment is processing, completed, failed, or returned.

Because anyone on the internet could attempt to imitate a webhook, LindenArc verifies the provider's certificate, message signature, timestamp, and unique event identifier before accepting the update.

### mTLS

**mTLS** means **mutual Transport Layer Security**. Ordinary TLS lets the client verify the server. Mutual TLS also requires the client—in this case, the payment provider—to present a trusted certificate to LindenArc's API endpoint.

A signed webhook provides an additional application-level check. Mutual TLS and message signing are separate layers; neither makes replay protection unnecessary.

### Reconciliation

Reconciliation means comparing LindenArc's payment record with the provider's authoritative record and investigating differences. It catches missing webhooks, delayed updates, and uncertain network results.

### TPRM and provider due diligence

**TPRM** means **Third-Party Risk Management**. It is the process of identifying which outside providers matter, checking their risks before use, writing requirements into contracts, monitoring them, preparing for incidents, and safely ending the relationship when necessary.

Provider due diligence means gathering and evaluating evidence before deciding to trust the provider. It is not necessarily a full audit. LindenArc would normally review independent reports and test its own integration; the contract may preserve additional evidence or audit rights for serious circumstances.

For example, LindenArc does not simply ask, “Do you use separation of duties?” It asks for appropriate evidence that the provider restricts powerful access, independently reviews sensitive actions, protects signing keys, and tests incident recovery. Because this is fictional, the portfolio records these as release requirements rather than pretending the evidence was received.

### SOC 2 Type II and conditional PCI DSS evidence

**SOC 2** means **System and Organization Controls 2**. A SOC 2 Type II report is an independent accountant's report about selected controls and whether they operated over a period of time. It is useful evidence, but it is not a security guarantee or a product certification. LindenArc must read exceptions, scope, complementary customer responsibilities, and subservice-provider treatment instead of accepting the report title alone.

**PCI DSS** means **Payment Card Industry Data Security Standard**. It applies to environments involving payment-card account data. LindenArc should request PCI DSS evidence only if the provider's service actually puts cardholder data in scope; bank-account payments do not automatically make PCI DSS the correct standard.

### Third-party risk can cross a boundary without a network breach

The provider has no direct connection into LindenArc's VPC or database, so a provider breach does not automatically become an AWS breach. The effects can still cross back in several ways: exposed customer data, forged or incorrect provider messages, delayed payments, uncertain transaction status, and damage to LindenArc's customer relationships.

This is sometimes called **concentration risk** when too much of an important service depends on one provider. LindenArc limits the immediate damage with authenticated messages, reconciliation, least privilege, and a payment-dispatch kill switch. It also plans a safe exit, but does not automatically switch to an unapproved provider during an incident.

### AWS Organizations and separate accounts

AWS Organizations centrally groups and governs multiple AWS accounts. An AWS account is also a security boundary.

LindenArc's reference design separates the Production Workload, Security Tooling, and Log Archive accounts. A compromised production administrator should not automatically have permission to erase centralized findings, logs, or backups.

### AWS CloudTrail

CloudTrail records AWS management activity, such as changing an IAM role, KMS key, firewall, or bucket policy. It answers “Who changed this AWS resource, what did they change, and when?”

CloudTrail is different from CloudWatch: CloudTrail focuses on AWS API activity, while CloudWatch focuses on application logs, measurements, and alarms.

### AWS Config

AWS Config records how AWS resources are configured and how those configurations change. Rules can flag a resource that becomes public, loses encryption, or stops meeting another selected configuration requirement.

### AWS Security Hub CSPM

**CSPM** means **Cloud Security Posture Management**. AWS Security Hub CSPM collects and normalizes findings from multiple security services so analysts have one place to triage them. A clean dashboard does not by itself prove that LindenArc is compliant.

### Amazon Macie

Macie detects likely sensitive data stored in Amazon S3. It is a detective control for stored objects. It does not inspect Aurora ticket text and is not the inline DLP filter that protects the Signal provider request.

### Amazon SNS

**SNS** means **Simple Notification Service**. EventBridge can route an important finding to SNS, which then sends the alert to an approved security-response destination.

### Backup Vault Lock and restore testing

AWS Backup creates recovery copies. Backup Vault Lock protects approved recovery points from early deletion or weakened retention settings.

A successful backup message proves only that a copy was created. Restore testing verifies that LindenArc can actually rebuild a usable resource from a selected recovery point.

## Re-evaluation result

The application and data architecture remains a strong fit for the fictional scenario:

- Lambda fits short API and event-driven tasks; the design does not pretend it is the only possible compute choice.
- Aurora PostgreSQL fits connected financial-workflow records and transactional updates.
- RDS Proxy has a specific reason to exist: it protects Aurora from serverless connection churn.
- Separate S3 buckets keep business documents and support attachments under different access and future lifecycle rules.
- GuardDuty scanning creates a defensible quarantine boundary without requiring LindenArc to build a malware engine.
- Row-level security is a second tenant barrier, not a substitute for authorization in Lambda.
- Controlled troubleshooting adds practical value without giving the model permission to invent or execute support procedures.
- Provider-hosted payment onboarding and opaque references keep raw banking credentials outside LindenArc's systems.
- Stable idempotency and reconciliation prevent an uncertain network result from becoming a duplicate payment.
- Separate security and log accounts preserve visibility and recovery evidence if the production account is compromised.
- The architecture remains a simulated reference design. Selected gateway behavior will be prototype-tested and one Guardrail configuration will be AWS-lab-tested, but the full services have not been deployed, load-tested, audited, or certified.
- The public Streamlit demonstration uses fixed synthetic cases only and no live provider or AWS credentials.
- The mock HTTP transport produces repeatable API-boundary evidence but does not prove real TP-AI-01 transport, security, availability, or contractual behavior.

No component is present only for decoration. Removing RDS Proxy, tenant-aware row-level security, private object storage, or quarantine handling would create a meaningful weakness. No additional database or compute platform is currently necessary.
