#!/usr/bin/env python3
"""Ensure guidelines/DNA is available before a gears preset relies on it.

Constructor Studio kit script: lives in studio-kit-gears/scripts/ensure-dna.py.
Resolves the actual on-disk location of `{dna_rust}`/`{dna_rest}` through
`cfs resolve-vars` rather than a hardcoded path, because where a kit resource
lands depends entirely on how it was installed (in-repo "register" mode keeps
it at its source path; a standalone "copy" install places it under
`.cf-studio/config/kits/<slug>/...` instead) — never on a fixed project-root-
relative path.

`guidelines/DNA` is additionally a git submodule in the `gears-rust` repo
itself, so a checkout can have it registered but not fetched. A kit installed
standalone (outside `gears-rust`) has no such submodule at all; there, the kit
manifest must already have bundled the needed files as plain copies at install
time. This script tells the two cases apart and gives the right remediation
for each, instead of silently reviewing or generating against absent files.
"""

import json
import os
import shutil
import subprocess
import sys

_GITMODULES_MARKER = 'submodule "guidelines/DNA"'


def _find_project_root():
    """Find project root via git rev-parse, then walk up for .gitmodules/.git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(25):
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return os.getcwd()


def _is_dna_submodule_checkout(root):
    gitmodules = os.path.join(root, ".gitmodules")
    if not os.path.isfile(gitmodules):
        return False
    try:
        with open(gitmodules, encoding="utf-8") as f:
            return _GITMODULES_MARKER in f.read()
    except OSError:
        return False


def _resolve_dna_rust_path():
    """Resolve the actual installed location of {dna_rust} via `cfs resolve-vars`.

    Returns the resolved absolute path, or None if `cfs` isn't available (the
    caller falls back to a best-effort guess in that case).
    """
    cfs_cmd = shutil.which("cfs")
    if cfs_cmd is None:
        return None
    try:
        result = subprocess.run(
            [cfs_cmd, "--json", "resolve-vars", "--kit", "gears", "--flat"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        return data.get("variables", {}).get("dna_rust")
    except (OSError, json.JSONDecodeError):
        return None


def main():
    root = _find_project_root()
    canary = _resolve_dna_rust_path()
    best_effort = canary is None
    if best_effort:
        canary = os.path.join(root, "guidelines", "DNA", "languages", "RUST.md")

    if os.path.isfile(canary) and os.path.getsize(canary) > 0:
        print(f"OK: {canary} present")
        return 0

    if _is_dna_submodule_checkout(root):
        print(
            f"{canary} is missing but guidelines/DNA is a registered submodule here; "
            "initializing it now..."
        )
        result = subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive", "--", "guidelines/DNA"],
            cwd=root,
        )
        # Re-resolve: initializing the submodule doesn't move it, but a `cfs`-less
        # best-effort guess may have been wrong before the submodule existed at all.
        canary = _resolve_dna_rust_path() or canary
        if result.returncode == 0 and os.path.isfile(canary) and os.path.getsize(canary) > 0:
            print(f"OK: {canary} fetched")
            return 0
        print(
            "ERROR: could not initialize the guidelines/DNA submodule automatically.\n"
            "Run this manually, then retry:\n"
            "  git submodule update --init --recursive -- guidelines/DNA",
            file=sys.stderr,
        )
        return 1

    print(
        f"ERROR: {canary} is missing and this project has no guidelines/DNA submodule "
        "(standalone kit install). The kit manifest should have bundled this file as a "
        "plain copy at install time — this looks like an incomplete or stale install.\n"
        "Reinstall or refresh the kit, then retry:\n"
        "  cfs kit update\n"
        "  cfs kit install --force",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
