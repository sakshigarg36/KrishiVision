
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

INPUT_PATH = "satellite/data/outputs/combined_gis_health_map.tif"

OUTPUT_PATH = "satellite/data/outputs/gis_health_visualization.png"

print("=== GIS HEALTH MAP VISUALIZATION ===")

with rasterio.open(INPUT_PATH) as src:
    health_map = src.read(1)
    valid_mask = src.read_masks(1) > 0

print("Raster loaded successfully")
print("Shape:", health_map.shape)

# Define class colors
colors = [
    "#202020",  # Class 0: Non-vegetation
    "#D7191C",  # Class 1: Very low health
    "#FDAE61",  # Class 2: Moderate health
    "#FFFF33",  # Class 3: Good health
    "#1A9641",  # Class 4: High health
]

cmap = ListedColormap(colors)
cmap.set_bad((0, 0, 0, 0))

# Mask NoData pixels
masked_map = np.ma.masked_where(
    (~valid_mask) | (health_map == 255),
    health_map
)

norm = BoundaryNorm(
    [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5],
    cmap.N
)

# Create visualization
fig, ax = plt.subplots(figsize=(12, 10))

image = ax.imshow(
    masked_map,
    cmap=cmap,
    norm=norm,
    interpolation="nearest"
)

labels = [
    "Non-Vegetation",
    "Very Low Health",
    "Moderate Health",
    "Good Health",
    "High Health"
]

colorbar = fig.colorbar(
    image,
    ax=ax,
    ticks=[0, 1, 2, 3, 4],
    fraction=0.035,
    pad=0.03
)

colorbar.ax.set_yticklabels(labels)
colorbar.set_label("Vegetation Health Classification")

ax.set_title(
    "AgriVision X - Vegetation Health Map",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Raster Columns")
ax.set_ylabel("Raster Rows")
ax.set_aspect("equal")

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("Visualization saved:", OUTPUT_PATH)
print("=== VISUALIZATION COMPLETE ===")
