# SecureLaunch AI Working-Record Index

## What this folder contains

The `work` folder preserves the complete security reasoning and decision history behind SecureLaunch AI. These files are intentionally more detailed than the main portfolio introduction because they allow a technical reviewer to trace conclusions back to architecture decisions, data flows, risks, safeguards, evidence, and release gates.

Start with the main [SecureLaunch AI overview](../README.md) if you want a shorter introduction.

## Recommended reading order

| Order | Document | Purpose | Status |
|---:|---|---|---|
| 1 | [Project roadmap](00_project_roadmap.md) | Defines the evidence-backed scope, phases, time boundaries, final technical product, and completion criteria | Current |
| 2 | [Scenario charter](01_scenario_charter.md) | Defines LindenArc, Signal, business goals, allowed behavior, prohibited behavior, actors, data, and assessment boundaries | Approved |
| 3 | [AWS architecture design brief](02_aws_architecture_design_brief.md) | Records the complete fictional AWS reference architecture, trust boundaries, numbered data flows, design decisions, and provider integrations | Approved reference design |
| 4 | [Architecture learning guide](02a_architecture_learning_guide.md) | Explains important AWS, AI, security, payment, and operations terminology in plain language | Learning companion |
| 5 | [Preliminary risk candidate log](02b_risk_candidate_log.md) | Preserves risks identified during architecture discussions before formal PASTA prioritization | Historical input |
| 6 | [Third-party provider register](02c_third_party_provider_register.md) | Separates AWS, the fictional AI provider, the fictional payment provider, and the local mock provider | Approved |
| 7 | [Data inventory and lifecycle](03_data_inventory_and_lifecycle.md) | Defines data classifications, locations, retention proposals, deletion realities, and reusable-knowledge controls | Approved and audited |
| 8 | [Seven-stage PASTA threat model](04_pasta_threat_model.md) | Documents objectives, technical scope, decomposition, threats, weaknesses, attack scenarios, risk prioritization, and the launch decision | Approved |
| 9 | [Risk register and control plan](05_risk_register_and_control_plan.md) | Converts PASTA findings into ten risks, safeguards, evidence requirements, release gates, and prototype requirements | Approved |

## Fast reading routes

### Understand the fictional company and feature

Read the scenario charter, then the architecture learning guide.

### Understand the risk treatment and evidence limits

Read the risk register and control plan, especially the risk heatmaps, safeguards, evidence register, and the boundaries of what the prototype can establish.

### Defend the analysis in a technical interview

Read the architecture design, data inventory, PASTA threat model, and risk/control plan in that order. Use the learning guide whenever a technical term is unfamiliar.

### Trace one decision from beginning to end

Follow identifiers in this order:

`Objective → DATA/DF/TB → Threat → Weakness → Attack scenario → Risk → Safeguard → Evidence → Release gate`

Example:

`SO-02 → DATA-06/DF-19/TB-11 → T-03 → W-04/W-05 → AS-02 → R-03 → SG-06 → EV-07 → RG-03`

## Why some documents are long

The architecture brief and PASTA model are detailed working evidence, not quick marketing documents. Their length preserves:

- decisions Eniola reviewed or corrected;
- assumptions and explicit exclusions;
- numbered data flows and trust boundaries;
- third-party risks and evidence gaps;
- historical versus current risk reasoning; and
- honest limits on what the portfolio can prove.

Short public summaries and polished exports belong in `outputs/`; they should link back to these records instead of deleting the underlying reasoning.

## Local viewing

Use Visual Studio Code's Markdown preview for the intended formatting:

1. Open a `.md` file.
2. Press **Ctrl+Shift+V**.

Notepad displays raw Markdown syntax and will not render tables or heading styles.
