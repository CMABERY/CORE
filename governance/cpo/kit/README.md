# CPO Starter Kit (Polished)

This repository is a **portable governance kernel**: contracts, templates, and validators for the **Capability Persistence Overlay (CPO)** protocol.

It includes:
- **CPO Contracts** (`cpo-contracts@0.1.0`): canonical artifact schemas + action contract
- **Evidence Pack** (`evidence-pack@1.0.0`): export bundle schemas (auditable, forwardable)
- **SUBSTRATE registry**: non-removable “physics” checks (code/DB enforced)
- **META-ETERNITY**: minimal constitutional constraints (prevents “vote CPO out”)
- **TRUST-BOUNDARY template**: explicit assumptions and required external assurances
- **Examples** + **one-command validators**

> CPO doesn’t eliminate trust or harm—it makes them explicit, time-bounded, auditable, and therefore governable.

## Quickstart

### 1) Validate the example artifacts
```bash
python scripts/validate_contracts.py
```

### 2) Validate an Evidence Pack directory or zip
```bash
python scripts/validate_evidence_pack.py examples/evidence-pack_example
python scripts/verify_evidence_pack_integrity.py examples/evidence-pack_example.zip
```

## What this is NOT
- Not a runtime service implementation.
- Not a compliance claim.
- Not a replacement for external attestation (see `TRUST-BOUNDARY.md`).

## Directory layout
- `schemas/` — JSON Schemas for both protocol families
- `substrate/` — SUBSTRATE registry + META-ETERNITY rules + TRUST-BOUNDARY template
- `examples/` — minimal valid fixtures
- `scripts/` — validators (schema + integrity)

## License
Use internally; add your org license as needed.

## JSON Canonicalization (RFC 8785 JCS)

This kit includes a reference JCS implementation:

```bash
node scripts/jcs.js < some.json > canonical.json
node scripts/jcs_test.js
```

Notes:
- Non-finite numbers (NaN/Infinity) are rejected (not valid JSON).
- -0 is canonicalized to 0.
