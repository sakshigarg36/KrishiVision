import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

HEALTH_PATH = "satellite/data/outputs/health_zones.tif"
PREVIEW_PATH = "satellite/data/outputs/health_zones_preview.png"

with rasterio.open(HEALTH_PATH) as src:
    zones = src.read(1)

plt.figure(figsize=(10, 8))

cmap = ListedColormap([
    "black",
    "red",
    "orange",
    "yellow",
    "green"
])

plt.imshow(
    zones,
    cmap=cmap,
    vmin=0,
    vmax=4
)

plt.colorbar(
    ticks=[0, 1, 2, 3, 4],
    label="Health Zone"
)

plt.title("Crop Health Zones")
plt.axis("off")

plt.savefig(
    PREVIEW_PATH,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print("=== Health Zone Preview Generated ===")
print("Preview:", PREVIEW_PATH)
