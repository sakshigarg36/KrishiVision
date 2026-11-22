
import numpy as np
import rasterio


def load_band(path):
    with rasterio.open(path) as src:
        band = src.read(1).astype("float32")

        valid_mask = (
            src.dataset_mask().astype(bool)
            & np.isfinite(band)
        )

        profile = src.profile.copy()
        crs = src.crs
        transform = src.transform

    band = band / 10000.0
    band[~valid_mask] = np.nan

    return band, profile, valid_mask, crs, transform


def load_red_nir(red_path, nir_path):
    red, red_profile, red_mask, red_crs, red_transform = load_band(red_path)

    nir, nir_profile, nir_mask, nir_crs, nir_transform = load_band(nir_path)

    if red.shape != nir.shape:
        raise ValueError("Red and NIR images must have the same shape.")

    if red_crs != nir_crs:
        raise ValueError("Red and NIR CRS must match.")

    if red_transform != nir_transform:
        raise ValueError("Red and NIR transforms must match.")

    valid_mask = red_mask & nir_mask

    return red, nir, red_profile, valid_mask
