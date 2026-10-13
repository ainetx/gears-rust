---
cf: true
type: workflow
name: cf-gears-gear-creator
description: Invoke when the user wants to create a new ToolKit gear from scratch, or add a feature to an existing one (REST endpoints, DB entities, OData filtering, plugins, lifecycle/background tasks, SSE events, error types) — e.g. "create a new gear", "scaffold a gear", "add a REST endpoint to <gear>", "/cf-gears-gear-creator"
version: 1.0
purpose: Thin Studio-kit wrapper over the gear-creator skill, which owns the full DDD-light scaffold/edit workflow (SDK pattern, contract/API/domain/infra layers, OperationBuilder, SecureORM, ClientHub, error handling, testing).
---

# Gear Creator Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/studio/SKILL.md` FIRST.

**Type**: Authoring
**Role**: Implementer
**Output**: new or edited gear crate(s) under `gears/<gear-name>/` (and `gears/<gear-name>-sdk/` when an SDK is needed), wired into the workspace and the example server.

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Create a brand-new gear | **this workflow** | "create a new gear", "scaffold a file-storage gear" |
| Add a feature to an existing gear (endpoint, entity, OData, plugin, lifecycle, SSE, error) | **this workflow** | "add a REST endpoint to settings-service" |
| Implement from an already-written FEATURE/DESIGN artifact with `@cpt-*` traceability | **`cf-gears-implement`** / **`cf-gears-coding`** | "implement FEATURE 0003 for file-storage" |

This workflow is for the layer-by-layer *mechanics* of standing up or extending a gear
(crate layout, SDK, OperationBuilder, SecureORM, ClientHub). `cf-gears-implement`/
`cf-gears-coding` are for realizing an already-authored FEATURE/DESIGN contract with
Constructor Studio traceability. Use this one first when there's no FEATURE/DESIGN yet, or
when the ask is purely structural (a new endpoint, entity, or plugin) rather than
traceability-bound. The two are complementary, not competing: a gear scaffolded here can
still gain `@cpt-*` traceability later through `cf-gears-doc-feature` + `cf-gears-implement`.

---

## Overview

Delegates entirely to the `gear-creator` skill, which owns:
- **Create a new gear**: requirements gathering → design (document routing table, checklist
  from `{toolkit_unified_system}/10_checklists_and_templates.md`) → scaffold (SDK crate,
  gear crate, contract/domain/infra/API layers in dependency order) → wire and register
  (workspace `Cargo.toml`, `apps/cf-gears-example-server`, ClientHub, feature flags) →
  verify.
- **Edit an existing gear**: understand scope → load only the relevant
  `{toolkit_unified_system}` chapter(s) → study the existing code against
  `examples/toolkit/users-info/` → implement under the DDD-light layer rules → verify.
- The key invariants it enforces either way (SDK-first public API, `SecureConn`+
  `AccessScope` for DB access, `OperationBuilder` with `.authenticated()`/
  `.standard_errors()`, `#[domain_model]` on domain types, no `unwrap()`/`expect()`,
  `PolicyEnforcer` PEP for AuthZ) are the same ones `{codebase_rules}` now names
  explicitly — this workflow and `cf-gears-coding`/`cf-gears-implement` agree on them
  rather than each inventing its own list.

## Steps

## Step 1: Resolve intent
Is this a new gear or an edit to an existing one? If unclear, ask (gear name, purpose,
capabilities needed — `db`/`rest`/`stateful` — dependencies on other gears, whether an SDK
is needed for a new gear; or what's changing for an edit).

## Step 2: Run the gear-creator skill
Invoke the `gear-creator` skill with the resolved intent. It drives its own
requirements/design/scaffold/wire/verify (new gear) or
understand-scope/load-docs/study/implement/verify (edit) sequence — this workflow does not
re-implement any of it.

### Fallback — skill not installed
If `gear-creator` isn't available in this session (e.g. a standalone kit install without
`.claude/skills/gear-creator`), follow `{toolkit_unified_system}`'s own document-routing
guidance directly: `01_overview.md` for the golden path, `02_gear_layout_and_sdk_pattern.md`
for structure, then the chapter matching the capability being added (see
`{codebase_rules}`'s routing list), and `examples/toolkit/users-info/` as the reference
implementation.

## Step 3: Verify
`cargo build -p <gear-crate>`, `cargo clippy -p <gear-crate>`, `make dylint`, `cargo test -p
<gear-crate>` (same as the skill's own Verify step). For a new gear, also confirm it's
registered in the workspace `Cargo.toml` and `apps/cf-gears-example-server/src/main.rs`.

## Step 4: Present results
Summarize what was scaffolded or changed, which layers were touched, and whether the gear
needs FEATURE-level traceability next (point at `cf-gears-doc-feature` when the request
came from a design/decomposition rather than ad hoc).

---

## Validation Criteria

- [ ] Intent resolved (new gear vs. edit) before any file was written
- [ ] The underlying skill was invoked, or the `{toolkit_unified_system}` fallback was
  applied when it wasn't available
- [ ] Key invariants held (SDK-first API, `SecureConn`+`AccessScope`, `OperationBuilder`
  `.authenticated()`/`.standard_errors()`, `#[domain_model]`, no `unwrap()`/`expect()`,
  `PolicyEnforcer` PEP) or an approved deviation is documented
- [ ] `cargo build`/`cargo clippy`/`make dylint`/`cargo test` pass for the touched crate(s)
- [ ] A new gear is registered in the workspace and the example server
- [ ] Results presented to the user, including whether FEATURE traceability is a sensible
  next step

---

## Next Steps

### Options
- [ ] Add FEATURE traceability through `cf-gears-doc-feature` + `cf-gears-implement`
- [ ] Prepare the pull request review through `cf-gears-pr-review`
- [ ] Commit the change through `cf-git-commit`
