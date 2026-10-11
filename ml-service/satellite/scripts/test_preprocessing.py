from preprocessing import load_red_nir

RED_PATH = "satellite/data/bands/B04_10m.jp2"
NIR_PATH = "satellite/data/bands/B08_10m.jp2"


red, nir, profile = load_red_nir(RED_PATH, NIR_PATH)

print("=== Sentinel-2 Preprocessing Test ===")
print("Red shape:", red.shape)
print("NIR shape:", nir.shape)
print("Red dtype:", red.dtype)
print("NIR dtype:", nir.dtype)
print("Red min:", red.min())
print("Red max:", red.max())
print("NIR min:", nir.min())
print("NIR max:", nir.max())
print("CRS:", profile["crs"])
print("Resolution:", profile["transform"].a)
print("B04/B08 extraction and preprocessing successful")