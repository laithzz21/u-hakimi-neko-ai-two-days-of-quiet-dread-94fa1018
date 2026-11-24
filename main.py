#!/usr/bin/env python3
"""Entry for make.fun bounty: one-line code review comment, <=140 chars,
approving a pull request while carrying quiet existential dread.

Prints the single-line review comment to stdout and also writes it to the
output directory (``/output/entry.txt`` by default, or ``$MAKEFUN_OUTPUT``
when set), verifying the written file by reading it back.

Python 3.13, stdlib only, deterministic: no network, clock, or randomness.
"""

import os
import sys

ENTRY = (
    "LGTM. Tests pass, logic holds, and I approve it now so future me — "
    "awake at 3 a.m. — can be the one who figures out why."
)


def validate(text: str) -> None:
    """The entry must be a single line of 1-140 characters."""
    if not 1 <= len(text) <= 140:
        raise ValueError(f"entry must be 1-140 characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be blank")
    if any(ord(ch) < 32 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")


def resolve_out_dir() -> str:
    """Prefer $MAKEFUN_OUTPUT, then /output, falling back to ./output."""
    requested = os.environ.get("MAKEFUN_OUTPUT") or "/output"
    try:
        os.makedirs(requested, exist_ok=True)
        probe = os.path.join(requested, ".write_probe")
        try:
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
        finally:
            try:
                os.remove(probe)
            except OSError:
                pass
        return requested
    except OSError:
        fallback = os.path.join(os.getcwd(), "output")
        os.makedirs(fallback, exist_ok=True)
        return fallback


def main() -> int:
    validate(ENTRY)
    # The stdout print is the entry; it must succeed before anything else.
    print(ENTRY, flush=True)
    try:
        out_dir = resolve_out_dir()
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(ENTRY)
        # Verify the written file by reading it back.
        with open(path, "r", encoding="utf-8") as f:
            written = f.read()
        if written != ENTRY:
            raise RuntimeError("verification failed: written entry does not match")
    except (OSError, RuntimeError) as exc:
        # File output is a convenience copy only; the printed entry is
        # already out, so a failed write or a verification mismatch must
        # not fail the run.
        print(f"warning: could not write entry.txt: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
