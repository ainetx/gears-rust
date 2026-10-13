# CODE Rules (FEATURE-led)

**Artifact**: CODE
**Kit**: gears

**Dependencies**:
- the source FEATURE artifact — the implementation contract
- `{codebase_checklist}` — code review criteria, review-only

---

## Prerequisites

### Load Dependencies
- [ ] Load the source FEATURE and the DESIGN, ADR, PRD, and UPSTREAM_REQS IDs it links; they are the implementation contract
- [ ] Resolve the source FEATURE location from `@cpt-*` markers or the request; stop and ask when it cannot be resolved
- [ ] Determine the traceability mode from the FEATURE or `artifacts.toml` (FULL or DOCS-ONLY)
- [ ] Leave `{codebase_checklist}` to the review stage; authoring does not load it
- [ ] Run `{ensure_dna_script}` before relying on `{dna_rust}`/`{dna_rest}` content

---

## Requirements

### Structural
- [ ] Follow the gear layout in `{toolkit_unified_system}/02_gear_layout_and_sdk_pattern.md`: SDK crate for public contracts, gear crate for domain, API, and infrastructure. Study `examples/toolkit/users-info/` for the layer being touched (SDK crate: `examples/toolkit/users-info/users-info-sdk/src/`; gear crate: `examples/toolkit/users-info/users-info/src/`) as the canonical reference implementation
- [ ] Route to the matching `{toolkit_unified_system}` chapter for the surface being touched: `03_clienthub_and_plugins.md` for ClientHub/inter-gear clients/plugins, `04_rest_operation_builder.md` for REST endpoints/OperationBuilder/SSE, `05_errors_rfc9457.md` for error types/Problem/`From` impls, `06_authn_authz_secure_orm.md` for DB entities/SecureORM/AuthZ, `07_odata_pagination_select_filter.md` for OData/pagination, `08_lifecycle_stateful_tasks.md` for lifecycle/background tasks, `09_oop_grpc_sdk_pattern.md` for out-of-process gears/gRPC, `12_unit_testing.md`/`13_e2e_testing.md` for test layout
- [ ] Follow cross-gear dependency rules, `SecurityContext` propagation, and middleware boundaries from `{gears_md}`
- [ ] Follow `{guidelines_security}`, `{gears_security}`, and `{guidelines_dependencies}`
- [ ] Follow repo Rust conventions from `{dna_rust}`
- [ ] If the gear exposes HTTP/REST or SSE endpoints, follow `{dna_rest}` for status codes, versioning, batching, and querying conventions
- [ ] Follow `{testing_policy}` for test strategy, coverage requirements, and which checks must be green locally before a PR
- [ ] Add `@cpt-begin` and `@cpt-end` markers for implemented CDSL IDs when traceability mode is FULL
- [ ] Generate marker IDs only from existing FEATURE CDSL IDs; never invent implementation-only CPT IDs
- [ ] Keep markers minimal, correctly nested, and attached to the code that realizes the referenced behavior

### Semantic
- [ ] Implement every in-scope flow step, algorithm requirement, state transition, and definition-of-done item
- [ ] Preserve PRD coverage outcomes and DESIGN principles, constraints, components, sequences, data contracts, and security requirements in code behavior
- [ ] Preserve SDK-first public contracts (the `<gear>-sdk` crate is the public API), domain/API/infrastructure separation, `SecureConn`+`AccessScope` for all DB access (no raw connections), AuthZ via the `PolicyEnforcer` PEP pattern (never construct `AccessScope` manually), `OperationBuilder` for all REST routes with `.authenticated()` and `.standard_errors()`, `#[domain_model]` on every non-module-private domain struct/enum (DE0309 lint; strictly module-private helpers are exempt), and safe wire errors unless the source FEATURE or DESIGN documents an approved deviation
- [ ] Never use `unwrap()`/`expect()` in gear code outside tests; use proper `Result` types
- [ ] Record review evidence for work touching registry, autodetect, or ignore matching, privilege boundaries, Secure ORM, SecurityContext, secrets, FIPS behavior (see `{fips_requirements}`), or other security-boundary logic: the touched guardrail or deviation, rationale, owner, and validation performed
- [ ] Add compile-fail tests when the code exposes compile-time guarantees (macro diagnostics, generated code contracts, type-state APIs, security or type-system invariants) and a compile-fail harness exists; otherwise state why the gate does not apply
- [ ] Never broaden scope beyond the source FEATURE without an explicit upstream artifact change

---

## Tasks

### Content Creation
- [ ] Split the FEATURE into implementation slices from its flow, algorithm, state, and definition-of-done IDs; each slice names the IDs it implements
- [ ] Order slices by dependency and user-observable behavior, each independently testable
- [ ] Implement one slice at a time with TDD: failing test first, smallest passing code, then refactor
- [ ] Preserve existing behavior outside the current slice and the requested FEATURE scope

### IDs and Structure
- [ ] Mark the FEATURE checkboxes of the CDSL IDs a slice implements as `[x]` in the author stage, once the slice's tests pass; `cfs validate` reports an implemented but unchecked ID as an error
- [ ] Leave inspection-only definition-of-done items unchecked until the close stage confirms them
- [ ] Preserve existing stable IDs and markers; move markers only with the code they describe
- [ ] Never introduce orphan, duplicate, stale, or speculative `@cpt-*` markers

---

## Validation

### Structural
- [ ] `make gear-ci GEAR=<gear>` (fmt, clippy with the workspace lint set, tests) and `make dylint` pass
- [ ] `cfs validate` reports zero errors for the gear's code traceability

### Semantic
- [ ] No test, lint, build, or traceability failure is left unresolved when the command is available

---

## Error Handling

### Recovery Options
- [ ] If traceability validation fails, fix the marker placement or ID against the FEATURE rather than editing the FEATURE to match the code
- [ ] If a slice cannot be finished within the FEATURE scope, stop and propose an upstream FEATURE change

---

## Next Steps

### Options
- [ ] Commit the slice through `cf-git-commit`
- [ ] Prepare the pull request review through `cf-gears-pr-review`
