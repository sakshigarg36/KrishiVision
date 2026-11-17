
import json
import os
import random

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, models, transforms
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Configuration
DATA_DIR = "datasets/disease"
MODEL_DIR = "trained_models"
IMAGE_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2
SEED = 42

os.makedirs(MODEL_DIR, exist_ok=True)

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Separate training and validation transformations
train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

validation_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Load dataset twice so validation has no random augmentation
train_full = datasets.ImageFolder(
    DATA_DIR,
    transform=train_transform
)

validation_full = datasets.ImageFolder(
    DATA_DIR,
    transform=validation_transform
)

class_names = train_full.classes

assert class_names == validation_full.classes

total_size = len(train_full)
validation_size = int(total_size * VALIDATION_SPLIT)
training_size = total_size - validation_size

generator = torch.Generator().manual_seed(SEED)

train_subset, validation_subset = random_split(
    range(total_size),
    [training_size, validation_size],
    generator=generator
)

# Use same split indices for both datasets
from torch.utils.data import Subset

train_dataset = Subset(train_full, train_subset.indices)
validation_dataset = Subset(
    validation_full,
    validation_subset.indices
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

validation_loader = DataLoader(
    validation_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

print("Classes:", class_names)
print("Total images:", total_size)
print("Training images:", training_size)
print("Validation images:", validation_size)

# MobileNetV3 transfer learning
print("Loading MobileNetV3-Small...")

weights = models.MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=weights)

for parameter in model.parameters():
    parameter.requires_grad = False

model.classifier[3] = nn.Linear(
    model.classifier[3].in_features,
    len(class_names)
)

model = model.to(device)

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.classifier[3].parameters(),
    lr=LEARNING_RATE
)

best_accuracy = -1.0
model_path = os.path.join(MODEL_DIR, "disease_model.pth")

# Training loop
for epoch in range(EPOCHS):
    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        predictions = outputs.argmax(dim=1)
        total += labels.size(0)
        correct += (predictions == labels).sum().item()

    train_accuracy = 100 * correct / total

    # Validation
    model.eval()
    validation_correct = 0
    validation_total = 0

    with torch.no_grad():
        for images, labels in validation_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            predictions = outputs.argmax(dim=1)

            validation_total += labels.size(0)
            validation_correct += (
                predictions == labels
            ).sum().item()

    validation_accuracy = (
        100 * validation_correct / validation_total
    )

    average_loss = running_loss / len(train_loader)

    print(
        f"Epoch {epoch + 1}/{EPOCHS} | "
        f"Loss: {average_loss:.4f} | "
        f"Train Accuracy: {train_accuracy:.2f}% | "
        f"Validation Accuracy: {validation_accuracy:.2f}%"
    )

    if validation_accuracy > best_accuracy:
        best_accuracy = validation_accuracy
        torch.save(model.state_dict(), model_path)
        print("Best model saved.")

# Evaluate best saved model
print("\nEvaluating best model...")

model.load_state_dict(
    torch.load(model_path, map_location=device)
)
model.eval()

all_labels = []
all_predictions = []

with torch.no_grad():
    for images, labels in validation_loader:
        images = images.to(device)

        outputs = model(images)
        predictions = outputs.argmax(dim=1)

        all_labels.extend(labels.numpy().tolist())
        all_predictions.extend(predictions.cpu().numpy().tolist())

accuracy = accuracy_score(all_labels, all_predictions)

report = classification_report(
    all_labels,
    all_predictions,
    labels=list(range(len(class_names))),
    target_names=class_names,
    output_dict=True,
    zero_division=0
)

matrix = confusion_matrix(
    all_labels,
    all_predictions
)

# Save class names
with open(
    os.path.join(MODEL_DIR, "disease_classes.json"),
    "w"
) as file:
    json.dump(class_names, file, indent=4)

# Save evaluation report
evaluation = {
    "model": "MobileNetV3-Small",
    "total_images": total_size,
    "training_images": training_size,
    "validation_images": validation_size,
    "epochs": EPOCHS,
    "best_validation_accuracy": round(best_accuracy, 2),
    "final_validation_accuracy": round(accuracy * 100, 2),
    "classification_report": report,
    "confusion_matrix": matrix.tolist(),
    "classes": class_names
}

report_path = os.path.join(
    MODEL_DIR,
    "disease_evaluation.json"
)

with open(report_path, "w") as file:
    json.dump(evaluation, file, indent=4)

print("\nTraining and evaluation completed.")
print("Best validation accuracy:", round(best_accuracy, 2), "%")
print("Evaluation report saved:", report_path)
print("Model saved:", model_path)
