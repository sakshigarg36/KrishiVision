
import os
import numpy as np
import rasterio
from rasterio.windows import Window

NDVI_PATH = "satellite/data/outputs/ndvi.tif"

IMAGE_DIR = "datasets/segmentation/images"
MASK_DIR = "datasets/segmentation/masks"

TILE_SIZE = 256

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(MASK_DIR, exist_ok=True)


def create_tiles():

    tile_count = 0
    skipped_tiles = 0

    with rasterio.open(NDVI_PATH) as src:

        width = src.width
        height = src.height

        total_rows = (height + TILE_SIZE - 1) // TILE_SIZE
        total_cols = (width + TILE_SIZE - 1) // TILE_SIZE

        for y in range(0, height, TILE_SIZE):

            for x in range(0, width, TILE_SIZE):

                tile_width = min(TILE_SIZE, width - x)
                tile_height = min(TILE_SIZE, height - y)

                window = Window(
                    x,
                    y,
                    tile_width,
                    tile_height
                )

                ndvi = src.read(1, window=window)
                valid_mask = src.read_masks(1, window=window) > 0

                valid_mask &= np.isfinite(ndvi)

                if src.nodata is not None:
                    valid_mask &= ndvi != src.nodata

                if not valid_mask.any():
                    skipped_tiles += 1
                    continue

                pad_height = TILE_SIZE - tile_height
                pad_width = TILE_SIZE - tile_width

                if pad_height > 0 or pad_width > 0:

                    ndvi = np.pad(
                        ndvi,
                        ((0, pad_height), (0, pad_width)),
                        mode="reflect"
                    )

                    valid_mask = np.pad(
                        valid_mask,
                        ((0, pad_height), (0, pad_width)),
                        mode="reflect"
                    )

                vegetation_mask = (
                    (ndvi >= 0.2) &
                    (ndvi <= 1.0) &
                    valid_mask
                ).astype(np.uint8)

                image_output = np.where(
                    valid_mask,
                    ndvi,
                    0.0
                ).astype(np.float32)

                tile_name = f"tile_{tile_count:04d}.npy"

                np.save(
                    os.path.join(IMAGE_DIR, tile_name),
                    image_output
                )

                np.save(
                    os.path.join(MASK_DIR, tile_name),
                    vegetation_mask
                )

                tile_count += 1

    print("=== Segmentation Dataset Created ===")
    print("Tile size:", TILE_SIZE)
    print("Expected grid:", total_rows, "x", total_cols)
    print("Total tiles:", tile_count)
    print("Skipped tiles:", skipped_tiles)
    print("Images:", IMAGE_DIR)
    print("Masks:", MASK_DIR)


if __name__ == "__main__":
    create_tiles()
