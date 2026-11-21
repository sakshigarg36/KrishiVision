
import os
import sys
import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader, random_split

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.unet import UNet


IMAGE_DIR = "datasets/segmentation/images"
MASK_DIR = "datasets/segmentation/masks"

MODEL_DIR = "models"
MODEL_PATH = "models/unet_baseline.pth"

BATCH_SIZE = 4
EPOCHS = 3
LEARNING_RATE = 0.001
TRAIN_RATIO = 0.8


class SegmentationDataset(Dataset):

    def __init__(self, image_dir, mask_dir):

        self.image_dir = image_dir
        self.mask_dir = mask_dir

        self.files = sorted([
            f for f in os.listdir(image_dir)
            if f.endswith(".npy")
        ])

    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):

        filename = self.files[index]

        image = np.load(
            os.path.join(self.image_dir, filename)
        ).astype(np.float32)

        mask = np.load(
            os.path.join(self.mask_dir, filename)
        ).astype(np.float32)

        image = torch.from_numpy(image).unsqueeze(0)
        mask = torch.from_numpy(mask).unsqueeze(0)

        return image, mask


def evaluate(model, loader, criterion, device):

    model.eval()

    total_loss = 0.0
    tp = fp = fn = tn = 0

    with torch.no_grad():

        for images, masks in loader:

            images = images.to(device)
            masks = masks.to(device)

            outputs = model(images)

            loss = criterion(outputs, masks)
            total_loss += loss.item()

            predictions = torch.sigmoid(outputs) >= 0.5
            targets = masks >= 0.5

            tp += (predictions & targets).sum().item()
            fp += (predictions & ~targets).sum().item()
            fn += (~predictions & targets).sum().item()
            tn += (~predictions & ~targets).sum().item()

    dice = (2 * tp + 1e-7) / (2 * tp + fp + fn + 1e-7)
    vegetation_iou = (tp + 1e-7) / (tp + fp + fn + 1e-7)
    nonvegetation_iou = (tn + 1e-7) / (tn + fp + fn + 1e-7)

    return (
        total_loss / len(loader),
        dice,
        vegetation_iou,
        nonvegetation_iou
    )


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

    total_samples = len(dataset)
    train_size = int(total_samples * TRAIN_RATIO)
    val_size = total_samples - train_size

    train_dataset, val_dataset = random_split(
        dataset,
        [train_size, val_size],
        generator=torch.Generator().manual_seed(42)
    )

    print("Total samples:", total_samples)
    print("Training samples:", len(train_dataset))
    print("Validation samples:", len(val_dataset))

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
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

    best_val_loss = float("inf")

    os.makedirs(MODEL_DIR, exist_ok=True)

    for epoch in range(EPOCHS):

        model.train()
        total_train_loss = 0.0

        for images, masks in train_loader:

            images = images.to(device)
            masks = masks.to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, masks)

            loss.backward()
            optimizer.step()

            total_train_loss += loss.item()

        average_train_loss = (
            total_train_loss / len(train_loader)
        )

        val_loss, dice, veg_iou, nonveg_iou = evaluate(
            model,
            val_loader,
            criterion,
            device
        )

        print(f"\nEpoch [{epoch + 1}/{EPOCHS}]")
        print(f"Training Loss: {average_train_loss:.4f}")
        print(f"Validation Loss: {val_loss:.4f}")
        print(f"Vegetation Dice: {dice:.4f}")
        print(f"Vegetation IoU: {veg_iou:.4f}")
        print(f"Non-vegetation IoU: {nonveg_iou:.4f}")

        if val_loss < best_val_loss:

            best_val_loss = val_loss

            torch.save(
                model.state_dict(),
                MODEL_PATH
            )

            print("Best model saved:", MODEL_PATH)

    print("\n=== Training Complete ===")


if __name__ == "__main__":
    main()
