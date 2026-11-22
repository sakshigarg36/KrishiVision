import numpy as np
import glob
import os

from services.segmentation_service import segment

files = sorted(
    glob.glob("datasets/segmentation/images/*.npy")
)

indices = np.linspace(
    0, len(files) - 1, 20, dtype=int
)

passed = 0
failed = []

print("DISTRIBUTED U-NET TEST")

for i in indices:
    file_path = files[i]

    try:
        image = np.load(file_path)
        result = segment(image)
        mask = result["mask"]

        valid = (
            mask.shape == (256, 256)
            and np.isfinite(mask).all()
        )

        if valid:
            passed += 1
            status = "PASS"
        else:
            status = "INVALID"

        print(
            os.path.basename(file_path),
            status,
            "Classes:",
            np.unique(mask).tolist()
        )

    except Exception as error:
        failed.append(
            (os.path.basename(file_path), str(error))
        )
        print(
            os.path.basename(file_path),
            "FAIL:",
            error
        )

print("\nSUMMARY")
print("Tested:", len(indices))
print("Passed:", passed)
print("Failed:", len(failed))
print("Failure details:", failed)
