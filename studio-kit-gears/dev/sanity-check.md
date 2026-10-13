# Gears Kit Sanity Check (dev-only — NOT a kit resource)

Not registered in `.cf-studio-kit.toml` on purpose: this is a maintainer tool for
regression-testing `studio-kit-gears/` itself (the concrete instance of
[gears-rust#5197](https://github.com/constructorfabric/gears-rust/issues/5197),
"Automated regression runs of the kit workflows"), not something a standalone kit
install should ship. It packages, as pinned/reproducible scenarios, everything that
was verified by hand across the session that produced
[gears-rust#5326](https://github.com/constructorfabric/gears-rust/pull/5326).

**Reproducibility rule**: every scenario below pins a concrete PR number, commit, file
path, or hypothetical condition. Never substitute "a small recent PR" or "pick
something" — re-running this suite on an unchanged kit must give the same pass/fail
result every time, which is the entire point of a regression check. If a pinned PR
number ever stops existing/resolving (force-push, repo history rewrite), replace it
with another *specific* pinned PR and update this file in the same change — never
silently fall back to "find something similar."

## How to run

Dispatch every scenario below as a **parallel** background agent (the `Agent` tool,
`subagent_type: general-purpose`, one call per scenario, all in a single message).
Each prompt is self-contained — paste it verbatim as that agent's prompt, filling in
only `<WORKTREE_PATH>` with the current worktree's absolute path. Every agent must be
told explicitly: **read-only except where a scenario says otherwise; never run a git
command that mutates state (checkout/branch/commit/stash/reset) in a shared worktree
without first confirming no other session is using it.** Collect results into the
pass/fail table in "Reporting" below.

---

## Scenario 1 — Repo-wide `{variable}` citations resolve to real, matching content

> Run `cfs resolve-vars --kit gears --flat` from `<WORKTREE_PATH>`. For each of these 17
> variables — `{gears_md}`, `{architecture_manifest}`, `{toolkit_unified_system}`,
> `{toolkit_pr_review_docs}`, `{repo_adrs}`, `{repo_arch}`, `{repo_playbook}`,
> `{guidelines_security}`, `{guidelines_dependencies}`, `{guidelines_gts}`, `{dna_rust}`,
> `{dna_rest}`, `{iso_29148}`, `{testing_policy}`, `{fips_requirements}`,
> `{gears_security}`, `{ensure_dna_script}` — confirm it resolves to a real path, open
> the resolved file/directory, and judge whether the real content genuinely supports
> what cites it in `studio-kit-gears/codebase/{rules.md,design-led-rules.md,checklist.md}`
> and `studio-kit-gears/artifacts/*/{rules.md,checklist.md}`. Flag any `{var}` that fails
> to resolve, any mismatch between a citation's claim and the real content, or any
> redundancy between two variables (e.g. check `{gears_security}` vs
> `{guidelines_security}`, and `{repo_playbook}` vs `{gears_md}`, specifically — these
> were previously confirmed distinct, confirm that's still true). Report pass/fail per
> variable, under 350 words total.

**Expected**: all 17 PASS, no broken resolution, no redundancy between the two named
pairs. (Last confirmed: all PASS, see PR #5326.)

## Scenario 2 — `ensure-dna.py`, all 3 real install states

> In `<WORKTREE_PATH>`, run `python3 studio-kit-gears/scripts/ensure-dna.py` and report
> its exact output and exit code (submodule state: whatever it currently is — note it).
> Then, in an isolated scratch directory (NOT `<WORKTREE_PATH>`, create a fresh one under
> your own scratchpad), run `git init -q`, `mkdir -p guidelines/DNA/languages`, then run
> the same script there via its absolute path from `<WORKTREE_PATH>/studio-kit-gears/scripts/ensure-dna.py`
> and confirm it reports the "standalone install with no submodule" error (not a
> submodule-init attempt) and exits non-zero. Then, back in `<WORKTREE_PATH>`, if
> `guidelines/DNA/languages/RUST.md` exists, temporarily rename it to `.bak`, re-run the
> script (expect it to auto-run `git submodule update --init --recursive -- guidelines/DNA`
> and succeed), then confirm the file is back and rename `.bak` back if you moved
> anything. Report pass/fail for: (a) no-op when already present, (b) submodule
> auto-init when registered-but-missing, (c) standalone-no-submodule gives the distinct
> error. Under 250 words.

**Expected**: all 3 PASS. (Last confirmed: all PASS, see PR #5326; this script itself
was fixed once already after this exact test caught it resolving paths wrong under
copy-mode installs — Scenario 3 covers that case.)

## Scenario 3 — Standalone copy-mode install bundles everything with real content

> In a fresh scratch directory (not `<WORKTREE_PATH>`), run: `git init -q`, then
> `cfs init -y`, then `cfs kit install --path <WORKTREE_PATH> --install-mode copy --kit
> gears` (add `--force --approve-overwrite scripts --approve-overwrite
> ensure_dna_script` plus any other resource ids it names as changed, if this isn't the
> first install there). Then run `cfs resolve-vars --kit gears --flat` from that scratch
> directory and confirm every one of the 17 variables in Scenario 1, plus
> `{workflow_toolkit_review}` and `{workflow_gear_creator}`, now resolves to a path under
> `.cf-studio/config/kits/gears/...` (NOT back into `<WORKTREE_PATH>`), and that the file
> at that resolved path actually exists with non-trivial size (not a 0-byte stub). Report
> a pass/fail table of all 19 resolved paths plus their byte sizes. Under 300 words.

**Expected**: all 19 resolve under the scratch install's own `.cf-studio/`, all non-trivial
size. (Last confirmed for the first 17: PR #5326; `{workflow_toolkit_review}` and
`{workflow_gear_creator}` were added later in the same PR — re-confirm both here.)

## Scenario 4 — `toolkit-pr-review` skill, live, pinned PR

> In `<WORKTREE_PATH>`, run the `toolkit-pr-review` skill in local mode against the
> *merged* PR **#5213** (`fix(settings-service): walk live tenants only under the
> subtree budget`, constructorfabric/gears-rust — 5 Rust/manifest files). Since it's
> already merged, reconstruct it as a local branch: find its merge commit via `gh pr view
> 5213 --repo constructorfabric/gears-rust --json mergeCommit`, then diff that commit
> against its first parent (the pre-merge base) rather than against current `main`.
> Invoke `toolkit-pr-review`'s local mode with `--base` pointed at that parent commit.
> Confirm all 7 subject sub-agents (errors, security, async, design, tests, toolkit,
> architecture) run and produce findings that cite real file:line locations in the diff
> (not generic filler) — specifically expect something resembling the `RUST-TYPE-001`
> finding on a hardcoded `TenantStatus` vec previously found here. Report pass/fail and
> whether the findings still look grounded. Under 250 words.

**Expected**: PASS, 7 sub-agents, grounded findings. (Last confirmed: PR #5326.)

## Scenario 5 — Full `cf-gears-pr-review` end-to-end, pinned PR

> In `<WORKTREE_PATH>`, follow `studio-kit-gears/workflows/pr-review.md` literally, in
> order, exactly as `/cf-gears-pr-review 5288` would, against PR **#5288**
> (`fix(quota-enforcement): build GTS ids with gts_id! and document the canonical
> resources`, constructorfabric/gears-rust — 4 files): `python3
> studio-kit-gears/scripts/pr.py fetch 5288`, select the "Code Review" prompt, run the
> architecture pass, reviewer-comment analysis, the guardrail pass, then step 4c3 (which
> should now say to run `cf-gears-toolkit-review` rather than invoking the underlying
> skill directly — confirm the wording actually says that). Confirm the resulting
> `.prs/5288/review.md` has the mandatory "Architecture" section, and that step 4c3
> fired and populated the Correctness/Conformance/Style/Performance/Tests/Security
> sections from real findings, not generic filler. Report pass/fail and the final
> verdict reached. Under 300 words.

**Expected**: PASS, Architecture section present, step 4c3 fires via `cf-gears-toolkit-review`,
verdict ✅ APPROVE (mechanical lint-compliance fix). (Last confirmed: PR #5326, though at
that time step 4c3 still named the underlying skill directly — re-confirm the delegation
wording specifically, since that changed after this test last ran.)

## Scenario 6 — `cf-gears-toolkit-review` workflow, live, pinned PR

> In `<WORKTREE_PATH>`, read `studio-kit-gears/workflows/toolkit-review.md` in full, then
> execute it in local mode against the same reconstructed-local-branch for PR **#5213**
> as Scenario 4 (reuse that reconstruction). Confirm the workflow's own prose reads
> clearly enough to execute without guessing, and that invoking the underlying skill
> through this wrapper produces the same quality of grounded findings as Scenario 4's
> direct call (don't just trust it — compare the findings). Also confirm the `--base
> <REF>` passthrough this workflow documents is actually honored. Report pass/fail. Under
> 200 words.

**Expected**: PASS, output indistinguishable from Scenario 4's direct skill call. (Last
confirmed: PR #5326.)

## Scenario 7 — `cf-gears-gear-creator` workflow, live

> **Not yet run as a live scenario** — `studio-kit-gears/workflows/gear-creator.md` was
> added and reviewed statically but never exercised end-to-end. Read it in full, then
> exercise Step 2 (invoke the `gear-creator` skill) against a small, low-risk edit: add
> one trivial new field to `examples/toolkit/users-info/users-info/src/domain/service/`
> (check the actual file layout first — do not invent a path) under a scratch branch, NOT
> committed, then `git checkout -- .` to discard it when done (confirm `git status
> --porcelain` is clean before you start, so you know exactly what to discard). Confirm
> the skill was actually invoked (not silently skipped) and that Step 3's verify commands
> (`cargo build`, `cargo clippy`, `make dylint`, `cargo test`, scoped to the touched
> crate) are the ones actually named. Report pass/fail. This scenario's PASS bar is
> lower — it's establishing a first baseline, not comparing against a prior confirmed
> run.

**Expected**: unestablished — first run. Once it passes once, pin the exact edit made
here (not "a trivial field") so future re-runs are comparable.

## Scenario 8 — Smart CI routing: fact-detection and `{testing_policy}` routing

> Read the full current `studio-kit-gears/modules/code-stage-router.md`, specifically
> `GearsCodeDispatchContext` and `GearsCodeClose`/`GearsCodeStageRoute`, plus
> `docs/TESTING.md` section "7.4 Local CI Routing". Hand-trace these 4 fixed hypothetical
> slices as a PDSL interpreter would (do not substitute different ones):
> (a) a slice that only edits `gears/<gear>/src/domain/service/foo.rs` — expect ONLY
> `gear-ci`+`dylint` (+`cfs validate` if feature-led), nothing routed;
> (b) a slice that adds `gears/<gear>/src/api/rest/handlers/new_thing.rs` where the gear
> has a server feature — expect `make openapi GEAR=<gear>` additionally routed;
> (c) a slice that bumps a dependency version in `gears/<gear>/Cargo.toml` — expect
> `make deny` AND `make shear` both routed (not just deny — confirm the shear row's
> wording no longer requires an undetectable "added/removed, not bumped" distinction);
> (d) a slice to `libs/toolkit/src/some_file.rs` — expect `make test-fips` routed (confirm
> the git-status scope in `GearsCodeDispatchContext` actually includes `libs/toolkit/`
> now, not just `gears/<gear>/`). Report pass/fail per scenario. Under 300 words.

**Expected**: all 4 PASS. (Last confirmed: PR #5326, after 2 rounds of bugfixes — this
scenario exists specifically because the first version silently failed (c) and (d).)

## Scenario 9 — `GearsCodeChainSweep`: last-feature detection and blocked-routing

> Read the full current `studio-kit-gears/modules/code-stage-router.md`'s
> `GearsCodeClose`/`GearsCodeChainSweep`. Hand-trace these 4 fixed hypothetical closes:
> (a) a FEATURE slice finishes but the FEATURE has more unimplemented slices — expect
> `GEARS_LAST_FEATURE_IN_CHAIN=false`, no sweep, same `cf-git-commit` pin as always;
> (b) a FEATURE finishes its last slice but siblings in its DECOMPOSITION are still
> pending — expect no sweep, `cf-git-commit` pinned;
> (c) a design-led (`cf-gears-coding`) run finishes its last slice — expect the sweep TO
> run (design-led has no DECOMPOSITION/FEATURE layer, so "every slice implemented" alone
> means chain-complete — confirm this branch is separate from the feature-led backreference
> check, not conflated with it);
> (d) a feature-led run's FEATURE has a missing/malformed DECOMPOSITION backreference —
> expect `GEARS_LAST_FEATURE_IN_CHAIN=false` (NOT treated as chain-complete) and the same
> `cf-git-commit` pin as if there were more features pending.
> Then confirm: when `GearsCodeChainSweep` returns `blocked` with a finding naming a
> specific FEATURE, the re-routed `validate` stage's payload carries THAT feature's path/
> slice, not the just-closed one; when a finding names DESIGN itself, it routes to
> `cf-gears-doc-design` instead; and confirm the findings riding in `NEXT_ACTION_PAYLOAD`
> use the canonical `review-findings` key, NOT a `GEARS_*`-prefixed one (check this
> specifically — `GearsCodeStageResolve` strips `GEARS_*` fields when building
> `GEARS_FORWARD_PAYLOAD`, which would silently drop a `GEARS_*`-named payload field).
> Report pass/fail per check. Under 350 words.

**Expected**: all PASS. (Last confirmed: PR #5326, after 3 rounds of bugfixes — (c)/(d)'s
mode-conflation and the `GEARS_*`-stripping issue were both real bugs caught by this exact
scenario shape; re-running it is specifically meant to catch a regression if either ever
comes back.)

## Scenario 10 — Manifest structural integrity

> In `<WORKTREE_PATH>`, run `cfs kit validate` and confirm 0 errors (note the exact
> warning count — compare it to the last known baseline of 8 warnings across
> ADR(1)/DECOMPOSITION(1)/DESIGN(2)/FEATURE(2)/PRD(2), all pre-existing frontmatter/
> heading issues unrelated to this kit's generation-rules work; a NEW warning beyond
> these is a regression to flag, not something to silently accept). Then run `grep -n
> "^\[kits.resources.artifacts\.\|^id = \"constraints\"" .cf-studio-kit.toml` and confirm
> the `constraints` resource immediately precedes the six
> `[kits.resources.artifacts.*]` blocks with nothing between them (a resource inserted
> between them silently reparents the artifacts bindings onto the wrong resource — this
> exact bug happened once already in this kit's history). Report pass/fail. Under 150
> words.

**Expected**: 0 errors, exactly 8 warnings at the known locations, `constraints`
immediately before the artifacts bindings. (Last confirmed: PR #5326.)

---

## Reporting

Collect every scenario's agent result into one table:

| # | Scenario | Pass/Fail | Notes (new findings since last pinned run) |
|---|---|---|---|
| 1 | Citation resolution + content match | | |
| 2 | ensure-dna.py (3 states) | | |
| 3 | Standalone copy-mode install | | |
| 4 | toolkit-pr-review live (PR #5213) | | |
| 5 | cf-gears-pr-review end-to-end (PR #5288) | | |
| 6 | cf-gears-toolkit-review live (PR #5213) | | |
| 7 | cf-gears-gear-creator live (baseline) | | |
| 8 | Smart CI routing (4 traces) | | |
| 9 | GearsCodeChainSweep (4 traces + routing) | | |
| 10 | Manifest structural integrity | | |

Any scenario that regresses from its "Expected" line is a real regression in the kit,
not a test-flake — these scenarios are all deterministic by construction (pinned PRs,
pinned hypothetical conditions, pinned file paths). Update each scenario's "Expected"
line in this file once a new baseline is confirmed, so the next run compares against
the current truth, not a stale one.
