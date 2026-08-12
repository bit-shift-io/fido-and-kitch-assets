#!/usr/bin/env python3
"""Assemble the final Gemini prompt for a level stencil.

prompt/level-gen.md is documentation for humans — it contains placeholder tokens,
every theme pack, and troubleshooting notes. Feeding that file to Gemini directly
poisons the generation: unsubstituted {{TOKENS}}, five competing themes, and
tuning prose the model reads as description. This script extracts only what the
model should see.

By default it writes full_prompt.md next to the stencil.

Usage:
    python3 tools/build_prompt.py maps/sandbox/export_sandbox.png steampunk
        -> writes maps/sandbox/full_prompt.md
    python3 tools/build_prompt.py <stencil.png> <theme> -o somewhere/else.md
    python3 tools/build_prompt.py <stencil.png> <theme> --stdout
    python3 tools/build_prompt.py --list
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "prompt" / "level-gen.md"
MANIFEST_TOOL = ROOT / "tools" / "stencil_manifest.py"


def blocks(text):
    """Yield (heading, code-block-body) for every fenced block in the doc."""
    heading = None
    for chunk in re.split(r"^(#+ .*)$", text, flags=re.M):
        if chunk.startswith("#"):
            heading = chunk.lstrip("# ").strip()
        else:
            for body in re.findall(r"^```text\n(.*?)^```", chunk, flags=re.M | re.S):
                yield heading, body


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load(path):
    """Return (template, themes).

    Two supported layouts:
      - a structured doc with a '## MASTER PROMPT' text block and theme packs
        (prompt/level-gen-complex.md)
      - a plain prompt file, used verbatim as the template with no theme packs
        (prompt/level-gen.md)
    """
    doc = path.read_text()
    master, themes = None, {}
    for heading, body in blocks(doc):
        if heading == "MASTER PROMPT":
            master = body
        elif body.lstrip().startswith("THEME NAME:"):
            themes[slug(heading)] = body
    if master is None:
        return doc, {}
    return master, themes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stencil", nargs="?")
    ap.add_argument("theme", nargs="?",
                    help="theme pack name; omit for prompt files that have none")
    ap.add_argument("-p", "--prompt", default=str(SOURCE),
                    help=f"prompt source file (default: {SOURCE.relative_to(ROOT)})")
    ap.add_argument("-o", "--out",
                    help="output path (default: full_prompt.md beside the stencil)")
    ap.add_argument("--stdout", action="store_true", help="print instead of writing a file")
    ap.add_argument("--cell", type=int, default=128)
    ap.add_argument("--list", action="store_true", help="list available themes")
    args = ap.parse_args()

    source = Path(args.prompt)
    master, themes = load(source)

    if args.list:
        print(f"Themes in {source}:" if themes else f"{source} has no theme packs.")
        for name in themes:
            print(f"  {name}")
        return 0
    if not args.stencil:
        ap.error("a stencil path is required")

    theme, chosen = None, "none"
    if themes:
        if not args.theme:
            ap.error(f"{source} needs a theme: {list(themes)}")
        matches = [k for k in themes if k.startswith(slug(args.theme))]
        if len(matches) != 1:
            sys.exit(
                f"error: theme '{args.theme}' matched {matches or 'nothing'}; "
                f"choose one of {list(themes)}"
            )
        theme, chosen = themes[matches[0]], matches[0]
    elif args.theme:
        print(f"note: {source} has no theme packs; ignoring theme '{args.theme}'",
              file=sys.stderr)

    manifest = subprocess.run(
        [sys.executable, str(MANIFEST_TOOL), args.stencil, "--cell", str(args.cell)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    out = master.replace("{{GEOMETRY_MANIFEST}}", manifest)

    if theme:
        # Substitute the theme pack for the whole {{SLOT}} skeleton in section 4.
        out = re.sub(
            r"THEME NAME: \{\{THEME_NAME\}\}.*?PALETTE: \{\{PALETTE\}\}",
            lambda _: theme.strip(),
            out, flags=re.S,
        )

    leftover = re.findall(r"\{\{(\w+)\}\}", out)
    if leftover:
        sys.exit(f"error: unsubstituted placeholders remain: {sorted(set(leftover))}")

    if args.stdout:
        sys.stdout.write(out)
        return 0

    dest = Path(args.out) if args.out else Path(args.stencil).parent / "full_prompt.md"
    dest.write_text(out)
    print(f"wrote {dest} — {len(out)} chars, from {source.name}, theme '{chosen}'. "
          f"Paste this whole file into Gemini with the stencil attached.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
