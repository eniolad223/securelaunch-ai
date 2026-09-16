# SecureLaunch AI Scenario Charter

**Status:** Scenario approved September 4, 2026; evidence-backed portfolio validation scope approved September 7, 2026  
**Case-study type:** Simulated cloud-security readiness review  
**Fictional company:** LindenArc Technologies  
**Core product:** LindenArc Financial Operations Platform  
**Proposed AI feature:** LindenArc Signal

## 1. The fictional business

LindenArc Technologies is a fictional business-to-business software-as-a-service company. Its customers are small and midsize organizations that use the LindenArc platform to manage accounts-payable and employee-expense work.

The platform helps customer finance teams receive and organize vendor invoices, submit expenses and receipts, route items for approval, monitor payment status, and maintain records for reconciliation and reporting. LindenArc does not directly hold or transmit customer funds. Actual money movement is performed by a fictional external licensed payment provider.

LindenArc is multi-tenant: several customer organizations use the same cloud platform, while each customer's users and data must remain logically separated from every other customer.

## 2. The proposed AI feature

LindenArc Technologies plans to launch LindenArc Signal, an AI-assisted feature for the company's internal customer-support team.

The ordinary LindenArc support-ticket system already exists in the fictional scenario; Signal does not. Signal is the proposed new LindenArc-owned feature added around that existing workflow. It includes LindenArc's queuing, data minimization, prompt construction, output validation, category handling, playbook lookup, user-interface, evaluation, monitoring, and shutdown controls. The hosted language model is one external component called through TP-AI-01's API; it is not Signal by itself, and LindenArc does not download or own it.

When a customer submits a support ticket, Signal sends the ticket's minimized written content and limited ticket context to an external large-language-model service. The model returns a concise summary and selects an issue category from LindenArc's small approved category list. The application then retrieves a versioned, human-authored troubleshooting checklist associated with that category. The summary and suggested approved starting steps are stored or linked with the original ticket and shown to an authorized LindenArc support agent.

Signal is intended to help a human agent understand a case and begin approved troubleshooting more quickly. It does not replace the original ticket, an approved support playbook, or the agent's judgment.

### Signal is allowed to

- summarize the customer's written ticket;
- identify the main issue described in the ticket;
- select one issue category from a small LindenArc-approved list or return `unknown`;
- organize key facts already present in the ticket; and
- display the draft summary and the category's versioned, human-authored troubleshooting checklist to an authorized human support agent.

### Signal is not allowed to

- send a response to the customer;
- approve, initiate, cancel, or modify a payment;
- approve an expense or invoice;
- reset an account or change access permissions;
- close or reassign a ticket automatically;
- change financial or customer records;
- invent an unrestricted troubleshooting procedure or replace the approved LindenArc playbook;
- execute a troubleshooting step or call a diagnostic, account, financial, or administrative tool;
- make a final fraud, legal, compliance, or security decision; or
- take any other autonomous action.

Attachments may be stored with a ticket, but the initial Signal release does not send attachments to the AI service.

### AI model adaptation and evaluation boundary

Signal uses a pretrained external foundation model through an API. LindenArc does not train or fine-tune that model in the initial release, and the selected provider must contractually exclude LindenArc inputs and outputs from provider model training.

LindenArc adapts the service through versioned instructions, a fixed response schema, approved issue categories, deterministic validation, and synthetic examples. Before release, it evaluates those configurations with fictional test tickets and expected results. After release, structured agent corrections and quality measurements inform human-approved changes to the prompt, category list, validation rules, playbooks, or selected model version; production tickets are not automatically turned into training data.

At inference time, the model receives the current approved minimized ticket plus the task instructions and category definitions. This provides case-specific and LindenArc-specific context for that one response without changing the model's internal parameters or teaching it to remember the ticket later.

Any future fine-tuning or training using customer-derived information requires a new privacy review, data-flow change, threat analysis, authorization, provider assessment, evaluation plan, and release decision. It is not included in this case study's initial Signal release.

## 3. People and systems involved

- **Customer finance administrator:** configures the customer's organization and manages authorized users.
- **Accounts-payable specialist:** reviews invoices, vendor records, approvals, and payment status.
- **Employee or expense submitter:** submits an expense and supporting receipt.
- **Approver:** approves or rejects an invoice or expense according to company policy.
- **Customer-support agent:** reads customer tickets and reviews Signal's AI-generated summary.
- **Support operations lead:** owns, approves, versions, and periodically reviews the troubleshooting playbooks and allowed issue-category list.
- **LindenArc administrator:** performs tightly controlled platform-administration work.
- **Engineering and security teams:** build, test, monitor, and protect the platform.
- **TP-PAY-01 — Licensed Payment Execution Provider:** performs regulated money movement outside LindenArc.
- **TP-AI-01 — External AI Model Service Provider:** hosts the pretrained model service and processes the limited ticket content sent for summarization.
- **CSP-01 — Amazon Web Services:** serves as the cloud service provider hosting the simulated reference architecture.

## 4. Important data

The scenario may involve:

- names and business email addresses;
- user and tenant identifiers;
- authentication and access-control data;
- vendor names and contact information;
- invoice numbers, descriptions, amounts, and payment status;
- employee expense details and receipts;
- customer-support ticket text and attachments;
- AI prompts, generated summaries, approved issue categories, playbook identifiers and versions, human-review status, and model-response metadata;
- audit, application, security, and access logs; and
- payment-provider references or tokens.

The design does not intentionally store raw card numbers, online-banking passwords, or payment-provider private keys. A customer might nevertheless place excessive or sensitive information inside free-form ticket text, which is one reason the proposed AI data flow requires a security review.

## 5. Business goal

LindenArc Technologies wants Signal to reduce the time support agents spend reading long tickets and locating approved initial troubleshooting steps while preserving accurate human decision-making and customer trust.

## 6. Security goal

Before launch, LindenArc wants to determine whether the proposed feature protects tenant separation, sensitive data, identities, APIs, secrets, logs, and third-party connections well enough to proceed. The review must identify high-priority risks, required safeguards, evidence needed to verify those safeguards, and any conditions that should block release.

## 7. Portfolio assessment scope

The SecureLaunch AI project will produce:

- an executive launch brief;
- an AWS architecture and data-flow diagram;
- a data inventory and lifecycle;
- a seven-stage PASTA threat model;
- a focused risk register;
- secure-software-development lifecycle gates;
- a limited NIST, ISO, and SOC readiness crosswalk;
- a responsible-AI verification log;
- one integrated Python and Streamlit Signal Security Gateway Lab;
- a fixed library of synthetic support-ticket and provider-response scenarios;
- automated security tests and a least-privilege GitHub Actions workflow;
- a limited Amazon Bedrock Guardrails lab using the same synthetic cases;
- sanitized evidence mapping risks to safeguards, test results, and release gates; and
- a public GitHub repository and synthetic-only Streamlit demonstration.

### Portfolio validation boundary

The working prototype implements only the security checkpoint surrounding the proposed TP-AI-01 request and response. It does not implement the existing LindenArc ticket system, authentication, Aurora database, payment workflow, or full AWS runtime.

The public Streamlit application presents fixed, reviewed synthetic scenarios. It does not accept unrestricted visitor text or file uploads, contact a real AI provider, store customer tickets, or contain AWS credentials. The provider adapter targets the reserved fictional host `tp-ai-01.invalid`, uses only a local mock HTTP transport, and has no live-network fallback. When the interface reports that the provider was called, the application constructed an HTTP API request and routed it through that local transport; no external TP-AI-01 network request occurred.

The separate AWS lab creates and evaluates a real Amazon Bedrock Guardrail through `ApplyGuardrail` using synthetic text. It does not invoke a foundation model or deploy the reference VPC, PrivateLink endpoint, Network Firewall, NAT Gateway, Lambda functions, or external-model integration. Results prove only the tested guardrail configuration and cases.

## 8. Explicit exclusions

This project does not include:

- building a complete production SaaS application;
- processing real customer, employer, or school data;
- accepting unrestricted public text or uploads in the portfolio demonstration;
- calling a live TP-AI-01 service or running a real language-model inference;
- deploying the complete AWS reference architecture or payment path;
- conducting a real audit or penetration test;
- claiming NIST, ISO, SOC 2, PCI DSS, or other compliance;
- claiming certification or production-client experience; or
- allowing an AI system to make financial or security decisions.

## 9. Final decision produced by the case study

After the security analysis, the executive brief will recommend one of three outcomes:

1. approve the Signal launch;
2. approve the launch with required conditions; or
3. delay the launch until specified risks are addressed.

The recommendation will be based on documented risks, prototype tests, limited AWS-lab evidence, stated assumptions, and unresolved provider requirements—not selected in advance. A passing prototype or AWS test does not by itself authorize or prove production readiness.
