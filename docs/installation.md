# Installation Guide

This guide assumes macOS and Python 3.11+. Windows and Linux can also work, but the commands may differ slightly.

## 1. Install Python Tools

From the project folder:

```bash
bash setup.sh
source .venv/bin/activate
```

Check that the scripts are available:

```bash
python scripts/load_scan.py --help
python scripts/visualize.py --help
python scripts/metrics.py --help
```

## 2. Install 3D Slicer

3D Slicer is the main open-source desktop application for this project.

1. Download 3D Slicer from https://download.slicer.org/
2. Install it like a normal macOS app.
3. Open the app.
4. Use **Sample Data** to download a CT chest example.

Why this matters: Slicer gives you the visual workflow used by many medical imaging teams: importing DICOM, viewing slices, painting labels, creating 3D models, and exporting segmentations.

## 3. Install Slicer Extensions

In 3D Slicer:

1. Open **View > Extension Manager**.
2. Search for **TotalSegmentator**.
3. Install it.
4. Search for **MONAILabel**.
5. Install it.
6. Restart 3D Slicer when prompted.

Official extension docs: https://slicer.readthedocs.io/en/latest/user_guide/extensions.html

## 4. Install ITK-SNAP

1. Download ITK-SNAP from https://www.itksnap.org/download/snap/
2. Install the macOS version.
3. Open a NIfTI image and its label file to inspect manual annotations.

Why this matters: ITK-SNAP is widely used for careful manual segmentation and annotation review.

## 5. Install TotalSegmentator For Python

TotalSegmentator is included in `requirements.txt`, but you can reinstall it manually if needed:

```bash
source .venv/bin/activate
pip install totalsegmentator
```

Check the CLI:

```bash
TotalSegmentator --help
```

CPU mode:

```bash
python scripts/segment_ai.py data/raw/ct_scan.nii.gz --cpu --fast
```

GPU mode:

```bash
python scripts/segment_ai.py data/raw/ct_scan.nii.gz --fast
```

CPU is easier to set up and works on most laptops. GPU is faster but depends on your hardware and PyTorch installation.

## 6. MONAI Label Notes

MONAI Label supports interactive AI-assisted annotation workflows. A beginner-friendly first goal is to install the Slicer extension and understand the client/server idea:

- Slicer is the annotation client.
- MONAI Label is the AI server.
- A model suggests labels.
- The annotator corrects the labels.

Quickstart: https://docs.monai.io/projects/label/en/stable/quickstart.html

## Troubleshooting

If `python` is not found, use `python3`.

If a package install fails, upgrade pip:

```bash
python -m pip install --upgrade pip setuptools wheel
```

If TotalSegmentator is slow, add `--fast --cpu` first. The first run may download model weights.

If DICOM loading fails, first load the DICOM folder in 3D Slicer, then export it as NIfTI and use the Python scripts on the `.nii.gz` file.

