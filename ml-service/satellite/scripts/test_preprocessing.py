
from preprocessing import load_red_nir

RED_PATH = "satellite/data/bands/B04_10m.jp2"
NIR_PATH = "satellite/data/bands/B08_10m.jp2"

red, nir, profile, valid_mask = load_red_nir(
    RED_PATH, NIR_PATH
)

print("Red shape:", red.shape)
print("NIR shape:", nir.shape)
print("Valid pixels:", int(valid_mask.sum()))
print("Invalid pixels:", int((~valid_mask).sum()))

print("CRS:", profile["crs"])
print("Preprocessing test completed successfully!")
