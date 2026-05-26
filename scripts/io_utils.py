"""Shared medical image loading and saving helpers.

The scripts in this project keep data handling simple on purpose:
SimpleITK is used for robust DICOM/NRRD/NIfTI reading, while nibabel is used
for NIfTI writing that is easy to inspect from Python notebooks.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import nibabel as nib
import numpy as np
import SimpleITK as sitk


@dataclass(frozen=True)
class Volume:
    data: np.ndarray
    affine: np.ndarray
    spacing_xyz: tuple[float, float, float]
    source: Path
    modality_hint: str

    @property
    def spacing_zyx(self) -> tuple[float, float, float]:
        return tuple(reversed(self.spacing_xyz))


def is_nifti(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".nii") or name.endswith(".nii.gz")


def load_volume(path: str | Path) -> Volume:
    """Load a NIfTI/NRRD file or DICOM directory as a z, y, x NumPy volume."""

    source = Path(path).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Input path does not exist: {source}")

    if source.is_dir():
        reader = sitk.ImageSeriesReader()
        series_ids = reader.GetGDCMSeriesIDs(str(source))
        if not series_ids:
            raise ValueError(
                f"No DICOM series found in {source}. "
                "Point this argument at a folder containing .dcm slices."
            )
        file_names = reader.GetGDCMSeriesFileNames(str(source), series_ids[0])
        reader.SetFileNames(file_names)
        image = reader.Execute()
        data = sitk.GetArrayFromImage(image).astype(np.float32)
        spacing_xyz = tuple(float(v) for v in image.GetSpacing())
        affine = affine_from_sitk(image)
        return Volume(data, affine, spacing_xyz, source, "DICOM")

    if is_nifti(source):
        nii = nib.load(str(source))
        data_xyz = nii.get_fdata(dtype=np.float32)
        # nibabel exposes NIfTI as x, y, z; the project uses z, y, x for slice-first workflows.
        data = np.transpose(data_xyz, (2, 1, 0))
        spacing_xyz = tuple(float(v) for v in nii.header.get_zooms()[:3])
        return Volume(data, nii.affine, spacing_xyz, source, "NIfTI")

    image = sitk.ReadImage(str(source))
    data = sitk.GetArrayFromImage(image).astype(np.float32)
    spacing_xyz = tuple(float(v) for v in image.GetSpacing())
    return Volume(data, affine_from_sitk(image), spacing_xyz, source, source.suffix.upper())


def affine_from_sitk(image: sitk.Image) -> np.ndarray:
    spacing = np.array(image.GetSpacing(), dtype=float)
    origin = np.array(image.GetOrigin(), dtype=float)
    direction = np.array(image.GetDirection(), dtype=float).reshape(3, 3)
    affine = np.eye(4, dtype=float)
    affine[:3, :3] = direction @ np.diag(spacing)
    affine[:3, 3] = origin
    return affine


def save_nifti(data_zyx: np.ndarray, reference: Volume, output_path: str | Path) -> Path:
    """Save a z, y, x array as NIfTI using the reference affine."""

    output = Path(output_path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Convert back to x, y, z before writing so external tools read the file correctly.
    data_xyz = np.transpose(data_zyx, (2, 1, 0))
    img = nib.Nifti1Image(data_xyz.astype(np.float32), reference.affine)
    img.header.set_zooms(reference.spacing_xyz)
    nib.save(img, str(output))
    return output


def binary_mask(data: np.ndarray) -> np.ndarray:
    return (np.asarray(data) > 0).astype(np.uint8)


def center_slice_index(mask_or_image: np.ndarray) -> int:
    nonzero = np.argwhere(mask_or_image > 0)
    if nonzero.size == 0:
        return int(mask_or_image.shape[0] // 2)
    return int(np.median(nonzero[:, 0]))
