#!/usr/bin/env python3
"""Copy the bundled artwork to /output/entry.png.

The bundled file is a JPEG image stored under the name entry.png; the
bounty rules distinguish it by its first bytes, not its extension.
"""

import hashlib
import os
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
TARGET = "/output/entry.png"
MAX_BYTES = 1024 * 1024
JPEG_START = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"


def main():
    with open(SOURCE, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        sys.exit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if not data.startswith(JPEG_START):
        sys.exit("entry.png does not start with the JPEG magic bytes")
    if not data.endswith(JPEG_END):
        sys.exit("entry.png does not end with the JPEG end marker")
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    with open(TARGET, "wb") as handle:
        handle.write(data)
    with open(TARGET, "rb") as handle:
        written = handle.read()
    if written != data:
        sys.exit("verification failed: /output/entry.png differs from entry.png")
    print(f"wrote {TARGET}: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
