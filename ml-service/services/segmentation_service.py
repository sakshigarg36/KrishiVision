import os
import numpy as np
import torch

from models.unet import UNet

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "unet_baseline.pth")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_model = None


def get_model():
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"U-Net model weights not found: {MODEL_PATH}"
            )

        _model = UNet(in_channels=1, out_channels=1).to(DEVICE)

        _model.load_state_dict(
            torch.load(MODEL_PATH, map_location=DEVICE)
        )

        _model.eval()

    return _model


def segment(image):
    image = np.asarray(image, dtype=np.float32)

    if image.ndim != 2:
        raise ValueError("Input image must be a 2D NDVI array.")

    if image.size == 0:
        raise ValueError("Input image cannot be empty.")
    if not np.isfinite(image).all():
        raise ValueError("Input image must contain only finite values.")
    model = get_model()

    input_tensor = (
        torch.from_numpy(image)
        .unsqueeze(0)
        .unsqueeze(0)
        .to(DEVICE)
    )

    with torch.no_grad():
        output = model(input_tensor)
        probability = torch.sigmoid(output)
        predicted_mask = (probability > 0.5).to(torch.uint8)

    mask = predicted_mask.squeeze().cpu().numpy()

    return {
        "mask": mask,
        "height": int(mask.shape[0]),
        "width": int(mask.shape[1]),
        "classes": [int(value) for value in np.unique(mask)],
        "model": "unet_baseline",
    }