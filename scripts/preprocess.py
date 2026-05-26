#!/usr/bin/env python3
"""Normalize and optionally resample a medical volume."""

from __future__ import annotations

import argparse
from pathlib import Path


def clip_and_normalize(data, lower: float, upper: float):
    import numpy as np

    clipped = np.clip(data, lower, upper)
    denom = upper - lower
    if denom <= 0:
        raise ValueError("--clip-max must be larger than --clip-min.")
    return ((clipped - lower) / denom).astype(np.float32)


def resample(data, old_spacing_zyx: tuple[float, float, float], new_spacing_zyx: tuple[float, float, float]):
    import scipy.ndimage as ndi

    zoom = tuple(old / new for old, new in zip(old_spacing_zyx, new_spacing_zyx))
    return ndi.zoom(data, zoom=zoom, order=1).astype(np.float32)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preprocess a medical image volume.")
    parser.add_argument("input", type=Path, help="Input .nii/.nii.gz/.nrrd file or DICOM folder.")
    parser.add_argument("--output", type=Path, default=Path("data/processed/preprocessed_scan.nii.gz"))
    parser.add_argument("--clip-min", type=float, default=-1000.0, help="Lower intensity clip value. CT lung default is -1000 HU.")
    parser.add_argument("--clip-max", type=float, default=1000.0, help="Upper intensity clip value.")
    parser.add_argument("--spacing", type=float, nargs=3, metavar=("X", "Y", "Z"), help="Optional target spacing in mm.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    from io_utils import Volume, load_volume, save_nifti

    volume = load_volume(args.input)
    data = clip_and_normalize(volume.data, args.clip_min, args.clip_max)

    reference = volume
    if args.spacing:
        target_xyz = tuple(float(v) for v in args.spacing)
        data = resample(data, volume.spacing_zyx, tuple(reversed(target_xyz)))
        reference = Volume(data=data, affine=volume.affine, spacing_xyz=target_xyz, source=volume.source, modality_hint=volume.modality_hint)

    output = save_nifti(data, reference, args.output)
    print(f"Saved preprocessed scan: {output}")
    print(f"Output shape (z, y, x): {data.shape}")
    print("Intensity range is now approximately 0 to 1.")


if __name__ == "__main__":
    main()
