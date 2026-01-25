# META-ETERNITY (DSL Shape)

These are **Charter meta-rules** evaluated from the **current** charter during `ACTIVATE_CHARTER`
(constitution-swap safe). They are **non-exceptionable**.

This repo uses the same operator vocabulary as `policy_rule.schema.json` and the evaluation context roots
defined in `evaluation_context.schema.json`.

## Minimal rule set (conceptual)

- META-ETERNITY-001: `GATE-CHANGE-CONTROL` must exist in current charter and be allow_exception=false
- META-ETERNITY-002: `meta_rules[]` must be non-empty
- META-ETERNITY-003: forbid `"*"` in `/resources/charter/mode_policy/allowed_actions_all_modes`
- META-ETERNITY-004: require `/resources/trust_boundary_declaration/version` non-empty
- META-ETERNITY-005: if `/resources/change/touches_approval_policy == true`, then approvals must satisfy independence constraints
