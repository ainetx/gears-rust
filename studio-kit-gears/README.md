# CF/Gears Kit (Constructor Studio-compatible)

**ID**: `gears`
**Format**: `Constructor Studio` (targets Studio v1.8.0 or later — the FEATURE artifact's
CDSL clarity findings are declared warnings only from v1.8.0 onward; v1.7.0 reports them
as errors, see `artifacts/FEATURE/rules.md`)
**Purpose**: Own CF/Gears’s SDLC document templates, examples, and expert checklists (`artifacts/<KIND>/`), and the Studio workflows that author, validate, and review gear documents and code.

## Artifact kinds

| Kind | `{template}` | `{rules}` | `{checklist}` | `{example}` |
|------|----------|-------|-----------|---------|
| UPSTREAM_REQS | `artifacts/UPSTREAM_REQS/template.md` | `artifacts/UPSTREAM_REQS/rules.md` | `artifacts/UPSTREAM_REQS/checklist.md` | `artifacts/UPSTREAM_REQS/examples` |
| PRD | `artifacts/PRD/template.md` | `artifacts/PRD/rules.md` | `artifacts/PRD/checklist.md` | `artifacts/PRD/examples` |
| ADR | `artifacts/ADR/template.md` | `artifacts/ADR/rules.md` | `artifacts/ADR/checklist.md` | `artifacts/ADR/examples` |
| DESIGN | `artifacts/DESIGN/template.md` | `artifacts/DESIGN/rules.md` | `artifacts/DESIGN/checklist.md` | `artifacts/DESIGN/examples` |
| DECOMPOSITION | `artifacts/DECOMPOSITION/template.md` | `artifacts/DECOMPOSITION/rules.md` | `artifacts/DECOMPOSITION/checklist.md` | `artifacts/DECOMPOSITION/examples` |
| FEATURE | `artifacts/FEATURE/template.md` | `artifacts/FEATURE/rules.md` | `artifacts/FEATURE/checklist.md` | `artifacts/FEATURE/examples` |
| CODE | — | `codebase/rules.md` + `codebase/design-led-rules.md` | `codebase/checklist.md` | — |

Template = structure/sections (authoring). Rules = required content (authoring + part of
review). Checklist = review criteria (review-only; authoring never loads it). Example =
reference implementation (review-only).

## How a preset runs

Every document preset (`cf-gears-doc-*`, `cf-gears-decompose`) and code preset
(`cf-gears-implement`, `cf-gears-coding`) is a stage router over the Studio
thin skills. One invocation runs one stage, then pins the same preset as the
suggested next action with the next stage:

- documents: author (`cf-documenting-gen`) → validate (`cf-documenting-ci`) →
  review (`cf-documenting-review`) → fix (`cf-documenting-fix`) → close
- code: tests (`cf-coding-tests`) → author (`cf-coding-gen`) → validate
  (`cf-coding-ci`) → review (`cf-coding-review`) → fix (`cf-coding-fix`) → close

The kit supplies the `phase-plan`, `phase-dod`, and `acceptance-criteria`
prerequisites the Studio skills require from `plans/doc-phase.md` and
`plans/code-phase.md`, so a single-artifact run needs no separate planning
session. The shared routing lives in `modules/doc-stage-router.md` and
`modules/code-stage-router.md`. Close checks the definition of done and offers
the next artifact of the chain.

Template and rules changes apply to newly authored documents only. Existing
gear documents keep their structure until someone revises them; the backlog
for bringing them in line (for example the frontmatter `description`) is
tracked separately in the kit improvements backlog.

## Repo-wide convention docs and standalone installs

The CODE and doc-artifact rules cite repo-wide convention docs that live outside this kit
folder by `{variable}` name, never by a hardcoded path, since the kit never assumes where
its resources end up on disk. `.cf-studio-kit.toml` declares each as a kit resource so a
kit installed outside the `gears-rust` checkout gets its own bundled copy, and
`{cfs_cmd} resolve-vars` resolves the name to wherever that install actually placed it.
`guidelines/DNA` is additionally a git submodule in `gears-rust` itself —
`{ensure_dna_script}` initializes it when working inside a `gears-rust` checkout that
hasn't fetched it yet; a standalone install has no submodule to init at all and instead
relies entirely on the bundled copy from install time.

### Which guide is used where

| Guide (`{variable}`) | Resolves to | Used by | Stage |
|---|---|---|---|
| `{gears_md}` | `docs/GEARS.md` | CODE, DESIGN, PRD, UPSTREAM_REQS, DECOMPOSITION rules | Authoring |
| `{toolkit_unified_system}` | `docs/toolkit_unified_system/` | CODE, DESIGN rules; `plans/code-phase.md` | Authoring |
| `{guidelines_security}` | `guidelines/SECURITY.md` | CODE rules; `artifacts/ISO_29148.md` | Authoring |
| `{gears_security}` | `docs/security/SECURITY.md` | CODE, DESIGN rules | Authoring |
| `{guidelines_dependencies}` | `guidelines/DEPENDENCIES.md` | CODE rules | Authoring |
| `{dna_rust}` | `guidelines/DNA/languages/RUST.md` | CODE rules | Authoring |
| `{dna_rest}` | `guidelines/DNA/REST/` | CODE rules (REST/SSE gears only) | Authoring |
| `{ensure_dna_script}` | `scripts/ensure-dna.py` | CODE rules (prerequisite) | Authoring |
| `{testing_policy}` | `docs/TESTING.md` | CODE, DESIGN rules | Authoring |
| `{fips_requirements}` | `docs/security/fips/` | CODE rules/checklist, DESIGN, PRD rules (FIPS-touching work only) | Both |
| `{guidelines_gts}` | `guidelines/GTS.md` | CODE, DESIGN checklist/rules | Review |
| `{toolkit_pr_review_docs}` | `docs/toolkit-pr-review/` | CODE checklist; `workflows/toolkit-review.md` (fallback for the `toolkit-pr-review` skill) | Review |
| `{architecture_manifest}` | `docs/ARCHITECTURE_MANIFEST.md` | PRD rules/checklist/template, DESIGN checklist, `artifacts/ISO_29148.md` | Both |
| `{iso_29148}` | `artifacts/ISO_29148.md` | PRD, UPSTREAM_REQS rules | Authoring |
| `{guidelines_readme}` | `guidelines/README.md` | PRD rules (Operational Concept, NFR sections) — indexes the other `guidelines/*` variables | Authoring |
| `{repo_adrs}` | `docs/adrs/` | ADR, DESIGN rules | Authoring |
| `{repo_arch}` | `docs/arch/` | ADR, PRD, DESIGN rules | Authoring |
| `{repo_playbook}` | `docs/REPO_PLAYBOOK.md` | PRD, UPSTREAM_REQS, DESIGN, DECOMPOSITION rules | Authoring |

## Workflows

| Preset | `{variable}` | Does |
|---|---|---|
| `cf-gears-doc-upstream-reqs` | `{workflow_doc_upstream_reqs}` | author/review UPSTREAM_REQS |
| `cf-gears-doc-prd` | `{workflow_doc_prd}` | author/review PRD |
| `cf-gears-doc-adr` | `{workflow_doc_adr}` | author/review ADR |
| `cf-gears-doc-design` | `{workflow_doc_design}` | author/review DESIGN |
| `cf-gears-decompose` | `{workflow_decompose}` | author/review DECOMPOSITION |
| `cf-gears-doc-feature` | `{workflow_doc_feature}` | author/review FEATURE |
| `cf-gears-implement` | `{workflow_implement}` | code from a FEATURE artifact, with `@cpt-*` traceability |
| `cf-gears-coding` | `{workflow_coding}` | code directly from DESIGN/ADR/PRD/upstream context, no FEATURE/`@cpt-*` |
| `cf-gears-gear-creator` | `{workflow_gear_creator}` | scaffold a new gear or add a feature to an existing one (DDD-light layers, SDK, OperationBuilder, SecureORM); thin wrapper over the `gear-creator` skill |
| `cf-gears-change-impact-analysis` | `{workflow_change_impact_analysis}` | read-only downstream impact report for an upstream artifact change |
| `cf-gears-pr-review` | `{workflow_pr_review}` | SDLC-traceability + guardrail PR review (delegates to `cf-gears-toolkit-review` for its Rust/ToolKit pass) |
| `cf-gears-pr-status` | `{workflow_pr_status}` | PR status report |
| `cf-gears-toolkit-review` | `{workflow_toolkit_review}` | idiomatic-Rust / ToolKit-framework conformance review (PR or local branch), standalone or via `cf-gears-pr-review`; thin wrapper over the `toolkit-pr-review` skill |

## Other kit resources

PR tooling, not tied to one artifact kind:

| `{variable}` | Resolves to | Used by |
|---|---|---|
| `{pr_code_review_template}` | `artifacts/PR-CODE-REVIEW-TEMPLATE/template.md` | `cf-gears-pr-review` output format |
| `{pr_status_report_template}` | `artifacts/PR-STATUS-REPORT-TEMPLATE/template.md` | `cf-gears-pr-status` output format |
| `{scripts}` | `scripts/` (directory) | `python3 {scripts}/pr.py`, `{scripts}/prompts/pr/*` |
| `{change_impact_config}` | `scripts/change-impact-analysis.toml` | `cf-gears-change-impact-analysis` thresholds |
| `{skill_toolkit_pr_review}` | `.claude/skills/toolkit-pr-review/` (directory) | bundles the real `toolkit-pr-review` skill (its `SKILL.md` and any future sibling files) for standalone installs; `cf-gears-toolkit-review`'s fallback reads it before falling back further to `{toolkit_pr_review_docs}` |
| `{skill_gear_creator}` | `.claude/skills/gear-creator/` (directory) | bundles the real `gear-creator` skill (its `SKILL.md` and any future sibling files) for standalone installs; `cf-gears-gear-creator`'s fallback reads it before falling back further to `{toolkit_unified_system}` |
| `{agent_toolkit_pr_review_architecture}` … `{agent_toolkit_pr_review_toolkit}` (7 resources) | `.claude/agents/toolkit-pr-review-{architecture,async,design,errors,security,tests,toolkit}.md` | the real definitions `toolkit-pr-review`'s 7 sub-agents dispatch to — bundled since a standalone install's own agent-discovery may not see them; `cf-gears-toolkit-review`'s fallback reads each for its rule-module assignment |

Shared chain infrastructure:

| `{variable}` | Resolves to | Role |
|---|---|---|
| `{agents}` | `AGENTS.md` | always-loaded kit session context (`public=true`) |
| `{constraints}` | `constraints.toml` | allowed ID kinds and downstream reference rules per artifact |
| `{gears_doc_stage_router}` | `modules/doc-stage-router.md` | author→validate→review→fix routing for doc presets |
| `{gears_code_stage_router}` | `modules/code-stage-router.md` | tests→author→validate→review→fix routing for code presets |
| `{gears_doc_phase}` | `plans/doc-phase.md` | phase-plan/phase-dod for doc presets, no separate planning session needed |
| `{gears_code_phase}` | `plans/code-phase.md` | same, for code presets |

60 kit-scoped variables in total (plus 5 Studio-system ones — `{cf-studio-path}`,
`{project_root}`, `{repo}`, `{base_dir}`, `{master_repo}` — that are not kit resources).
Run `{cfs_cmd} resolve-vars --kit gears --flat` for the live, authoritative list.
