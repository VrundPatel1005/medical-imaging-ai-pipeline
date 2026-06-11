"""Unit tests for the pure segmentation-metric functions.

Run from the project root with:

    pytest

These tests use tiny in-memory arrays only, so they need no dataset download.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# Make scripts/ importable without installing the project.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from metrics import compare, dice, jaccard, mask_stats  # noqa: E402


def test_dice_identical_masks_is_one():
    mask = np.zeros((4, 4, 4), dtype=np.uint8)
    mask[1:3, 1:3, 1:3] = 1
    assert dice(mask, mask) == 1.0
    assert jaccard(mask, mask) == 1.0


def test_disjoint_masks_score_zero():
    a = np.zeros((4, 4, 4), dtype=np.uint8)
    b = np.zeros((4, 4, 4), dtype=np.uint8)
    a[0, 0, 0] = 1
    b[3, 3, 3] = 1
    assert dice(a, b) == 0.0
    assert jaccard(a, b) == 0.0


def test_two_empty_masks_are_defined_as_perfect():
    empty = np.zeros((2, 2, 2), dtype=np.uint8)
    assert dice(empty, empty) == 1.0
    assert jaccard(empty, empty) == 1.0


def test_half_overlap_known_values():
    # Two 2-voxel masks sharing exactly one voxel: Dice = 2*1/(2+2) = 0.5,
    # Jaccard = 1/3.
    a = np.array([1, 1, 0, 0], dtype=np.uint8)
    b = np.array([0, 1, 1, 0], dtype=np.uint8)
    assert dice(a, b) == 0.5
    assert jaccard(a, b) == 1.0 / 3.0


def test_compare_matches_standalone_functions():
    rng = np.random.default_rng(0)
    a = (rng.random((6, 6, 6)) > 0.5).astype(np.uint8)
    b = (rng.random((6, 6, 6)) > 0.5).astype(np.uint8)
    scores = compare(a, b)
    assert scores["dice_score"] == dice(a, b)
    assert scores["jaccard_score"] == jaccard(a, b)


def test_mask_stats_volume_uses_spacing():
    mask = np.zeros((4, 4, 4), dtype=np.uint8)
    mask[1:3, 1:3, 1:3] = 1  # 8 voxels
    spacing_zyx = (2.0, 1.0, 1.0)  # 2 mm^3 per voxel
    stats = mask_stats(mask, spacing_zyx)
    assert stats["voxel_count"] == 8
    assert stats["volume_mm3"] == 16.0
    assert stats["volume_ml"] == 16.0 / 1000.0


def test_mask_stats_empty_mask_is_safe():
    stats = mask_stats(np.zeros((3, 3, 3), dtype=np.uint8), (1.0, 1.0, 1.0))
    assert stats["voxel_count"] == 0
    assert stats["centroid_zyx"] is None
    assert stats["surface_area_mm2"] == 0.0
