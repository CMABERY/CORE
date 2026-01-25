# TRUST BOUNDARY (Template)

CPO enforces **process integrity** inside its trust boundary. It does not guarantee physical reality.

This document is a **canonical declaration** of assumptions and required assurances.

## Runtime Integrity
- Status: [ASSUMED | ATTESTED | UNKNOWN]
- Evidence: (artifact digest / attestation / link)
- If false: Action logs may be fabricated.

## Database Integrity
- Status: [ASSUMED | ATTESTED | UNKNOWN]
- Evidence: (DB configuration audit / access control proof)
- If false: Append-only guarantees are unverified.

## Deployment Integrity
- Status: [ASSUMED | ATTESTED | UNKNOWN]
- Evidence: (SLSA provenance / signed images / CI evidence)
- If false: running binary may not match audited source.

## Oracle / External Evidence Sources
Registered sources:
- name:
  trust basis:
  verification method:

Conflict policy:
- how disagreements are resolved (arbitration, quorum, external audit)

## Required External Assurances (recommended)
- Signed builds + provenance (SLSA-style or equivalent)
- Signed container/image digests
- Runtime attestation when stakes justify (TPM/enclave/measured boot)
- Independent verification of deployed digest vs audited digest

## Failure Modes CPO cannot prevent
- Compromised runtime forging logs
- Compromised DB bypassing triggers/roles
- Compromised deployment pipeline swapping binaries

## Bottom line
CPO makes action legible and governance enforceable **within this boundary**.
