
import rasterio
import numpy as np

path = "satellite/data/outputs/ndvi.tif"

with rasterio.open(path) as src:
    ndvi = src.read(1)

    print("NDVI Shape:", ndvi.shape)
    print("Minimum:", np.nanmin(ndvi))
    print("Maximum:", np.nanmax(ndvi))
    print("Mean:", np.nanmean(ndvi))

    print("NaN pixels:", np.isnan(ndvi).sum())
    print("Infinite pixels:", np.isinf(ndvi).sum())

    valid = np.isfinite(ndvi)

    print("Valid pixels:", valid.sum())
    print("Invalid pixels:", (~valid).sum())

    print("Outside range:", ((ndvi[valid] < -1) | (ndvi[valid] > 1)).sum())

print("\nNDVI Quality Check Completed")
