import os
import sys
import numpy as np
import torch
import rasterio
import matplotlib.pyplot as plt
from rasterio.windows import Window

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.unet import UNet


NDVI_PATH = "satellite/data/outputs/ndvi.tif"
MODEL_PATH = "models/unet_baseline.pth"

OUTPUT_PATH = "inference/outputs/full_segmentation_mask.tif"
PREVIEW_PATH = "inference/outputs/full_segmentation_preview.png"

TILE_SIZE = 256
STRIDE = 256


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=== Full Scene U-Net Inference ===")
print("Device:", device)


model = UNet(in_channels=1, out_channels=1).to(device)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

model.eval()


with rasterio.open(NDVI_PATH) as src:

    width = src.width
    height = src.height

    profile = src.profile.copy()

    full_mask = np.zeros(
        (height, width),
        dtype=np.uint8
    )

    tile_count = 0

    total_rows = (height - TILE_SIZE) // STRIDE + 1
    total_cols = (width - TILE_SIZE) // STRIDE + 1
    total_tiles = total_rows * total_cols

    print("Scene size:", width, "x", height)
    print("Total tiles:", total_tiles)

    for y in range(0, height - TILE_SIZE + 1, STRIDE):

        for x in range(0, width - TILE_SIZE + 1, STRIDE):

            window = Window(
                x,
                y,
                TILE_SIZE,
                TILE_SIZE
            )

            ndvi = src.read(
                1,
                window=window
            )

            if ndvi.shape != (TILE_SIZE, TILE_SIZE):
                continue

            image = ndvi.astype(np.float32)

            input_tensor = (
                torch.from_numpy(image)
                .unsqueeze(0)
                .unsqueeze(0)
                .to(device)
            )

            with torch.no_grad():

                output = model(input_tensor)

                probability = torch.sigmoid(output)

                predicted_mask = (
                    probability > 0.5
                ).float()

            predicted_mask = (
                predicted_mask
                .squeeze()
                .cpu()
                .numpy()
                .astype(np.uint8)
            )

            full_mask[
                y:y + TILE_SIZE,
                x:x + TILE_SIZE
            ] = predicted_mask

            tile_count += 1

            if tile_count % 100 == 0:

                print(
                    f"Processed {tile_count}/{total_tiles} tiles"
                )


profile.update(
    driver="GTiff",
    dtype="uint8",
    count=1,
    nodata=0,
    compress="lzw"
)


with rasterio.open(
    OUTPUT_PATH,
    "w",
    **profile
) as dst:

    dst.write(full_mask, 1)


plt.figure(figsize=(12, 10))

plt.imshow(
    full_mask,
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
print("Mask shape:", full_mask.shape)
print("Mask values:", np.unique(full_mask))
print("GeoTIFF:", OUTPUT_PATH)
print("Preview:", PREVIEW_PATH)