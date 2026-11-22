
import json
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "trained_models"

MODEL_PATH = MODEL_DIR / "disease_model.pth"
CLASSES_PATH = MODEL_DIR / "disease_classes.json"

DEVICE = torch.device("cpu")

# Same preprocessing used during model training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


with open(CLASSES_PATH, "r") as file:
    CLASS_NAMES = json.load(file)


def load_model():
    model = models.mobilenet_v3_small(weights=None)

    model.classifier[3] = nn.Linear(
        model.classifier[3].in_features,
        len(CLASS_NAMES)
    )

    state_dict = torch.load(
        MODEL_PATH,
        map_location=DEVICE,
        weights_only=True
    )

    model.load_state_dict(state_dict)
    model.to(DEVICE)
    model.eval()

    return model


model = load_model()


def classify(image: Image.Image):
    image = image.convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)

        confidence, predicted_index = torch.max(
            probabilities, dim=1
        )

    predicted_class = CLASS_NAMES[predicted_index.item()]
    confidence_score = round(confidence.item() * 100, 2)

    if "___" in predicted_class:
        crop, disease = predicted_class.split("___", 1)
    else:
        crop = "Unknown"
        disease = predicted_class

    disease = disease.replace("_", " ")

    return {
        "crop": crop,
        "disease": disease,
        "predicted_class": predicted_class,
        "confidence": confidence_score,
        "is_healthy": "healthy" in disease.lower()
    }
