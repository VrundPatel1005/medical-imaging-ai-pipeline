# Portfolio Notes

Use this language honestly. The goal is to show practical exposure and learning, not to imply clinical deployment.

## LinkedIn Project Post

I built a beginner-friendly medical imaging AI portfolio project: **AI-Assisted Medical Image Segmentation & 3D Reconstruction Pipeline**.

The project walks through a full research-style workflow using open-source tools: 3D Slicer, ITK-SNAP, TotalSegmentator, MONAI/PyTorch, SimpleITK, nibabel, and Python.

What I practiced:

- Loading DICOM and NIfTI medical imaging data.
- Creating manual and semi-automatic segmentation masks.
- Running AI-assisted CT segmentation with TotalSegmentator.
- Visualizing segmentation overlays.
- Computing segmentation metrics like Dice, Jaccard, volume, and surface area.
- Exporting segmentation masks as STL/OBJ 3D anatomy models.
- Documenting an end-to-end healthcare AI data workflow.

This project helped me understand how annotation, segmentation, quality control, and 3D reconstruction fit into medical imaging AI pipelines.

Keywords: Medical Imaging, Healthcare AI, DICOM, NIfTI, 3D Slicer, ITK-SNAP, TotalSegmentator, MONAI, Segmentation, Annotation, AI Data Operations.

## Resume Bullets

- Built a Python-based medical imaging segmentation pipeline for DICOM/NIfTI loading, preprocessing, overlay visualization, segmentation metrics, and STL/OBJ 3D model export.
- Used 3D Slicer, ITK-SNAP, and TotalSegmentator to practice manual, semi-automatic, and AI-assisted CT segmentation workflows on public medical imaging datasets.
- Implemented segmentation quality analysis including voxel volume, surface area, Dice score, Jaccard score, centroid, and bounding-box statistics.
- Created a Streamlit dashboard for interactive slice review, segmentation overlay inspection, and beginner-friendly metric reporting.
- Documented a reproducible healthcare AI workflow with setup instructions, dataset guidance, troubleshooting, and portfolio-ready presentation materials.

## Portfolio Description

This project demonstrates an end-to-end medical imaging AI workflow for educational and research portfolio use. It combines open-source clinical imaging tools with Python automation to load CT/MRI scans, create and compare segmentation masks, generate overlays, compute metrics, and export 3D anatomical models. The project emphasizes practical familiarity with DICOM/NIfTI workflows, annotation tooling, AI-assisted segmentation, and quality-control concepts used in healthcare AI data operations.

## Short Elevator Pitch

I built a medical imaging AI pipeline that takes public CT/MRI scans from DICOM or NIfTI format, supports manual and AI-assisted segmentation, compares mask quality with metrics like Dice and volume, and exports 3D anatomical STL models for visualization.

## Honest Skill Framing

Good wording:

- "Practiced AI-assisted segmentation workflows using TotalSegmentator."
- "Built a portfolio pipeline for medical image loading, visualization, metrics, and 3D export."
- "Gained hands-on exposure to 3D Slicer, ITK-SNAP, DICOM, NIfTI, and segmentation masks."

Avoid overstating:

- Do not say the model is clinically validated.
- Do not say it diagnoses disease.
- Do not claim production hospital deployment.

## Screenshot Captions

- "3D Slicer CT volume loaded from public sample data."
- "Manual segmentation review in Segment Editor."
- "AI-assisted segmentation generated with TotalSegmentator."
- "Python overlay showing mask alignment on axial CT slice."
- "3D STL reconstruction exported from binary segmentation mask."
- "Streamlit dashboard for slice review and segmentation metrics."

