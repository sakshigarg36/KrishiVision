
import rasterio
import numpy as np

files = {
    "NDVI": "satellite/data/outputs/ndvi.tif",
    "Health Zones": "satellite/data/outputs/health_zones.tif"
}

for name, path in files.items():

    print(f"\n===== {name} =====")

    with rasterio.open(path) as src:

        data = src.read(1, masked=True)
        valid = ~np.ma.getmaskarray(data)

        print("Shape:", data.shape)
        print("CRS:", src.crs)
        print("NoData:", src.nodata)
        print("Valid pixels:", int(valid.sum()))
        print("Invalid pixels:", int((~valid).sum()))

        if name == "NDVI" and valid.any():

            values = data.compressed()

            print("Minimum:", values.min())
            print("Maximum:", values.max())
            print("Mean:", values.mean())

            print(
                "Outside range:",
                int(((values < -1) | (values > 1)).sum())
            )

        elif name == "Health Zones":

            classes, counts = np.unique(
                data.compressed(),
                return_counts=True
            )

            print("\nZone Distribution:")

            for cls, count in zip(classes, counts):
                print(f"Zone {cls}: {count} pixels")

print("\nFinal Output Validation Completed!")
