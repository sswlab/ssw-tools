# ssw-ml

Machine learning for solar physics using preprocessed SSW data.

## Description

This skill provides comprehensive machine learning capabilities for solar physics research. It specializes in building, training, and evaluating deep learning models using solar EUV imagery and related observations. Designed to handle the unique challenges of solar physics ML applications.

## When to Use

Use this skill when Claude needs to:
1. Train deep learning models on solar EUV images
2. Build solar flare prediction models
3. Perform image-to-image translation between solar instruments
4. Detect and segment coronal holes or active regions
5. Create PyTorch/TensorFlow dataloaders for FITS files
6. Evaluate ML models on solar observation data

## Triggers

This skill is automatically invoked when users mention:
- 'solar ML'
- 'solar deep learning'
- 'flare prediction'
- 'coronal hole detection'
- 'instrument translation'
- 'solar image segmentation'
- 'FITS dataloader'
- 'solar neural network'
- '태양 ML'
- '태양 딥러닝'
- '플레어 예측'
- 'solar AI'

## Machine Learning Applications

### 1. Solar Flare Prediction
- **Task**: Predict M-class and X-class flares from magnetogram/EUV data
- **Models**: CNN, LSTM, Transformer-based architectures
- **Input**: Time series of solar active region observations
- **Output**: Flare probability within forecast window (6h, 12h, 24h)
- **Metrics**: TSS (True Skill Statistic), HSS (Heidke Skill Score)

### 2. Image-to-Image Translation
- **Task**: Translate between different instruments/wavelengths
- **Examples**:
  - SDO/AIA → STEREO/EUVI (cross-instrument)
  - 171Å → 193Å (cross-wavelength)
  - Low-res → High-res (super-resolution)
- **Models**: Pix2Pix, CycleGAN, Diffusion models
- **Applications**: Fill data gaps, synthetic observations

### 3. Coronal Hole Detection
- **Task**: Segment coronal holes from EUV imagery
- **Models**: U-Net, SegFormer, Mask R-CNN
- **Input**: 193Å or 211Å images (best for CH visibility)
- **Output**: Binary masks or polygonal boundaries
- **Validation**: Compare with manual expert annotations

### 4. Active Region Detection
- **Task**: Identify and track solar active regions
- **Models**: YOLO, Faster R-CNN, RetinaNet
- **Input**: Magnetogram and EUV multi-channel data
- **Output**: Bounding boxes with AR properties (area, flux, McIntosh class)
- **Tracking**: Associate ARs across time using motion models

### 5. Solar Wind Prediction
- **Task**: Predict solar wind parameters from coronal imagery
- **Models**: CNN + MLP, Physics-Informed Neural Networks
- **Input**: Full-disk EUV images, coronal hole maps
- **Output**: Solar wind speed, density at Earth's location
- **Lead time**: 1-4 days (solar rotation dependent)

## Usage Examples

### Create PyTorch DataLoader
```python
from ssw_tools.ml import SolarImageDataset
from torch.utils.data import DataLoader

# Dataset for multi-wavelength images
dataset = SolarImageDataset(
    data_dir='ml_ready/multi_channel/',
    wavelengths=[94, 131, 171, 193, 211, 304],
    transform=True,  # Apply augmentations
    normalize=True
)

dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4
)

# Training loop
for batch in dataloader:
    images, metadata = batch
    # images shape: [32, 6, 512, 512]
    # Train your model...
```

### Solar Flare Prediction Model
```python
from ssw_tools.ml import FlarePredictor
import torch

# Initialize model
model = FlarePredictor(
    backbone='resnet50',
    num_channels=6,
    sequence_length=12,  # 12 time steps
    forecast_window='24h'
)

# Train
model.fit(
    train_loader=train_loader,
    val_loader=val_loader,
    epochs=100,
    lr=1e-4,
    loss='focal_loss'  # Handle class imbalance
)

# Predict
proba = model.predict(test_images)
print(f"Flare probability: {proba:.3f}")
```

### Coronal Hole Segmentation
```python
from ssw_tools.ml import CoronalHoleSegmenter

# U-Net model for CH detection
segmenter = CoronalHoleSegmenter(
    architecture='unet',
    encoder='resnet34',
    input_channels=1  # Single wavelength (193Å)
)

segmenter.train(
    train_dataset=train_ds,
    val_dataset=val_ds,
    epochs=50,
    batch_size=16
)

# Segment coronal holes
mask = segmenter.predict('solar_image_193.npy')
# mask shape: [512, 512], binary values
```

### Instrument Translation (GAN)
```python
from ssw_tools.ml import InstrumentTranslator

# Translate AIA to EUVI
translator = InstrumentTranslator(
    source='SDO/AIA',
    target='STEREO/EUVI',
    wavelength=195,
    model_type='pix2pix'
)

translator.train(
    paired_data=paired_dataset,
    epochs=200,
    lr=2e-4,
    lambda_l1=100  # L1 loss weight
)

# Generate synthetic EUVI image
synthetic_euvi = translator.translate(aia_image)
```

### Transfer Learning from Pre-trained Models
```python
from ssw_tools.ml import SolarVisionTransformer

# Load pre-trained model on solar data
model = SolarVisionTransformer.from_pretrained(
    'solar-vit-base-patch16',
    num_classes=2  # Binary flare classification
)

# Fine-tune on your dataset
model.fine_tune(
    train_loader=train_loader,
    val_loader=val_loader,
    epochs=30,
    freeze_layers=8  # Freeze first 8 layers
)
```

## Model Zoo

Pre-trained models available:
- **solar-resnet50**: ResNet-50 pre-trained on SDO/AIA multi-wavelength
- **solar-vit-base**: Vision Transformer for solar image classification
- **ch-unet-193**: U-Net specialized for CH detection in 193Å
- **flare-predictor-lstm**: LSTM model for 24h flare forecasting
- **aia-to-euvi-gan**: Pix2Pix model for AIA→EUVI translation

## Data Augmentation

Specialized augmentations for solar data:
```python
from ssw_tools.ml.augmentation import SolarAugmentation

aug = SolarAugmentation(
    rotation=True,  # Random rotation (preserves solar physics)
    flip_lr=True,   # Horizontal flip
    flip_ud=True,   # Vertical flip
    brightness=(0.8, 1.2),  # Intensity variation
    noise=0.01,     # Gaussian noise
    solar_rotate=True  # Simulate solar rotation
)
```

## Evaluation Metrics

### Classification (Flare Prediction)
- True Skill Statistic (TSS)
- Heidke Skill Score (HSS)
- Precision, Recall, F1-Score
- ROC-AUC, PR-AUC
- Confusion Matrix

### Segmentation (CH/AR Detection)
- Dice Coefficient
- IoU (Intersection over Union)
- Pixel Accuracy
- Boundary F1-Score

### Regression (Solar Wind)
- RMSE (Root Mean Square Error)
- MAE (Mean Absolute Error)
- R² Score
- Skill Score vs. Persistence Model

### Image Translation
- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index)
- LPIPS (Learned Perceptual Image Patch Similarity)
- Physical consistency metrics

## Training Best Practices

### Handling Imbalanced Data
- Use focal loss or class weights for flare prediction
- Oversample rare events (X-class flares)
- Synthetic data generation with GANs

### Cross-Validation
- Temporal split (avoid data leakage across time)
- Active region-based split (test on unseen ARs)
- K-fold with temporal awareness

### Computational Resources
- GPU memory: 8-16 GB for most tasks
- Training time: Hours to days depending on dataset size
- Distributed training supported for large datasets

## Model Interpretability

```python
from ssw_tools.ml.explainability import GradCAM, SaliencyMap

# Generate attention maps
gradcam = GradCAM(model, target_layer='layer4')
attention_map = gradcam.explain(input_image)

# Visualize what the model focuses on
viz.plot_attention(input_image, attention_map)
```

## Dependencies

- **PyTorch** or **TensorFlow**: Deep learning frameworks
- **torchvision** / **tf.keras**: Model architectures
- **scikit-learn**: Traditional ML and metrics
- **pytorch-lightning**: Training boilerplate
- **timm**: Pre-trained vision models
- **segmentation-models-pytorch**: Segmentation architectures

## Advanced Features

### Physics-Informed Neural Networks (PINNs)
- Incorporate MHD equations as constraints
- Ensure physical consistency in predictions

### Self-Supervised Learning
- Pre-train on unlabeled solar data
- Contrastive learning for representation learning

### Multi-Modal Learning
- Combine EUV, magnetogram, and coronagraph data
- Fusion architectures for improved predictions

## Related Skills

- **ssw-prep**: Preprocess data before ML training
- **ssw-download**: Obtain training datasets
- **ssw-viz**: Visualize ML model predictions and attention maps
