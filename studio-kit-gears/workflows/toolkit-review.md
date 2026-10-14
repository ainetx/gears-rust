---
cf: true
type: workflow
name: cf-gears-toolkit-review
description: Invoke when the user wants idiomatic-Rust and ToolKit-framework conformance review of a PR or local branch, independent of SDLC-traceability review — e.g. "toolkit review PR 123", "review ToolKit conformance", "/cf-gears-toolkit-review local"
version: 1.0
purpose: Thin Studio-kit wrapper over the toolkit-pr-review skill.
---

# Toolkit Conformance Review Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/studio/SKILL.md` FIRST.

LOAD `{skill_toolkit_pr_review}` and FOLLOW all of its instructions, passing through
whatever parameters were given to this workflow.

This kit's `generate-agents` renames the skill's 7 sub-agents with a `cf-gears-` prefix
(`cf-gears-toolkit-pr-review-{architecture,async,design,errors,security,tests,toolkit}`),
not the bare names the skill's own text uses to dispatch them
(`toolkit-pr-review-{architecture,async,design,errors,security,tests,toolkit}`). Dispatch by
whichever identity actually exists in this session, preferring the renamed one.

The skill's own text also cites `docs/toolkit-pr-review/...` and
`tools/scripts/toolkit-pr-review/...` as plain, project-root-relative paths — correct when
running inside the `gears-rust` checkout itself (register-mode install, or no install at
all), but not when this kit was installed standalone in copy mode: there, every bundled
resource (this skill included) lands nested under this install's own kit-storage root, not
at the literal project root. Resolve `{toolkit_pr_review_docs}` and
`{toolkit_pr_review_scripts}` first and read every such path the skill's text names relative
to whichever one of those two actually contains it, instead of the literal path the skill's
own text gives — the file names and sub-paths past that root are unchanged, only the root
differs. When `{toolkit_pr_review_docs}`/`{toolkit_pr_review_scripts}` resolve to the exact
same literal `docs/toolkit-pr-review`/`tools/scripts/toolkit-pr-review` the skill's text
already assumes (the in-repo case), this is a no-op.
