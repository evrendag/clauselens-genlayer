# Test results

Last local verification: 2026-09-09

Environment:

- Python 3.12.14
- genlayer-test 0.29.2
- pytest 9.1.1
- GenVM universal 0.2.12

Command:

```bash
python3 -m pytest tests/ -v
```

Result:

```text
6 passed in 0.16s
```

Covered behavior:

- Initial policy registration
- Material revision enters `REVIEW_REQUIRED`
- Explicit approval activates a material revision
- Non-material revision activates automatically
- Non-owner proposal reverts
- Independent validator disagreement returns false

These are Direct Mode tests with mocked LLM outputs. A finalized Studio or
testnet deployment and transaction should be added as public submission evidence.

