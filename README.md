# ClauseLens — Semantic Policy Registry for GenLayer

ClauseLens is a reusable Intelligent Contract primitive for protocols, DAOs,
marketplaces, subscription products, and autonomous services that keep
human-readable rules on-chain.

It maintains a versioned policy registry and uses GenLayer consensus to detect
whether a proposed revision materially changes user rights or obligations. A
non-material revision can become active automatically. A material revision is
placed in `REVIEW_REQUIRED` and cannot replace the active policy until a separate
human approval transaction is submitted.

This is more than an "AI decides X" wrapper: the nondeterministic assessment
controls a documented state machine, validators independently repeat the
semantic analysis, and deterministic checks limit which consensus results can
affect contract state.

## Why this primitive matters

Byte comparison can prove that a policy changed, but not whether its meaning
changed. ClauseLens turns semantic change detection into a composable on-chain
gate. A frontend or another contract can read the active version, inspect a
revision's consensus-backed risk classification, and require human review for
high-impact transitions.

## State model

Every `PolicyRevision` stores its parent and text, an author change note, the
consensus verdict/severity/category/summary, lifecycle status, and proposer.

```text
NON_MATERIAL proposal: ACTIVE; previous version becomes SUPERSEDED
MATERIAL proposal: REVIEW_REQUIRED; then ACTIVE or REJECTED
Stale material proposal: cannot activate if its parent is no longer active
```

## Consensus design

The leader analyzes the active and proposed policy and returns structured JSON.
Each validator independently runs the same semantic comparison. Validation is
substantive rather than format-only:

1. `verdict` and primary risk `category` must match exactly.
2. Severity may differ by at most 15 points.
3. Both scores must remain in the same band: 0–39, 40–69, or 70–100.
4. Cross-field checks reject impossible combinations such as
   `NON_MATERIAL` with severity 80.

The explanation is stored but not compared byte-for-byte because equivalent LLM
explanations naturally differ in wording.

## Safety properties

- Owner-only proposals and reviews.
- Input bounds and identical-revision rejection before LLM execution.
- Fail-closed human review for material changes.
- Parent-lineage checks prevent stale activation.
- Submitted text is delimited and treated as untrusted evidence.
- Validator failures disagree instead of accepting a leader-only answer.

## Public methods

- `propose_revision(revised_text, change_note)`
- `review_material_revision(revision_id, approve)`
- `get_active_policy()`
- `get_revision(revision_id)`
- `get_revision_count()`

## Deploy in GenLayer Studio

1. Create a contract and paste `contract.py`.
2. Deploy with a document name and initial policy of 20–12,000 characters.
3. Call `propose_revision` with a sample from `TEST_CASES.md`.
4. Wait for consensus and inspect the new revision.
5. If material, call `review_material_revision(id, true)` and verify that the
   active version advances only after this second transaction.
6. Record the repository, deployed contract, and finalized transaction URLs.

## Tests

The tests cover initialization, access control, automatic activation, material
review gating, and validator disagreement:

```bash
pip install genlayer-test pytest
pytest tests/ -v
```

ClauseLens is an experimental developer primitive, not legal advice or a
production legal-review system. Integrators should tune governance, thresholds,
categories, and limits for their own threat model.

## License

MIT

