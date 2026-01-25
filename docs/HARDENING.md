# Repository Hardening Notes

This file documents the baseline hygiene added before introducing new subsystems.

## Added guardrails
- UTF-8 enforcement check (`scripts/check_utf8.py`)
- `.editorconfig` + `.gitattributes` (LF normalization, consistent formatting)
- `.gitignore` includes generated `state/transactions` output
- GitHub Actions workflow `core-python.yml` runs:
  - compileall
  - stdlib self-tests
  - demo (review-only) and validators

## Out-of-repo settings to apply (GitHub)
- Protect `main` branch
- Require PR reviews + CODEOWNERS
- Require CI checks (`core-python`) to pass
- Disable force-push to protected branches
