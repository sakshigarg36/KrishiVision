
import os
import numpy as np
import rasterio

NDVI_PATH = "satellite/data/outputs/ndvi.tif"
HEALTH_PATH = "satellite/data/outputs/health_zones.tif"
UNET_PATH = "inference/outputs/full_segmentation_mask.tif"

OUTPUT_PATH = "satellite/data/outputs/combined_gis_health_map.tif"

os.makedirs("satellite/data/outputs", exist_ok=True)


def main():

    print("=== Combined GIS Health Map Generation ===")

    with rasterio.open(NDVI_PATH) as ndvi_src, \
         rasterio.open(HEALTH_PATH) as health_src, \
         rasterio.open(UNET_PATH) as unet_src:

        reference = ndvi_src

        for name, src in [
            ("Health zones", health_src),
            ("U-Net mask", unet_src)
        ]:

            aligned = (
                src.width == reference.width
                and src.height == reference.height
                and src.crs == reference.crs
                and src.transform == reference.transform
            )

            if not aligned:
                raise ValueError(
                    f"{name} raster is not aligned with NDVI"
                )

        profile = reference.profile.copy()

        profile.update(
            driver="GTiff",
            dtype="uint8",
            count=1,
            nodata=255,
            compress="lzw",
            BIGTIFF="IF_SAFER"
        )

        class_counts = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            255: 0
        }

        total_windows = 0

        with rasterio.open(
            OUTPUT_PATH,
            "w",
            **profile
        ) as dst:

            for _, window in reference.block_windows(1):

                ndvi = ndvi_src.read(
                    1,
                    window=window
                )

                zones = health_src.read(
                    1,
                    window=window
                )

                unet = unet_src.read(
                    1,
                    window=window
                )

                valid = (
                    (ndvi_src.read_masks(1, window=window) > 0)
                    & (health_src.read_masks(1, window=window) > 0)
                    & (unet_src.read_masks(1, window=window) > 0)
                    & np.isfinite(ndvi)
                )

                if ndvi_src.nodata is not None:
                    valid &= ndvi != ndvi_src.nodata

                if health_src.nodata is not None:
                    valid &= zones != health_src.nodata

                if unet_src.nodata is not None:
                    valid &= unet != unet_src.nodata

                valid &= np.isin(zones, [0, 1, 2, 3, 4])
                valid &= np.isin(unet, [0, 1])

                result = np.full(
                    ndvi.shape,
                    255,
                    dtype=np.uint8
                )

                non_vegetation = valid & (unet == 0)
                vegetation = valid & (unet == 1)

                result[non_vegetation] = 0

                result[vegetation & (zones <= 1)] = 1
                result[vegetation & (zones == 2)] = 2
                result[vegetation & (zones == 3)] = 3
                result[vegetation & (zones == 4)] = 4

                dst.write(
                    result,
                    1,
                    window=window
                )

                dst.write_mask(
                    valid.astype(np.uint8) * 255,
                    window=window
                )

                values, counts = np.unique(
                    result,
                    return_counts=True
                )

                for value, count in zip(values, counts):
                    class_counts[int(value)] += int(count)

                total_windows += 1

                if total_windows % 100 == 0:
                    print(
                        f"Processed windows: {total_windows}"
                    )

    print("\n=== GIS Health Map Complete ===")
    print("Output:", OUTPUT_PATH)
    print("Total windows:", total_windows)
    print("Pixel distribution:")

    for class_id, count in class_counts.items():
        print(f"Class {class_id}: {count} pixels")

    print("=== Processing Finished ===")


if __name__ == "__main__":
    main()
