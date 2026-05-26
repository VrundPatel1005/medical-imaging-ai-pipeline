#!/usr/bin/env python3
"""Convert a segmentation mask into an STL or OBJ mesh."""

from __future__ import annotations

import argparse
from pathlib import Path


def mask_to_mesh(mask, spacing_zyx: tuple[float, float, float]):
    import numpy as np
    import trimesh
    from skimage import measure

    if mask.sum() == 0:
        raise ValueError("Mask is empty; there is no surface to export.")
    verts, faces, normals, _ = measure.marching_cubes(mask.astype(np.float32), level=0.5, spacing=spacing_zyx)
    return trimesh.Trimesh(vertices=verts, faces=faces, vertex_normals=normals, process=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export a binary segmentation mask as STL or OBJ.")
    parser.add_argument("mask", type=Path, help="Input segmentation mask.")
    parser.add_argument("--output", type=Path, default=Path("data/outputs/segmentation_model.stl"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    from io_utils import binary_mask, load_volume

    volume = load_volume(args.mask)
    mesh = mask_to_mesh(binary_mask(volume.data), volume.spacing_zyx)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(args.output)
    print(f"Saved 3D model: {args.output}")
    print(f"Vertices: {len(mesh.vertices)}")
    print(f"Faces: {len(mesh.faces)}")


if __name__ == "__main__":
    main()
