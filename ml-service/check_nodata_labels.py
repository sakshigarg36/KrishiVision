import numpy as np
import rasterio

PATH = "satellite/data/outputs/ndvi.tif"

with rasterio.open(PATH) as src:
    ndvi = src.read(1)
    valid_mask = src.dataset_mask() > 0
    nodata = src.nodata

    print("NoData value:", nodata)
    print("Total pixels:", ndvi.size)
    print("Valid pixels:", int(valid_mask.sum()))
    print("Invalid pixels:", int((~valid_mask).sum()))

    print("Invalid values:", np.unique(ndvi[~valid_mask], return_counts=True) if (~valid_mask).any() else "None")

    vegetation = (ndvi >= 0.2) & (ndvi <= 1.0)

    print("Vegetation pixels:", int(vegetation.sum()))
    print("Non-vegetation pixels:", int((~vegetation).sum()))

    print("Invalid pixels labelled as class 0:", int((~valid_mask & ~vegetation).sum()))
