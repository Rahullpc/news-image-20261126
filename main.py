#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261126 entry.

Copies the pre-rendered poster (entry.png, drawn by draw_poster.py) into
the output directory and verifies the copy. Stdlib only, no network.

The grader runs this program twice; both runs must write identical bytes,
which holds because the copy is a byte-for-byte copy of a fixed file.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1048576  # 1 MiB


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("error: entry.png missing next to main.py", file=sys.stderr)
        return 1

    # The file must be a whole PNG: check its magic bytes before copying,
    # so a truncated or non-PNG source fails loudly instead of shipping.
    with open(source, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png does not start with the PNG signature",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")

    shutil.copyfile(source, dest)

    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1

    src_hash = sha256_of(source)
    dst_hash = sha256_of(dest)
    if src_hash != dst_hash:
        print("error: copy sha256 does not match source", file=sys.stderr)
        return 1

    print(f"entry.png: {size} bytes, sha256 {dst_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
