import os
import numpy as np
import rasterio
from rasterio.windows import Window

NDVI_PATH = "satellite/data/outputs/ndvi.tif"

IMAGE_DIR = "datasets/segmentation/images"
MASK_DIR = "datasets/segmentation/masks"

TILE_SIZE = 256
STRIDE = 256

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(MASK_DIR, exist_ok=True)


def create_tiles():
    with rasterio.open(NDVI_PATH) as src:
        width = src.width
        height = src.height

        tile_count = 0

        for y in range(0, height - TILE_SIZE + 1, STRIDE):
            for x in range(0, width - TILE_SIZE + 1, STRIDE):

                window = Window(x, y, TILE_SIZE, TILE_SIZE)
                ndvi = src.read(1, window=window)

                if ndvi.shape != (TILE_SIZE, TILE_SIZE):
                    continue

                image_path = os.path.join(
                    IMAGE_DIR,
                    f"tile_{tile_count:04d}.npy"
                )

                mask_path = os.path.join(
                    MASK_DIR,
                    f"tile_{tile_count:04d}.npy"
                )

                vegetation_mask = (
                    (ndvi >= 0.2) &
                    (ndvi <= 1.0)
                ).astype(np.uint8)

                np.save(image_path, ndvi.astype(np.float32))
                np.save(mask_path, vegetation_mask)

                tile_count += 1

        print("=== Segmentation Dataset Created ===")
        print("Tile size:", TILE_SIZE)
        print("Total tiles:", tile_count)
        print("Images:", IMAGE_DIR)
        print("Masks:", MASK_DIR)


if __name__ == "__main__":
    create_tiles()