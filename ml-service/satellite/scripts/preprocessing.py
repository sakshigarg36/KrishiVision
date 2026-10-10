import numpy as np
import rasterio


def load_band(path):
    with rasterio.open(path) as src:
        band = src.read(1).astype("float32")
        profile = src.profile.copy()

    band = band / 10000.0

    return band, profile


def load_red_nir(red_path, nir_path):
    red, red_profile = load_band(red_path)
    nir, nir_profile = load_band(nir_path)

    if red.shape != nir.shape:
        raise ValueError("Red and NIR images must have the same shape.")

    return red, nir, red_profile