#!/usr/bin/env python3
"""Set the Picturesque version in picturesque.spec and add a changelog entry."""

from __future__ import annotations

import datetime
import pathlib
import re
import sys

PACKAGER = "Benedikt Nimmervoll <beneedict@users.noreply.github.com>"
SPEC = pathlib.Path(__file__).resolve().parent.parent / "picturesque.spec"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} VERSION", file=sys.stderr)
        return 2
    version = sys.argv[1].removeprefix("v")
    if not re.fullmatch(r"\d+(?:\.\d+)+", version):
        print(f"invalid version: {version!r}", file=sys.stderr)
        return 2

    text = SPEC.read_text()
    current = re.search(r"(?m)^Version:\s*(\S+)$", text)
    if current and current.group(1) == version:
        print(f"{SPEC.name} is already at {version}")
        return 0

    text = re.sub(r"(?m)^Version:\s*.*$", f"Version:        {version}", text, count=1)
    text = re.sub(r"(?m)^Release:\s*.*$", "Release:        1%{?dist}", text, count=1)

    date = datetime.datetime.now(datetime.timezone.utc).strftime("%a %b %d %Y")
    entry = f"* {date} {PACKAGER} - {version}-1\n- Update to Picturesque {version}.\n\n"
    text = text.replace("%changelog\n", "%changelog\n" + entry, 1)
    SPEC.write_text(text)
    print(f"updated {SPEC.name} to {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
