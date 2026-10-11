import rasterio
import matplotlib.pyplot as plt

NDVI_PATH = "satellite/data/outputs/ndvi.tif"
PREVIEW_PATH = "satellite/data/outputs/ndvi_preview.png"

with rasterio.open(NDVI_PATH) as src:
    ndvi = src.read(1)

plt.figure(figsize=(10, 8))

plt.imshow(
    ndvi,
    cmap="RdYlGn",
    vmin=-1,
    vmax=1
)

plt.colorbar(label="NDVI")
plt.title("Sentinel-2 NDVI Map")
plt.axis("off")

plt.savefig(
    PREVIEW_PATH,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print("=== NDVI Preview Generated ===")
print("Preview:", PREVIEW_PATH)
