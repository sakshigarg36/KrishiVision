import numpy as np
import rasterio

from preprocessing import load_red_nir


RED_PATH = "satellite/data/bands/B04_10m.jp2"
NIR_PATH = "satellite/data/bands/B08_10m.jp2"

NDVI_OUTPUT = "satellite/data/outputs/ndvi.tif"
HEALTH_OUTPUT = "satellite/data/outputs/health_zones.tif"


def calculate_ndvi(red, nir):
    denominator = nir + red

    ndvi = np.divide(
        nir - red,
        denominator,
        out=np.zeros_like(nir, dtype="float32"),
        where=denominator != 0
    )

    ndvi = np.clip(ndvi, -1.0, 1.0)

    return ndvi


def classify_health_zones(ndvi):
    zones = np.zeros(ndvi.shape, dtype=np.uint8)

    zones[(ndvi >= 0.0) & (ndvi < 0.2)] = 1
    zones[(ndvi >= 0.2) & (ndvi < 0.4)] = 2
    zones[(ndvi >= 0.4) & (ndvi < 0.6)] = 3
    zones[(ndvi >= 0.6) & (ndvi <= 1.0)] = 4

    return zones


def main():
    red, nir, profile = load_red_nir(
        RED_PATH,
        NIR_PATH
    )

    ndvi = calculate_ndvi(red, nir)
    health_zones = classify_health_zones(ndvi)

    ndvi_profile = profile.copy()
    ndvi_profile.update(driver="GTiff")
    ndvi_profile.update(
        dtype="float32",
        count=1,
        compress="lzw"
    )

    with rasterio.open(
        NDVI_OUTPUT,
        "w",
        **ndvi_profile
    ) as dst:
        dst.write(ndvi, 1)

    health_profile = profile.copy()
    health_profile.update(driver="GTiff")
    health_profile.update(
        dtype="uint8",
        count=1,
        compress="lzw"
    )

    with rasterio.open(
        HEALTH_OUTPUT,
        "w",
        **health_profile
    ) as dst:
        dst.write(health_zones, 1)

    print("=== NDVI Generation Complete ===")
    print("NDVI shape:", ndvi.shape)
    print("NDVI min:", ndvi.min())
    print("NDVI max:", ndvi.max())
    print("NDVI mean:", ndvi.mean())
    print("Health zones:", np.unique(health_zones))
    print("NDVI output:", NDVI_OUTPUT)
    print("Health zones output:", HEALTH_OUTPUT)


if __name__ == "__main__":
    main()