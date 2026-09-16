# Amazon Bedrock Guardrails Lab Plan and Execution Record

**Project:** SecureLaunch AI  
**Owner and analyst:** Eniola Durojaiye  
**Status:** Executed and validated September 14-15, 2026  
**Data restriction:** Fixed synthetic data only

## Plain-language objective

This lab will configure one real Amazon Bedrock Guardrail and use it to inspect synthetic support-ticket text before that text could be sent to an external AI provider.

The lab will not call an AI model. It will call the Amazon Bedrock `ApplyGuardrail` application programming interface, or API, which can inspect text independently of a foundation model.

## Execution outcome

- Nine risk-based synthetic scenarios were executed against the Working draft.
- All nine produced their expected allow, mask, or block outcome.
- The tested configuration was frozen as immutable Version 1.
- Version 1 passed one console email-masking smoke test.
- Version 1 passed one direct API reproduction that masked a phone number and custom LindenArc account reference.
- No foundation model, external AI endpoint, real customer record, or usable credential was involved.
- The detailed, sanitized results are in [`evidence/aws/AWS_GUARDRAIL_VALIDATION_REPORT.md`](../evidence/aws/AWS_GUARDRAIL_VALIDATION_REPORT.md).

## Why this strengthens the portfolio

The Python gateway proves that LindenArc's own rules work in a repeatable local prototype. The AWS lab adds a real managed cloud-security control. The two layers serve different purposes:

| Layer | Main strength | Main limitation |
|---|---|---|
| Python gateway | Deterministic rules, approved fields, exact allow, mask, block, and fallback behavior | A prototype must be maintained and expanded by LindenArc |
| Amazon Bedrock Guardrail | Managed personally identifiable information detection and prompt-attack filtering | Some detection is probabilistic, AWS may update the underlying safeguards, and results still require testing |

The comparison will not assume that AWS must match every Python result. Differences will be documented as security findings.

## Locked AWS scope

- **Primary Region:** US East, N. Virginia (`us-east-1`)
- **Guardrail name:** `lindenarc-signal-boundary-v1`
- **Tier:** Standard, using the US guardrail profile if the console requires cross-Region inference
- **Content types:** Synthetic ticket input plus one simulated provider output
- **API:** `ApplyGuardrail` with `source` set to `INPUT` or `OUTPUT`
- **Foundation model:** None
- **External AI endpoint:** None
- **Real customer data:** Prohibited
- **Maximum live evaluations:** 25
- **Approved lab spend ceiling:** USD 1.00

Standard tier is selected because AWS recommends it for stronger content and prompt-attack safeguards. If cross-Region inference is enabled, the lab will use the US geography profile. Only synthetic data will be processed. A real European deployment would require its own Region and transfer assessment.

## Proposed guardrail controls

| Control | AWS action | Reason |
|---|---|---|
| Email address | Mask | The support problem may continue after unnecessary contact information is removed |
| Phone number | Mask | The support problem may continue after unnecessary contact information is removed |
| LindenArc account-reference pattern | Mask through custom regular expression | Internal identifiers should not reach the external AI when they are unnecessary |
| US Social Security number | Block | Identity data is prohibited from the AI route |
| Credit or debit card number | Block | Payment-card data is prohibited from the AI route |
| Credit or debit card CVV and expiry | Block | Payment-card authentication data is prohibited from the AI route |
| PIN | Block | Authentication data is prohibited from the AI route |
| US bank-account number | Block | Bank-account data is prohibited from the AI route |
| US bank-routing number | Block | Routing information is prohibited from the AI route |
| Password | Block | Credentials are prohibited from the AI route |
| AWS access key and secret key | Block | Cloud credentials are prohibited from the AI route |
| Prompt attack | Block at the strongest practical input setting | Ticket text must not override LindenArc's instructions |

Denied-topic filters, word filters, contextual grounding, and automated reasoning are excluded. They do not directly test the narrow pre-provider data-protection question.

## Executed test set

The final set was selected by risk and decision coverage. It avoids repetitive checks that would increase test volume without adding a distinct portfolio claim.

| Scenario | Security question | Expected and observed result |
|---|---|---|
| AWS-T01 | Does clean support text continue? | Allow; no action taken |
| AWS-T02 | Is an email removed without discarding the ticket? | Mask; email replaced |
| AWS-T03 | Do a built-in phone detector and custom account-reference regex work together? | Mask; both values replaced |
| AWS-T04 | Does a synthetic SSN stop the request? | Block; request stopped |
| AWS-T05 | Do synthetic card number, expiry, and CVV values stop the request? | Block; three detections stopped the request |
| AWS-T06 | Do nonfunctional example AWS credentials stop the request? | Block; access and secret keys detected |
| AWS-T07 | Does a direct prompt-manipulation attempt stop the request? | Block; High-confidence prompt attack detected |
| AWS-T08 | Can clearly quoted suspicious text avoid unnecessary blocking? | Allow; prompt attack not detected |
| AWS-T09 | Is sensitive data checked in simulated provider output? | Mask; output email replaced |

All outcomes above were observed in the AWS console. The nine scenarios tested the Working draft. Version 1 then passed a console smoke test and direct API reproduction.

## Cost boundary

AWS currently lists these Guardrails prices:

- Content filters: USD 0.15 per 1,000 text units
- Sensitive information filters: USD 0.10 per 1,000 text units
- Custom regular-expression sensitive-information filters: no charge
- Word filters: no charge

One text unit contains up to 1,000 characters. Each selected scenario is below that limit. At the 25-call maximum, content and sensitive-information checks would have a simple estimated usage charge of about USD 0.00625, excluding taxes or unexpected service changes. The USD 1.00 ceiling leaves a large safety margin.

Pricing must be checked again on the execution date. A billing alert is informative and may not stop spending immediately.

## Account and permission safeguards

1. Do not perform routine lab work with the AWS root user.
2. Enable multi-factor authentication on the root user and the lab identity.
3. Do not create or download long-term AWS access keys for this lab.
4. Use AWS CloudShell because it inherits the signed-in console identity and already includes the AWS command-line interface.
5. Give the lab identity only the permissions required to create, version, inspect, apply, and later remove the guardrail, plus the CloudShell permissions required to open the session.
6. Never place an AWS account number, credential, or secret in GitHub evidence.

AWS documents that a caller using Guardrails without a model needs `bedrock:ApplyGuardrail`, not foundation-model invocation permissions.

## Evidence to retain

For every AWS run, record:

- scenario ID;
- test date in Coordinated Universal Time;
- AWS Region;
- guardrail ID with account-specific portions removed from public evidence;
- immutable guardrail version;
- configured tier and geography profile;
- expected result;
- actual `action` result;
- masked or blocked result without publishing matched sensitive values;
- policy usage units;
- local Python decision;
- comparison finding;
- limitation or follow-up decision.

The public evidence package will include:

1. A configuration screenshot with account identifiers removed.
2. Sanitized expected-versus-actual results for the nine scenarios.
3. A sanitized Version 1 API response and Python-versus-AWS comparison table.
4. A short cost and cleanup record.
5. A statement that no model or real customer data was used.

## Important AWS limitation

AWS warns that original personally identifiable information can appear in some trace or logging fields even when the model-facing content is masked. For this reason:

- all lab values must remain synthetic;
- verbose traces will not be published without review;
- raw CloudShell output will be sanitized before GitHub publication;
- production logging would need separate data-protection controls.

This is an important reason to keep the LindenArc-owned gateway. A managed guardrail is an additional control, not permission to send the entire original ticket to AWS.

## Execution sequence and status

1. **Complete:** Secured the AWS account and configured a USD 1.00 billing alert.
2. **Complete:** Selected `us-east-1` and maintained the approved USD 1.00 lab ceiling.
3. **Complete:** Created the named Guardrail in the Bedrock console.
4. **Complete:** Configured masking, blocking, custom regex, and prompt-attack controls.
5. **Complete:** Executed nine risk-based scenarios against the Working draft.
6. **Complete:** Created immutable Version 1 after the draft results matched expectations.
7. **Complete:** Smoke-tested Version 1 in the console.
8. **Complete:** Reproduced Version 1 behavior through the direct `ApplyGuardrail` API.
9. **Complete:** Sanitized and organized the AWS evidence package.
10. **Pending project closeout:** Compare the managed AWS and deterministic Python results, check billing, and document the retention or cleanup decision.

## Official sources

- [Amazon Bedrock Guardrails overview](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [ApplyGuardrail without a foundation model](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html)
- [Sensitive information filters](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html)
- [Guardrails permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions.html)
- [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [AWS CloudShell overview](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html)
