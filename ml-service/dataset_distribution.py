import os
import numpy as np

MASK_DIR = "datasets/segmentation/masks"
IMAGE_DIR = "datasets/segmentation/images"

total_pixels = 0
class_counts = {}
unexpected_masks = []
image_min = float("inf")
image_max = float("-inf")
image_sum = 0.0
image_pixels = 0

for filename in sorted(os.listdir(MASK_DIR)):
    if not filename.endswith(".npy"):
        continue

    mask = np.load(os.path.join(MASK_DIR, filename))

    values, counts = np.unique(mask, return_counts=True)

    for value, count in zip(values, counts):
        class_counts[int(value)] = class_counts.get(int(value), 0) + int(count)

    total_pixels += mask.size

    if not set(values.tolist()).issubset({0, 1}):
        unexpected_masks.append(filename)

    image = np.load(os.path.join(IMAGE_DIR, filename))

    image_min = min(image_min, float(np.min(image)))
    image_max = max(image_max, float(np.max(image)))
    image_sum += float(np.sum(image))
    image_pixels += image.size

print("=== FULL DATASET DISTRIBUTION ===")
print("Total mask pixels:", total_pixels)

for label in sorted(class_counts):
    count = class_counts[label]
    percentage = count / total_pixels * 100
    print(f"Class {label}: {count} pixels ({percentage:.2f}%)")

print("\nUnexpected mask files:", len(unexpected_masks))
print("Global image min:", image_min)
print("Global image max:", image_max)
print("Global image mean:", image_sum / image_pixels)

print("\n=== DISTRIBUTION CHECK COMPLETE ===")
