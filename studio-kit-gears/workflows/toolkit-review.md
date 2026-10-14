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

This kit's `generate-agents` renames every one of the skill's sub-agents with a `cf-gears-`
prefix (e.g. `toolkit-pr-review-security` becomes `cf-gears-toolkit-pr-review-security`), not
the bare name the skill's own text uses to dispatch it. Dispatch by whichever identity
actually exists in this session, preferring the renamed one.

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

Each sub-agent's own file also hardcodes its rule-module and companion-agent path as a
literal `docs/toolkit-pr-review/...` string — wrong after a standalone copy-mode install,
and a sub-agent dispatch never inherits this session's own path resolution above. Every time
you dispatch any sub-agent, append this line to its dispatch prompt, filled in with the real
resolved path: "Your own file names `docs/toolkit-pr-review/rules/<name>.md` and
`docs/toolkit-pr-review/agents/subject.md` — actually read them at `<resolved
{toolkit_pr_review_docs}>/rules/<name>.md` and `<resolved {toolkit_pr_review_docs}>/agents/
subject.md` instead."
