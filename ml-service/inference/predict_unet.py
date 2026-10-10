import os
import sys
import numpy as np
import torch
import matplotlib.pyplot as plt

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from models.unet import UNet


IMAGE_PATH = "datasets/segmentation/images/tile_0000.npy"
MODEL_PATH = "models/unet_baseline.pth"
OUTPUT_PATH = "inference/predicted_mask.png"


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=== U-Net Inference ===")
print("Device:", device)


model = UNet(
    in_channels=1,
    out_channels=1
).to(device)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model.eval()


image = np.load(IMAGE_PATH).astype(np.float32)

input_tensor = torch.from_numpy(
    image
).unsqueeze(0).unsqueeze(0).to(device)


with torch.no_grad():
    output = model(input_tensor)
    probability = torch.sigmoid(output)
    predicted_mask = (
        probability > 0.5
    ).float()


predicted_mask = (
    predicted_mask
    .squeeze()
    .cpu()
    .numpy()
    .astype(np.uint8)
)


os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)


plt.figure(figsize=(8, 8))

plt.imshow(
    predicted_mask,
    cmap="gray",
    vmin=0,
    vmax=1
)

plt.title("U-Net Predicted Segmentation Mask")
plt.axis("off")

plt.savefig(
    OUTPUT_PATH,
    dpi=150,
    bbox_inches="tight"
)

plt.close()


print("Input shape:", image.shape)
print("Prediction shape:", predicted_mask.shape)
print("Prediction values:", np.unique(predicted_mask))
print("Predicted mask:", OUTPUT_PATH)
print("=== Inference Complete ===")