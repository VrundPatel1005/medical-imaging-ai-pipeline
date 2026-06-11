#!/usr/bin/env python3
"""Create 2D slice previews and segmentation overlays."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def normalize_for_display(image):
    low, high = np.percentile(image, [1, 99])
    if high <= low:
        return np.zeros_like(image, dtype=np.float32)
    return np.clip((image - low) / (high - low), 0, 1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Save a medical image slice preview or mask overlay.")
    parser.add_argument("image", type=Path, help="Input scan.")
    parser.add_argument("--mask", type=Path, help="Optional segmentation mask.")
    parser.add_argument("--slice", type=int, help="Axial slice index. Defaults to mask center or volume center.")
    parser.add_argument("--output", type=Path, default=Path("data/outputs/overlay.png"))
    parser.add_argument("--title", default="Medical Image Segmentation Preview")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    import matplotlib.pyplot as plt

    from io_utils import binary_mask, center_slice_index, load_volume

    image_volume = load_volume(args.image)
    image = image_volume.data
    mask = None
    if args.mask:
        mask = binary_mask(load_volume(args.mask).data)
        if mask.shape != image.shape:
            raise ValueError(f"Image and mask shapes differ: {image.shape} vs {mask.shape}")

    slice_index = args.slice
    if slice_index is None:
        slice_index = center_slice_index(mask if mask is not None else image)
    if not 0 <= slice_index < image.shape[0]:
        raise ValueError(f"Slice index must be between 0 and {image.shape[0] - 1}")

    plt.figure(figsize=(8, 8))
    plt.imshow(normalize_for_display(image[slice_index]), cmap="gray")
    if mask is not None:
        overlay = np.ma.masked_where(mask[slice_index] == 0, mask[slice_index])
        plt.imshow(overlay, cmap="autumn", alpha=0.45)
    plt.title(f"{args.title} | axial slice {slice_index}")
    plt.axis("off")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(args.output, dpi=180)
    plt.close()
    print(f"Saved visualization: {args.output}")


if __name__ == "__main__":
    main()
