
import os
import sys
import numpy as np
import torch
import rasterio
import matplotlib.pyplot as plt

from rasterio.windows import Window
from rasterio.enums import Resampling

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from models.unet import UNet


NDVI_PATH = "satellite/data/outputs/ndvi.tif"
MODEL_PATH = "models/unet_baseline.pth"

OUTPUT_PATH = "inference/outputs/full_segmentation_mask.tif"
PREVIEW_PATH = "inference/outputs/full_segmentation_preview.png"

TILE_SIZE = 256

os.makedirs("inference/outputs", exist_ok=True)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=== Full Scene U-Net Inference ===")
print("Device:", device)

model = UNet(
    in_channels=1,
    out_channels=1
).to(device)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

model.eval()

with rasterio.open(NDVI_PATH) as src:

    width = src.width
    height = src.height

    total_rows = (height + TILE_SIZE - 1) // TILE_SIZE
    total_cols = (width + TILE_SIZE - 1) // TILE_SIZE
    total_tiles = total_rows * total_cols

    print("Scene size:", width, "x", height)
    print("Tile grid:", total_rows, "x", total_cols)
    print("Total tiles:", total_tiles)

    full_mask = np.full(
        (height, width),
        255,
        dtype=np.uint8
    )

    tile_count = 0
    skipped_tiles = 0

    for y in range(0, height, TILE_SIZE):

        for x in range(0, width, TILE_SIZE):

            tile_height = min(TILE_SIZE, height - y)
            tile_width = min(TILE_SIZE, width - x)

            window = Window(
                x,
                y,
                tile_width,
                tile_height
            )

            ndvi = src.read(
                1,
                window=window
            )

            valid_mask = (
                src.read_masks(1, window=window) > 0
            )

            valid_mask &= np.isfinite(ndvi)

            if src.nodata is not None:
                valid_mask &= ndvi != src.nodata

            if not valid_mask.any():
                skipped_tiles += 1
                continue

            image = np.where(
                valid_mask,
                ndvi,
                0.0
            ).astype(np.float32)

            pad_height = TILE_SIZE - tile_height
            pad_width = TILE_SIZE - tile_width

            if pad_height > 0 or pad_width > 0:

                image = np.pad(
                    image,
                    ((0, pad_height), (0, pad_width)),
                    mode="reflect"
                )

            input_tensor = (
                torch.from_numpy(image)
                .unsqueeze(0)
                .unsqueeze(0)
                .to(device)
            )

            with torch.no_grad():

                output = model(input_tensor)

                probability = torch.sigmoid(output)

                prediction = (
                    probability > 0.5
                ).squeeze().cpu().numpy().astype(np.uint8)

            prediction = prediction[
                :tile_height,
                :tile_width
            ]

            tile_result = np.full(
                (tile_height, tile_width),
                255,
                dtype=np.uint8
            )

            tile_result[valid_mask] = prediction[valid_mask]

            full_mask[
                y:y + tile_height,
                x:x + tile_width
            ] = tile_result

            tile_count += 1

            if tile_count % 100 == 0:
                print(
                    f"Processed {tile_count}/{total_tiles} tiles"
                )

    profile = src.profile.copy()

    profile.update(
        driver="GTiff",
        dtype="uint8",
        count=1,
        nodata=255,
        compress="lzw",
        BIGTIFF="IF_SAFER"
    )

    with rasterio.open(
        OUTPUT_PATH,
        "w",
        **profile
    ) as dst:

        dst.write(full_mask, 1)

    preview = src.read(
        1,
        out_shape=(1, 2048, 2048),
        resampling=Resampling.nearest
    )

    mask_preview = full_mask[
        ::max(1, height // 2048),
        ::max(1, width // 2048)
    ][:2048, :2048]

    plt.figure(figsize=(12, 10))

    plt.imshow(
        mask_preview,
        cmap="gray",
        vmin=0,
        vmax=1
    )

    plt.title("Full Scene U-Net Segmentation Mask")
    plt.axis("off")

    plt.savefig(
        PREVIEW_PATH,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    print()
    print("=== Full Scene Inference Complete ===")
    print("Processed tiles:", tile_count)
    print("Skipped tiles:", skipped_tiles)
    print("Expected tiles:", total_tiles)
    print("Mask shape:", full_mask.shape)
    print("Mask values:", np.unique(full_mask))
    print("GeoTIFF:", OUTPUT_PATH)
    print("Preview:", PREVIEW_PATH)
