import os
import numpy as np
import matplotlib.pyplot as plt

IMAGE_PATH = "datasets/segmentation/images/tile_0000.npy"
MASK_PATH = "datasets/segmentation/masks/tile_0000.npy"

OUTPUT_PATH = "datasets/segmentation/segmentation_preview.png"

ndvi = np.load(IMAGE_PATH)
mask = np.load(MASK_PATH)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
axes[0].set_title("NDVI Tile")
axes[0].axis("off")

axes[1].imshow(mask, cmap="gray", vmin=0, vmax=1)
axes[1].set_title("Vegetation Segmentation Mask")
axes[1].axis("off")

plt.tight_layout()

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
plt.close()

print("=== Segmentation Preview Generated ===")
print("Image tile:", IMAGE_PATH)
print("Mask tile:", MASK_PATH)
print("NDVI shape:", ndvi.shape)
print("Mask shape:", mask.shape)
print("Mask values:", np.unique(mask))
print("Preview:", OUTPUT_PATH)