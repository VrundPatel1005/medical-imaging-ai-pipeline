#!/usr/bin/env python3
"""Run TotalSegmentator for AI-assisted CT segmentation."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run TotalSegmentator on a CT NIfTI scan.")
    parser.add_argument("input", type=Path, help="Input CT image, usually .nii.gz.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/outputs/totalsegmentator"))
    parser.add_argument("--task", default="total", help="TotalSegmentator task name. Default: total.")
    parser.add_argument("--fast", action="store_true", help="Use faster lower-resolution mode.")
    parser.add_argument("--cpu", action="store_true", help="Force CPU inference.")
    parser.add_argument("--preview", action="store_true", help="Print command without running it.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if not args.preview and not args.input.exists():
        print(f"Input scan does not exist: {args.input}", file=sys.stderr)
        raise SystemExit(2)

    executable = shutil.which("TotalSegmentator")
    if executable is None:
        if args.preview:
            executable = "TotalSegmentator"
        else:
            print("TotalSegmentator CLI was not found in this environment.", file=sys.stderr)
            print("Install with: pip install totalsegmentator", file=sys.stderr)
            print("Then rerun this script after activating your virtual environment.", file=sys.stderr)
            raise SystemExit(2)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    command = [
        executable,
        "-i",
        str(args.input),
        "-o",
        str(args.output_dir),
        "--task",
        args.task,
    ]
    if args.fast:
        command.append("--fast")
    if args.cpu:
        # CPU mode is slower, but it is the most reliable default for beginner laptops.
        command.append("--device")
        command.append("cpu")

    print("Running AI-assisted segmentation:")
    print(" ".join(command))
    if args.preview:
        return

    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    print(f"TotalSegmentator outputs saved in: {args.output_dir}")


if __name__ == "__main__":
    main()
