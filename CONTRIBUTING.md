# Contributing

This repository is intentionally small. Changes should preserve:
- Determinism
- Append-only semantics where applicable
- Dependency-light execution

## Development
- Python >= 3.10
- Standard library only (unless explicitly approved)

## Validation
From `codex_like_mvp_project/`:

```bash
python -m tools.test_merge3
python -m tools.test_redaction
python -m tools.test_secret_guardrails
python -m codex_like_mvp.client.mvp_cli demo
```

## Pull requests
- Prefer small diffs.
- Update docs if behavior or usage changes.
- Keep any new invariants explicit and testable.
