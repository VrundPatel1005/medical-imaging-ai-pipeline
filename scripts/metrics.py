#!/usr/bin/env python3
"""Compute segmentation statistics and comparison metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _overlap_counts(a, b) -> tuple[int, int, int]:
    """Return (intersection, |a|, |b|) in a single pass over the masks."""
    a = np.asarray(a, dtype=bool)
    b = np.asarray(b, dtype=bool)
    inter = int(np.count_nonzero(a & b))
    return inter, int(a.sum()), int(b.sum())


def dice(a, b) -> float:
    inter, sa, sb = _overlap_counts(a, b)
    denom = sa + sb
    return 1.0 if denom == 0 else 2.0 * inter / denom


def jaccard(a, b) -> float:
    inter, sa, sb = _overlap_counts(a, b)
    union = sa + sb - inter
    return 1.0 if union == 0 else inter / union


def compare(a, b) -> dict[str, float]:
    """Dice and Jaccard from one shared overlap computation."""
    inter, sa, sb = _overlap_counts(a, b)
    denom = sa + sb
    union = denom - inter
    return {
        "dice_score": 1.0 if denom == 0 else 2.0 * inter / denom,
        "jaccard_score": 1.0 if union == 0 else inter / union,
    }


def mask_stats(mask, spacing_zyx: tuple[float, float, float]) -> dict[str, object]:
    from skimage import measure

    coords = np.argwhere(mask > 0)
    # Physical volume depends on voxel spacing; counting voxels alone is not enough.
    voxel_volume_mm3 = float(np.prod(spacing_zyx))
    stats: dict[str, object] = {
        "voxel_count": int(mask.sum()),
        "volume_mm3": float(mask.sum() * voxel_volume_mm3),
        "volume_ml": float(mask.sum() * voxel_volume_mm3 / 1000.0),
    }
    if coords.size:
        stats["centroid_zyx"] = [float(v) for v in coords.mean(axis=0)]
        stats["bbox_min_zyx"] = [int(v) for v in coords.min(axis=0)]
        stats["bbox_max_zyx"] = [int(v) for v in coords.max(axis=0)]
        try:
            # Marching cubes approximates the mask boundary as a triangle mesh for surface area.
            verts, faces, _, _ = measure.marching_cubes(mask.astype(np.float32), level=0.5, spacing=spacing_zyx)
            stats["surface_area_mm2"] = float(measure.mesh_surface_area(verts, faces))
        except ValueError:
            stats["surface_area_mm2"] = 0.0
    else:
        stats["centroid_zyx"] = None
        stats["bbox_min_zyx"] = None
        stats["bbox_max_zyx"] = None
        stats["surface_area_mm2"] = 0.0
    return stats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Measure one segmentation mask and optionally compare it to another.")
    parser.add_argument("mask", type=Path, help="Predicted or generated mask.")
    parser.add_argument("--reference", type=Path, help="Ground-truth/reference mask for Dice and Jaccard.")
    parser.add_argument("--json-output", type=Path, help="Optional path to save metrics JSON.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    from io_utils import binary_mask, load_volume

    pred_volume = load_volume(args.mask)
    pred = binary_mask(pred_volume.data)
    results = mask_stats(pred, pred_volume.spacing_zyx)

    if args.reference:
        ref = binary_mask(load_volume(args.reference).data)
        if ref.shape != pred.shape:
            raise ValueError(f"Shape mismatch: prediction {pred.shape}, reference {ref.shape}")
        results.update(compare(pred, ref))

    text = json.dumps(results, indent=2)
    print(text)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(text + "\n", encoding="utf-8")
        print(f"Saved metrics: {args.json_output}")


if __name__ == "__main__":
    main()
