
import rasterio

files = [
    "satellite/data/bands/B04_10m.jp2",
    "satellite/data/bands/B08_10m.jp2"
]

for f in files:
    with rasterio.open(f) as s:
        print("\nFILE:", f)
        print("NoData:", s.nodata)
        print("CRS:", s.crs)
        print("Transform:", s.transform)
        print("Bounds:", s.bounds)
        print("Valid pixels:", int(s.dataset_mask().astype(bool).sum()))
        print("Total pixels:", s.width * s.height)
