import os
import numpy as np

IMAGE_DIR = "datasets/segmentation/images"
MASK_DIR = "datasets/segmentation/masks"

image_files = sorted(f for f in os.listdir(IMAGE_DIR) if f.endswith(".npy"))
mask_files = sorted(f for f in os.listdir(MASK_DIR) if f.endswith(".npy"))

print("=== DATASET QUALITY CHECK ===")
print("Images:", len(image_files))
print("Masks:", len(mask_files))

missing_masks = sorted(set(image_files) - set(mask_files))
extra_masks = sorted(set(mask_files) - set(image_files))

print("Missing masks:", len(missing_masks))
print("Extra masks:", len(extra_masks))

shape_errors = []
invalid_images = []
invalid_masks = []

for filename in image_files:
    image = np.load(os.path.join(IMAGE_DIR, filename))
    mask_path = os.path.join(MASK_DIR, filename)

    if not os.path.exists(mask_path):
        continue

    mask = np.load(mask_path)

    if image.shape != mask.shape:
        shape_errors.append(filename)

    if not np.isfinite(image).all():
        invalid_images.append(filename)

    if not np.isfinite(mask).all():
        invalid_masks.append(filename)

print("Shape mismatches:", len(shape_errors))
print("Images with NaN/Inf:", len(invalid_images))
print("Masks with NaN/Inf:", len(invalid_masks))

sample_image = np.load(os.path.join(IMAGE_DIR, image_files[0]))
sample_mask = np.load(os.path.join(MASK_DIR, image_files[0]))

print("\n=== FIRST SAMPLE DETAILS ===")
print("Filename:", image_files[0])
print("Image shape:", sample_image.shape)
print("Image dtype:", sample_image.dtype)
print("Image min:", float(np.min(sample_image)))
print("Image max:", float(np.max(sample_image)))
print("Image mean:", float(np.mean(sample_image)))

print("\nMask shape:", sample_mask.shape)
print("Mask dtype:", sample_mask.dtype)
print("Mask unique values:", np.unique(sample_mask, return_counts=True))

print("\n=== CHECK COMPLETE ===")
