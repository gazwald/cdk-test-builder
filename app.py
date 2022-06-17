#!/usr/bin/env python
import sys

from builder import builder

if __name__ == "__main__":
    args = sys.argv
    files: list[str] = ["template.json"]
    if len(args) > 1:
        files = args[1:]

    builder(files)
