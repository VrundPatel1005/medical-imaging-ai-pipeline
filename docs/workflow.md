# Workflow Guide

This document explains the complete beginner workflow from medical image loading to 3D model export.

## Core Concepts

**DICOM** is the standard format used by scanners and hospitals. A single CT scan is often stored as a folder of many `.dcm` slice files.

**NIfTI** is a research-friendly format. A full 3D scan is usually stored as one `.nii` or `.nii.gz` file.

**Segmentation mask** is an image where each voxel label says what anatomy or object the voxel belongs to. A binary mask uses `0` for background and `1` for the target structure.

## Beginner Workflow

1. Download a public dataset.
2. Load the scan in 3D Slicer.
3. Inspect axial, coronal, and sagittal views.
4. Create a manual or semi-automatic segmentation.
5. Export the segmentation as NIfTI.
6. Run Python metrics and visualization.
7. Export a 3D mesh as STL or OBJ.
8. Capture screenshots for GitHub and LinkedIn.

## 3D Slicer Walkthrough

### Load Sample CT Data

1. Open 3D Slicer.
2. Open **Sample Data**.
3. Download **CTChest** or another CT sample.
4. Use the slice views to scroll through the scan.

### Import DICOM Data

1. Open **DICOM** from the toolbar.
2. Click **Import**.
3. Select the folder containing DICOM files.
4. Choose the detected series.
5. Click **Load**.

Official data loading docs: https://slicer.readthedocs.io/en/5.4/user_guide/data_loading_and_saving.html

### Manual Segmentation

1. Open **Segment Editor**.
2. Click **Add** to create a segment.
3. Use **Paint** or **Draw** to mark anatomy on slices.
4. Use **Erase** to clean mistakes.
5. Toggle 3D visibility to inspect the reconstruction.

### Semi-Automatic Segmentation

Useful Segment Editor tools:

- **Threshold**: selects voxels within an intensity range.
- **Grow from seeds**: expands labels from user-marked seed regions.
- **Islands**: removes small disconnected components.
- **Smoothing**: cleans jagged surfaces.

Official segmentation docs: https://slicer.readthedocs.io/en/latest/user_guide/image_segmentation.html

### Export STL

1. In Segment Editor, finish your segment.
2. Open **Segmentations** module.
3. Use **Export to files**.
4. Choose STL or OBJ.
5. Save the mesh into `data/outputs/` or `screenshots/` for project review.

## ITK-SNAP Walkthrough

1. Open ITK-SNAP.
2. Load a main image, such as `spleen_2.nii.gz`.
3. Load a segmentation label, such as the matching MSD label file.
4. Review how masks line up with anatomy.
5. Practice manual correction on a copy of the mask.

ITK-SNAP is especially useful for careful review of annotation quality.

## Python Workflow

Inspect a scan:

```bash
python scripts/load_scan.py data/raw/Task09_Spleen/imagesTr/spleen_2.nii.gz
```

Create a simple threshold baseline:

```bash
python scripts/segment_manual.py data/raw/Task09_Spleen/imagesTr/spleen_2.nii.gz --lower 20 --upper 200 --largest-component
```

Create an overlay:

```bash
python scripts/visualize.py data/raw/Task09_Spleen/imagesTr/spleen_2.nii.gz --mask data/outputs/manual_mask.nii.gz
```

Measure a mask:

```bash
python scripts/metrics.py data/outputs/manual_mask.nii.gz --reference data/raw/Task09_Spleen/labelsTr/spleen_2.nii.gz
```

Export a mesh:

```bash
python scripts/export_3d_model.py data/outputs/manual_mask.nii.gz --output data/outputs/model.stl
```

## TotalSegmentator Workflow

TotalSegmentator automatically segments many CT anatomy classes. It is best used on CT scans, not arbitrary MRI scans.

Preview:

```bash
python scripts/segment_ai.py data/raw/ct_scan.nii.gz --output-dir data/outputs/totalseg --cpu --fast --preview
```

Run:

```bash
python scripts/segment_ai.py data/raw/ct_scan.nii.gz --output-dir data/outputs/totalseg --cpu --fast
```

The output directory will contain many organ and structure masks. Choose one mask and compare or export it:

```bash
python scripts/export_3d_model.py data/outputs/totalseg/spleen.nii.gz --output data/outputs/ai_spleen.stl
```

## Screenshot Checklist

Capture:

- Loaded CT/MRI in 3D Slicer.
- Segment Editor with a visible mask.
- Before and after manual cleanup.
- TotalSegmentator extension result.
- ITK-SNAP label review.
- Python overlay PNG.
- Streamlit dashboard.
- Exported STL model in a 3D viewer.

These screenshots become the visual proof that you completed the workflow.
