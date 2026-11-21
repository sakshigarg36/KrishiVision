
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from rasterio.enums import Resampling

INPUT_PATH = "satellite/data/outputs/combined_gis_health_map.tif"
OUTPUT_PATH = "satellite/data/outputs/combined_gis_health_map_preview.png"

print("=== Generating Combined GIS Health Map Preview ===")

with rasterio.open(INPUT_PATH) as src:
    # Read a smaller version for faster visualization
    preview = src.read(
        1,
        out_shape=(2000, 2000),
        resampling=Resampling.nearest
    )

    print("Original dimensions:", src.width, "x", src.height)
    print("Preview dimensions:", preview.shape)

# Mask NoData pixels
masked_preview = np.ma.masked_equal(preview, 255)

# Class colours: non-vegetation, very low, low, moderate, healthy
colors = [
    "#303030",
    "#e53935",
    "#ff9800",
    "#ffeb3b",
    "#2e9d50"
]

cmap = ListedColormap(colors)
cmap.set_bad(color="white", alpha=0)

norm = BoundaryNorm(
    [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5],
    cmap.N
)

plt.figure(figsize=(14, 10))

image = plt.imshow(
    masked_preview,
    cmap=cmap,
    norm=norm,
    interpolation="nearest"
)

colorbar = plt.colorbar(
    image,
    ticks=[0, 1, 2, 3, 4],
    fraction=0.035,
    pad=0.03
)

colorbar.ax.set_yticklabels([
    "Non-Vegetation",
    "Very Low Health",
    "Low Health",
    "Moderate Health",
    "Healthy Vegetation"
])

plt.title("AgriVision X - Combined GIS Health Map", fontsize=16)
plt.axis("off")
plt.tight_layout()

plt.savefig(
    OUTPUT_PATH,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("Preview generated successfully!")
print("Output:", OUTPUT_PATH)
