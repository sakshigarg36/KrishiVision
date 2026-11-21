
import rasterio
import numpy as np

path = "satellite/data/outputs/health_zones.tif"

with rasterio.open(path) as src:
    zones = src.read(1)

    print("Shape:", zones.shape)
    print("Data Type:", zones.dtype)

    classes, counts = np.unique(
        zones,
        return_counts=True
    )

    print("\nHealth Zone Distribution:")

    for cls, count in zip(classes, counts):
        percentage = (count / zones.size) * 100

        print(
            f"Zone {cls}: {count} pixels "
            f"({percentage:.2f}%)"
        )

    print("\nTotal Pixels:", zones.size)
    print("Unique Classes:", classes)
    print("NaN Pixels:", np.isnan(zones).sum())

print("\nHealth Zone Validation Completed")
