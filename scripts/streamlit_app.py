"""Streamlit dashboard for segmentation overlays and metrics."""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from io_utils import binary_mask, center_slice_index, load_volume
from metrics import dice, jaccard, mask_stats
from visualize import normalize_for_display


def save_upload(uploaded_file) -> Path:
    suffix = ".nii.gz" if uploaded_file.name.endswith(".nii.gz") else Path(uploaded_file.name).suffix
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp.write(uploaded_file.getbuffer())
    temp.close()
    return Path(temp.name)


st.set_page_config(page_title="Medical Segmentation Dashboard", layout="wide")
st.title("AI-Assisted Medical Image Segmentation Dashboard")
st.caption("Educational portfolio tool only. Not for diagnosis or clinical decision-making.")

image_upload = st.sidebar.file_uploader("Upload image NIfTI", type=["nii", "gz"])
mask_upload = st.sidebar.file_uploader("Upload mask NIfTI", type=["nii", "gz"])
reference_upload = st.sidebar.file_uploader("Optional reference mask", type=["nii", "gz"])

if not image_upload:
    st.info("Upload a NIfTI image to begin. Try an MSD Task09 Spleen image after downloading the dataset.")
else:
    image_volume = load_volume(save_upload(image_upload))
    image = image_volume.data
    mask = None
    if mask_upload:
        mask = binary_mask(load_volume(save_upload(mask_upload)).data)
        if mask.shape != image.shape:
            st.error(f"Image shape {image.shape} does not match mask shape {mask.shape}.")
            st.stop()

    default_slice = center_slice_index(mask if mask is not None else image)
    slice_index = st.sidebar.slider("Axial slice", 0, image.shape[0] - 1, default_slice)

    left, right = st.columns([2, 1])
    with left:
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.imshow(normalize_for_display(image[slice_index]), cmap="gray")
        if mask is not None:
            overlay = np.ma.masked_where(mask[slice_index] == 0, mask[slice_index])
            ax.imshow(overlay, cmap="autumn", alpha=0.55)
        ax.axis("off")
        ax.set_title(f"Slice {slice_index}")
        st.pyplot(fig)

    with right:
        st.subheader("Scan Metadata")
        st.write({"shape_zyx": image.shape, "spacing_xyz_mm": image_volume.spacing_xyz})
        if mask is not None:
            st.subheader("Mask Metrics")
            stats = mask_stats(mask, image_volume.spacing_zyx)
            st.json(stats)
            if reference_upload:
                ref = binary_mask(load_volume(save_upload(reference_upload)).data)
                if ref.shape == mask.shape:
                    st.metric("Dice", f"{dice(mask, ref):.4f}")
                    st.metric("Jaccard", f"{jaccard(mask, ref):.4f}")
                else:
                    st.warning("Reference mask shape does not match.")
