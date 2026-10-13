---
cf: true
type: workflow
name: cf-gears-toolkit-review
description: Invoke when the user wants idiomatic-Rust and ToolKit-framework conformance review of a PR or local branch, independent of SDLC-traceability review — e.g. "toolkit review PR 123", "review ToolKit conformance", "/cf-gears-toolkit-review local"
version: 1.0
purpose: Thin Studio-kit wrapper over the toolkit-pr-review skill, with a rule-module fallback when that skill isn't installed.
---

# Toolkit Conformance Review Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/studio/SKILL.md` FIRST.

**Type**: Analysis
**Role**: Reviewer
**Output**: PR mode — inline GitHub review comments (via the underlying skill); local mode — a local markdown report.

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Rust/ToolKit-framework conformance on a PR | **this workflow** | "toolkit review PR 123", `/cf-gears-toolkit-review 123` |
| Rust/ToolKit-framework conformance on a local branch | **this workflow** | "toolkit review my branch", `/cf-gears-toolkit-review local` |
| Full SDLC-traceability + guardrail PR review | **pr-review.md** | "review PR 123", `/cf-gears-pr-review 123` |

---

## Overview

Accepts the same arguments as the underlying `toolkit-pr-review` skill:
- `<PR_NUMBER>` — PR mode: reviews a GitHub PR, posts inline review comments.
- `local [<branch-name>]` — local mode: reviews a local branch against its trunk, writes a
  markdown report, posts nothing.
- `--repo <owner/repo>` — optional, PR mode only.
- `--base <REF>` — optional, local mode only: override the auto-resolved trunk. Needed in
  fork setups where the default base-resolution order picks the wrong remote, or when the
  branch's tip is already an ancestor of the current trunk (e.g. the PR already merged) and
  auto-resolution can't find a meaningful diff. Passed straight through to the underlying
  skill — this workflow adds no logic of its own around it.

This workflow is a thin Studio entrypoint: it's the canonical kit-level way to run
idiomatic-Rust / ToolKit-framework conformance review **on its own**, outside the
SDLC-traceability-focused `cf-gears-pr-review`. `cf-gears-pr-review` step 4c3 delegates
here for its Rust/ToolKit compliance pass too, so there is one place that owns this
capability, not two independently-drifting copies.

---

## Prerequisite Checklist

- [ ] For PR mode: `gh` CLI installed and authenticated (`gh auth status`), repository has
  a GitHub remote configured
- [ ] For local mode: a resolvable local branch and trunk (see the underlying skill's own
  base-resolution rule)

---

## Steps

## Step 1: Resolve mode and arguments
Parse the argument exactly as the `toolkit-pr-review` skill does: a number selects PR
mode; the literal word `local` (plus an optional branch name, defaulting to the current
branch) selects local mode.

## Step 2: Run the review
Invoke the `toolkit-pr-review` skill with the resolved arguments — `/toolkit-pr-review
<PR_NUMBER>` or `/toolkit-pr-review local [<branch-name>]`, plus `--repo` when given. It
owns PR/branch resolution, diff fetching, the seven subject sub-agent dispatch
(architecture, async, design, errors, security, tests, toolkit), merge/dedup, and output
formatting or posting — this workflow does not re-implement any of that.

### Fallback — skill not installed
`cfs generate-agents` only turns this kit's own `workflow_*` resources (this wrapper
included) into invocable skills — it does not generate a bare `toolkit-pr-review` skill
from `{skill_toolkit_pr_review}`. So in a standalone kit install, the live skill is never
available here, not just rarely: go straight to this fallback rather than attempting
`/toolkit-pr-review` first and only falling back on failure.

Read `{skill_toolkit_pr_review}` (its `SKILL.md`) first for the intended process — it's the
actual skill content, not a paraphrase. That process dispatches seven sub-agents named
`toolkit-pr-review-architecture`, `-async`, `-design`, `-errors`, `-security`, `-tests`,
`-toolkit` — but `cfs generate-agents` installs this kit's bundled copies of them
(`{agent_toolkit_pr_review_architecture}` / `-async` / `-design` / `-errors` / `-security` /
`-tests` / `-toolkit`) under the renamed identity `cf-gears-toolkit-pr-review-<area>`, not
the bare name. **Dispatch them by that renamed identity, not the bare one.** If they aren't
present under either name, read `{toolkit_pr_review_docs}/RULES.md` and
`{toolkit_pr_review_docs}/rules/*.md` directly and apply them manually, one pass per module,
covering the same architecture/async/design/errors/security/tests/toolkit areas — since
those bundled files
are the actual real definitions this review is based on, dispatchable or not.

## Step 3: Present results
Summarize the findings to the user: severity, file:line, rule ID, and suggested fix. In PR
mode, confirm whether comments were posted; in local mode, give the report's file path.

---

## Validation Criteria

- [ ] Mode resolved correctly (PR vs. local)
- [ ] The underlying skill was invoked, or the rule-module fallback was applied when it
  wasn't available
- [ ] Findings cover all seven subject areas (architecture, async, design, errors,
  security, tests, toolkit), or state why one doesn't apply to this diff
- [ ] Results presented to the user

---

## Next Steps

### Options
- [ ] Run the full SDLC-traceability review through `cf-gears-pr-review`
- [ ] Fix flagged findings, then re-run this workflow
