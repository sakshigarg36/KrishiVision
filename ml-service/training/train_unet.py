import os
import sys
import numpy as np
import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from models.unet import UNet


IMAGE_DIR = "datasets/segmentation/images"
MASK_DIR = "datasets/segmentation/masks"

MODEL_DIR = "models"
MODEL_PATH = "models/unet_baseline.pth"

BATCH_SIZE = 4
EPOCHS = 3
LEARNING_RATE = 0.001


class SegmentationDataset(Dataset):
    def __init__(self, image_dir, mask_dir):
        self.image_dir = image_dir
        self.mask_dir = mask_dir

        self.files = sorted(
            [
                f for f in os.listdir(image_dir)
                if f.endswith(".npy")
            ]
        )

    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):
        filename = self.files[index]

        image_path = os.path.join(self.image_dir, filename)
        mask_path = os.path.join(self.mask_dir, filename)

        image = np.load(image_path).astype(np.float32)
        mask = np.load(mask_path).astype(np.float32)

        image = torch.from_numpy(image).unsqueeze(0)
        mask = torch.from_numpy(mask).unsqueeze(0)

        return image, mask


def main():

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("=== U-Net Training ===")
    print("Device:", device)

    dataset = SegmentationDataset(
        IMAGE_DIR,
        MASK_DIR
    )

    print("Total samples:", len(dataset))

    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0
    )

    model = UNet(
        in_channels=1,
        out_channels=1
    ).to(device)

    criterion = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE
    )

    model.train()

    for epoch in range(EPOCHS):

        total_loss = 0.0

        for images, masks in dataloader:

            images = images.to(device)
            masks = masks.to(device)

            optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(outputs, masks)

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        average_loss = total_loss / len(dataloader)

        print(
            f"Epoch [{epoch + 1}/{EPOCHS}] "
            f"Loss: {average_loss:.4f}"
        )

    os.makedirs(MODEL_DIR, exist_ok=True)

    torch.save(
        model.state_dict(),
        MODEL_PATH
    )

    print("=== Training Complete ===")
    print("Model saved:", MODEL_PATH)


if __name__ == "__main__":
    main()