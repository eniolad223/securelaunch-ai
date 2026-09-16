# Reviewer showcase: design and source notes

## Purpose

Present Eniola Durojaiye's security reasoning, Python controls, AWS validation, and business judgment to a reviewer who has no prior project context. The first view explains the problem, fictional company, proposed support product, external provider, and analyst contribution. The other views reveal evidence on demand.

## Decisions applied

- Five short views: Overview, Try the gateway, AWS validation, Risk & governance, My approach.
- Light lavender, legible sans-serif typography, visible navigation states, restrained motion, and responsive layouts.
- A working control illustration on the opening view, followed by an explicit choose/run/compare path.
- Actual Python execution supplies local decisions. Changing scenarios clears the old result and receipt.
- The AWS view presents recorded cloud evidence and distinguishes draft validation from Version 1 confirmation.
- Decisions connect a risk to the chosen control, business value, and supporting evidence.
- Detailed traces, legal mappings, source artifacts, and AI-assistance disclosure are available without dominating the overview.
- Signal is defined as the fictional company's support product. Its hosted AI provider is external. Later narration uses ordinary descriptions where possible.

## Design research

Linear's documented interface refresh emphasizes scanning, consistent navigation, and keeping attention on the task. The showcase applies those principles with quiet navigation and one primary content view. [Linear: A calmer interface for a product in motion](https://linear.app/now/behind-the-latest-design-refresh).

Tines presents workflow execution through an interactive storyboard with inspection of data at individual steps. The showcase uses a much smaller version of that learning pattern: choose a ticket, execute the gateway, compare the permitted data, and inspect the trace. [Tines: Introduction to the storyboard](https://explained.tines.com/en/articles/12709994-introduction-to-the-storyboard).

Wiz offers an interactive guided tour of its security platform. The relevant pattern here is a directed path through an unfamiliar security concept, applied to a bounded portfolio rather than a commercial platform. [Wiz platform tour](https://www.wiz.io/platform/ai-powered-wiz).

Implementation uses supported Streamlit containers and buttons, with styles attached to explicit container keys. [Streamlit container documentation](https://docs.streamlit.io/develop/api-reference/layout/st.container), [button documentation](https://docs.streamlit.io/develop/api-reference/widgets/st.button).

## Framework and legal references

The presentation offers selected relevance mappings. It does not claim a completed audit, certification, or comprehensive implementation.

- **NIST CSF 2.0:** data inventory and flows, risk assessment and response, data protection, and supplier requirements. References include ID.AM-03/07, ID.RA-05/06, PR.DS, and GV.SC-05/06. [Official CSF 2.0](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf).
- **NIST AI RMF:** Govern, Map, Measure, and Manage organize the AI-specific risk discussion. It is a voluntary framework. [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework).
- **GDPR:** Articles 5(1)(c), 25, 28, and 32 connect minimization, protection by design, processor obligations, and security to the case study where legally applicable. The prototype does not resolve lawful basis, cross-border transfers, retention, or the full set of legal duties. [Official GDPR text](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng).
- **FTC GLBA Safeguards Rule:** relevance depends on covered activities, customer relationships, and service-provider obligations. Being described as fintech does not establish direct coverage. The presentation connects risk assessment, safeguards, provider oversight, and testing to the case study. [FTC business guidance](https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know).

Sources reviewed September 15, 2026. These are portfolio mappings, not legal advice or a finding about a real company.

## Run and verify

Run the reviewer application with:

```text
streamlit run app_redesign.py
```

The original gateway is imported from `src/securelaunch`. Presentation copy and styling are in `presentation/`. The prior image-based hero is no longer loaded by the application.

```text
pytest -q
python work/verify_reviewer_interface.py
```

The first command verifies the 43 existing backend security tests. The second exercises the opening controls, 15 scenario/result transitions, all nine AWS views, four decision views, four framework views, the launch recommendation, five approach views, and return navigation. Visual review separately checks layout, navigation contrast, and responsive behavior.
