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
If the `toolkit-pr-review` skill isn't live-invocable in this session (for example a
standalone kit install without `.claude/skills/toolkit-pr-review` registered as a usable
skill), the kit still bundles the real skill directory at `{skill_toolkit_pr_review}`
(its `SKILL.md`) — read it
first for the intended process (it's the actual skill content, not a paraphrase). Its
process assumes seven dispatchable sub-agents that a standalone install likely doesn't have
configured, so when those aren't available, read `{toolkit_pr_review_docs}/RULES.md` and
`{toolkit_pr_review_docs}/rules/*.md` directly instead and apply them manually against the
diff — one pass per rule module, covering the same
architecture/async/design/errors/security/tests/toolkit areas — since those bundled rule
modules are the actual criteria this review is based on, skill or no skill.

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
