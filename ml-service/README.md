
# ML Service - KrishiVision

This module contains the machine learning training pipelines and trained model artifacts developed for KrishiVision.

## 1. Disease Classification - CNN

- Architecture: MobileNetV3-Small (pretrained)
- Framework: PyTorch and Torchvision
- Dataset: 5,500 images across 4 classes
- Training images: 4,400
- Validation images: 1,100
- Epochs: 5
- Best validation accuracy: 96.45%

### Classes
- Potato___Early_blight
- Tomato___Early_blight
- Tomato___Late_blight
- Tomato___healthy

Evaluation details: `trained_models/disease_evaluation.json`

## 2. Crop Yield Prediction - XGBoost

- Dataset: 198,369 rows
- Train-validation split: 80:20

| Metric | Value |
|---|---:|
| MAE | 313.1966 |
| RMSE | 540.3052 |
| R2 Score | 0.8714 |

Metrics are from the validation split.

## 3. Installation

```bash
pip install -r requirements-training.txt
```

## 4. Training

```bash
python train_disease.py
python train_yield.py
```

## 5. Dataset Locations

- Disease: `datasets/disease/`
- Yield: `datasets/yield/source/crop_yield_dataset.csv`

Datasets are not included in this contribution.

## 6. Model Artifacts

- Disease: `trained_models/disease_model.pth`
- Yield: `trained_models/yield_model.pkl`
- Evaluation reports and feature metadata are stored in `trained_models/`.
