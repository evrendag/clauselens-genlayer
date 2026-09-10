# Architecture and integration notes

ClauseLens separates deterministic registry logic, nondeterministic semantic
analysis, and independent consensus validation.

## Reuse patterns

- A DAO can replace owner approval with a governance vote.
- A marketplace can warn users when a material revision is staged.
- An autonomous agent can accept wording maintenance while routing
  rights-changing edits to a human.
- A subscription protocol can specialize the categories and thresholds.

## Why the summary is not compared

Two validators can reach the same decision using different words. Exact summary
matching would turn harmless phrasing variation into consensus failure. The
contract compares verdict and category exactly, then applies numeric tolerance
plus a shared severity-band requirement.

## Known trade-offs

- Exact category matching is conservative for multi-category revisions.
- Full policy text improves auditability but increases storage cost.
- The reference implementation uses one owner; integrations can use multisig,
  DAO, or cross-contract authorization.
- Semantic analysis remains model-dependent, so material changes require a
  separate explicit approval transaction.

