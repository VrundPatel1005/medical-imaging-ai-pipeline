#!/usr/bin/env python3
"""Create a beginner-friendly baseline segmentation mask."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import scipy.ndimage as ndi


def threshold_mask(data, lower: float, upper: float):
    return ((data >= lower) & (data <= upper)).astype(np.uint8)


def largest_component(mask):
    labels, count = ndi.label(mask)
    if count == 0:
        return mask.astype(np.uint8)
    sizes = ndi.sum(mask, labels, index=np.arange(1, count + 1))
    keep = int(np.argmax(sizes) + 1)
    return (labels == keep).astype(np.uint8)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a simple manual/semi-automatic threshold segmentation."
    )
    parser.add_argument("input", type=Path, help="Input scan.")
    parser.add_argument("--output", type=Path, default=Path("data/outputs/manual_mask.nii.gz"))
    parser.add_argument("--lower", type=float, default=-500.0, help="Lower threshold.")
    parser.add_argument("--upper", type=float, default=500.0, help="Upper threshold.")
    parser.add_argument("--largest-component", action="store_true", help="Keep only the largest connected component.")
    parser.add_argument("--closing", type=int, default=0, help="Optional binary closing iterations.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    from io_utils import load_volume, save_nifti

    volume = load_volume(args.input)
    mask = threshold_mask(volume.data, args.lower, args.upper)
    if args.closing > 0:
        mask = ndi.binary_closing(mask, iterations=args.closing).astype(np.uint8)
    if args.largest_component:
        mask = largest_component(mask)
    output = save_nifti(mask, volume, args.output)
    print(f"Saved baseline segmentation mask: {output}")
    print(f"Foreground voxels: {int(mask.sum())}")


if __name__ == "__main__":
    main()
