import numpy as np
import rasterio


def calculate_ndvi(red_path, nir_path, output_path):
    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype("float32")
        profile = red_src.profile

    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype("float32")

    if red.shape != nir.shape:
        raise ValueError("Red and NIR images must have the same shape.")

    denominator = nir + red

    ndvi = np.divide(
        nir - red,
        denominator,
        out=np.zeros_like(nir, dtype="float32"),
        where=denominator != 0
    )

    ndvi = np.clip(ndvi, -1.0, 1.0)

    profile.update(
        dtype="float32",
        count=1,
        compress="lzw"
    )

    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(ndvi, 1)

    return ndvi

def classify_health_zones(ndvi):
    zones = np.zeros(ndvi.shape, dtype=np.uint8)

    zones[(ndvi >= 0.0) & (ndvi < 0.2)] = 1
    zones[(ndvi >= 0.2) & (ndvi < 0.4)] = 2
    zones[(ndvi >= 0.4) & (ndvi < 0.6)] = 3
    zones[(ndvi >= 0.6) & (ndvi <= 1.0)] = 4

    return zones