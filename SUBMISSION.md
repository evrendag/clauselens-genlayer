# GenLayer contribution submission

## Category

Builder / Intelligent Contracts

## Title

ClauseLens: Versioned Semantic Policy Registry with Material-Change Gating

## Notes / Description

I built ClauseLens, a reusable GenLayer Intelligent Contract primitive for
protocols, DAOs, marketplaces, and autonomous services that manage
human-readable policies. It stores versioned revisions with parent lineage and
uses a custom `run_nondet_unsafe` leader/validator flow to classify semantic
changes. Validators independently repeat the analysis; verdict and primary risk
category must match exactly, while severity must remain within 15 points and the
same risk band. Deterministic cross-field checks prevent malformed or internally
inconsistent results from changing state.

The consensus result drives a fail-closed lifecycle rather than simply returning
LLM text: non-material revisions may activate automatically, while material
revisions enter `REVIEW_REQUIRED` and need a separate owner approval transaction.
Stale material proposals cannot replace a newer active version. The repository
documents the state machine, consensus rationale, prompt-injection boundary,
reuse patterns, trade-offs, Studio workflow, and direct-mode tests covering
access control, transitions, and validator disagreement.

## Evidence to attach

1. Public GitHub repository URL.
2. GenLayer deployed contract or finalized deployment transaction URL.
3. Finalized `propose_revision` transaction showing `REVIEW_REQUIRED`.
4. Optional approval transaction showing explicit version activation.

Do not submit until the repository is public and the deployment plus at least
one consensus transaction has finalized successfully.

