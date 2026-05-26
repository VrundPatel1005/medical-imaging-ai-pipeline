# AI-Assisted Medical Image Segmentation & 3D Reconstruction Pipeline

Beginner-to-intermediate medical imaging project using 3D Slicer, ITK-SNAP, TotalSegmentator, MONAI, Python, DICOM, NIfTI, segmentation metrics, and 3D mesh export.

> Research prototype only. This repository is not intended for diagnosis, treatment planning, or clinical decision-making.

## Project Objectives

- Load CT/MRI scans from DICOM folders, NIfTI files, and NRRD files.
- Create manual and semi-automatic segmentation baselines.
- Run AI-assisted CT segmentation with TotalSegmentator.
- Visualize 2D slices, segmentation overlays, and output masks.
- Export segmentation masks as STL/OBJ 3D anatomy models.
- Compute beginner-friendly segmentation statistics and comparison metrics.
- Document a complete workflow suitable for healthcare AI and data operations review.

## Tools Used

- **3D Slicer**: DICOM import, Segment Editor, 3D rendering, STL export.
- **ITK-SNAP**: manual annotation and slice-by-slice segmentation review.
- **TotalSegmentator**: AI-assisted CT segmentation of over 100 anatomical structures.
- **Python 3.11+**: automation, visualization, metrics, and reproducible workflows.
- **MONAI / PyTorch**: healthcare AI ecosystem exposure.
- **nibabel / SimpleITK**: NIfTI, NRRD, and DICOM image handling.
- **scikit-image / trimesh**: marching cubes and mesh export.
- **Streamlit**: optional mini-dashboard for overlays and metrics.

## Workflow

```text
Public CT/MRI data
      |
      v
DICOM or NIfTI loading
      |
      v
Preprocessing and scan inspection
      |
      +--> Manual/semi-auto mask in 3D Slicer or ITK-SNAP
      |
      +--> AI-assisted mask with TotalSegmentator
      |
      v
Metrics, overlay visualization, 3D mesh export
      |
      v
GitHub screenshots, LinkedIn post, resume bullets
```

## Recommended Public Datasets

1. **3D Slicer CT-chest sample data**
   - Best first dataset for practicing Slicer loading, rendering, and segmentation.
   - Link: https://www.slicer.org/wiki/SampleData

2. **Medical Segmentation Decathlon Task09 Spleen**
   - Main project dataset because it includes CT scans and reference spleen masks.
   - Link: https://medicaldecathlon.com/
   - Download index: https://medicaldecathlon.com/dataaws/
   - Expected layout after download:

```text
data/raw/Task09_Spleen/
├── imagesTr/
│   ├── spleen_2.nii.gz
│   └── ...
└── labelsTr/
    ├── spleen_2.nii.gz
    └── ...
```

3. **TCIA collections**
   - Useful for DICOM practice after the NIfTI workflow is comfortable.
   - Link: https://www.cancerimagingarchive.net/

## Installation

```bash
cd medical-imaging-ai-pipeline
bash setup.sh
source .venv/bin/activate
```

For full app walkthroughs, read:

- `docs/installation.md`
- `docs/workflow.md`
- `docs/project_notes.md`

## Quick Start With A NIfTI Scan

Inspect a scan:

```bash
python scripts/load_scan.py data/raw/Task09_Spleen/imagesTr/spleen_2.nii.gz
```

Create a simple baseline segmentation:

```bash
python scripts/segment_manual.py \
  data/raw/Task09_Spleen/imagesTr/spleen_2.nii.gz \
  --output data/outputs/manual_mask.nii.gz \
  --lower 20 --upper 200 --largest-component
```

Visualize an overlay:

```bash
python scripts/visualize.py \
  data/raw/Task09_Spleen/imagesTr/spleen_2.nii.gz \
  --mask data/outputs/manual_mask.nii.gz \
  --output data/outputs/manual_overlay.png
```

Compare against an MSD reference mask:

```bash
python scripts/metrics.py \
  data/outputs/manual_mask.nii.gz \
  --reference data/raw/Task09_Spleen/labelsTr/spleen_2.nii.gz \
  --json-output data/outputs/manual_metrics.json
```

Export a 3D model:

```bash
python scripts/export_3d_model.py \
  data/outputs/manual_mask.nii.gz \
  --output data/outputs/manual_spleen.stl
```

Run the dashboard:

```bash
streamlit run scripts/streamlit_app.py
```

For the included MSD Task09 Spleen workflow, upload these files in the dashboard:

```text
Image: data/raw/Task09_Spleen/imagesTr/spleen_2.nii.gz
Mask:  data/raw/Task09_Spleen/labelsTr/spleen_2.nii.gz
```

## TotalSegmentator Example

TotalSegmentator is designed for CT scans and can segment more than 100 anatomical structures. CPU mode works but can be slow; GPU mode is faster if your PyTorch installation and hardware support it.

Preview the command:

```bash
python scripts/segment_ai.py data/raw/ct_scan.nii.gz --output-dir data/outputs/totalseg --cpu --fast --preview
```

Run AI-assisted segmentation:

```bash
python scripts/segment_ai.py data/raw/ct_scan.nii.gz --output-dir data/outputs/totalseg --cpu --fast
```

Compare an AI-generated spleen mask to the MSD human/reference label:

```bash
python scripts/metrics.py \
  data/outputs/totalseg/spleen.nii.gz \
  --reference data/raw/Task09_Spleen/labelsTr/spleen_2.nii.gz
```

This is the AI-assisted part of the project: TotalSegmentator proposes anatomy masks, then the project reviews, measures, visualizes, and exports them.

## Screenshots To Add

Place final project images in `screenshots/`:

- 3D Slicer DICOM browser or loaded CT volume.
- 3D Slicer Segment Editor with manual mask.
- 3D Slicer 3D reconstruction view.
- ITK-SNAP annotation view.
- Python overlay generated by `visualize.py`.
- Streamlit dashboard with metrics.
- STL/OBJ model opened in 3D Slicer or another mesh viewer.

## Learning Outcomes

This project demonstrates practical exposure to:

- DICOM and NIfTI medical imaging formats.
- Manual, semi-automatic, and AI-assisted segmentation workflows.
- Medical image preprocessing and visualization.
- Segmentation quality metrics such as Dice and Jaccard.
- 3D reconstruction and STL/OBJ export.
- Reproducible Python tooling for healthcare AI data workflows.

## Future Improvements

- Add MONAI Label server/client examples for interactive annotation.
- Train a lightweight MONAI 3D U-Net on a tiny subset of MSD data.
- Add batch processing for entire dataset folders.
- Add richer mesh cleanup controls.
- Add experiment tracking with CSV or MLflow.

## Keywords

Medical Imaging, Healthcare AI, DICOM, NIfTI, CT Segmentation, 3D Slicer, ITK-SNAP, TotalSegmentator, MONAI, PyTorch, Annotation, Data Operations, 3D Reconstruction, STL Export.
