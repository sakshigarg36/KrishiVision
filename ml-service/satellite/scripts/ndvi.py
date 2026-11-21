
import numpy as np
import rasterio

from preprocessing import load_red_nir


RED_PATH = "satellite/data/bands/B04_10m.jp2"
NIR_PATH = "satellite/data/bands/B08_10m.jp2"

NDVI_OUTPUT = "satellite/data/outputs/ndvi.tif"
HEALTH_OUTPUT = "satellite/data/outputs/health_zones.tif"


def calculate_ndvi(red, nir, valid_mask):
    denominator = nir + red

    valid_mask = (
        valid_mask
        & np.isfinite(red)
        & np.isfinite(nir)
        & (denominator != 0)
    )

    ndvi = np.full(red.shape, np.nan, dtype=np.float32)

    np.divide(
        nir - red,
        denominator,
        out=ndvi,
        where=valid_mask
    )

    ndvi[valid_mask] = np.clip(
        ndvi[valid_mask], -1.0, 1.0
    )

    return ndvi, valid_mask


def classify_health_zones(ndvi, valid_mask):
    zones = np.zeros(ndvi.shape, dtype=np.uint8)

    zones[valid_mask & (ndvi < 0.0)] = 0
    zones[valid_mask & (ndvi >= 0.0) & (ndvi < 0.2)] = 1
    zones[valid_mask & (ndvi >= 0.2) & (ndvi < 0.4)] = 2
    zones[valid_mask & (ndvi >= 0.4) & (ndvi < 0.6)] = 3
    zones[valid_mask & (ndvi >= 0.6)] = 4

    return zones


def main():
    red, nir, profile, valid_mask = load_red_nir(
        RED_PATH,
        NIR_PATH
    )

    ndvi, valid_mask = calculate_ndvi(
        red, nir, valid_mask
    )

    health_zones = classify_health_zones(
        ndvi, valid_mask
    )

    ndvi_profile = profile.copy()
    ndvi_profile.update(
        driver="GTiff",
        dtype="float32",
        count=1,
        compress="lzw",
        nodata=-9999.0
    )

    ndvi_output = np.where(
        valid_mask, ndvi, -9999.0
    ).astype(np.float32)

    with rasterio.open(
        NDVI_OUTPUT,
        "w",
        **ndvi_profile
    ) as dst:
        dst.write(ndvi_output, 1)
        dst.write_mask(valid_mask.astype(np.uint8) * 255)

    health_profile = profile.copy()
    health_profile.update(
        driver="GTiff",
        dtype="uint8",
        count=1,
        compress="lzw",
        nodata=255
    )

    zone_output = np.where(
        valid_mask, health_zones, 255
    ).astype(np.uint8)

    with rasterio.open(
        HEALTH_OUTPUT,
        "w",
        **health_profile
    ) as dst:
        dst.write(zone_output, 1)
        dst.write_mask(valid_mask.astype(np.uint8) * 255)

    print("=== NDVI Generation Complete ===")
    print("Shape:", ndvi.shape)
    print("Valid pixels:", int(valid_mask.sum()))
    print("Invalid pixels:", int((~valid_mask).sum()))

    if valid_mask.any():
        print("NDVI min:", float(np.min(ndvi[valid_mask])))
        print("NDVI max:", float(np.max(ndvi[valid_mask])))
        print("NDVI mean:", float(np.mean(ndvi[valid_mask])))

    print("Health zones:", np.unique(health_zones[valid_mask]))
    print("NDVI output:", NDVI_OUTPUT)
    print("Health zones output:", HEALTH_OUTPUT)


if __name__ == "__main__":
    main()
