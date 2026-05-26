#!/usr/bin/env python3
"""Load a DICOM folder, NIfTI file, or NRRD file and print scan metadata."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a CT/MRI scan stored as DICOM, NIfTI, or NRRD."
    )
    parser.add_argument("input", type=Path, help="Path to .nii/.nii.gz/.nrrd file or DICOM folder.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    import shlex

    import numpy as np

    from io_utils import load_volume

    volume = load_volume(args.input)
    data = volume.data

    print("\nMedical scan loaded successfully")
    print(f"Source: {volume.source}")
    print(f"Format hint: {volume.modality_hint}")
    print(f"Array shape (z, y, x): {data.shape}")
    print(f"Voxel spacing (x, y, z) mm: {tuple(round(v, 4) for v in volume.spacing_xyz)}")
    print(f"Intensity min/max: {float(np.nanmin(data)):.3f} / {float(np.nanmax(data)):.3f}")
    print(f"Intensity mean/std: {float(np.nanmean(data)):.3f} / {float(np.nanstd(data)):.3f}")
    print("Affine matrix:")
    print(np.array2string(volume.affine, precision=3, suppress_small=True))
    print("\nNext step example:")
    print(f"python scripts/visualize.py {shlex.quote(str(volume.source))} --output data/outputs/scan_preview.png")


if __name__ == "__main__":
    main()
