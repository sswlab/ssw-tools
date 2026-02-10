# ssw-ml

Machine learning for solar physics using preprocessed SSW data (PLANNED).

## Description

This skill is planned to provide comprehensive machine learning capabilities for solar physics research. It will specialize in building, training, and evaluating deep learning models using solar EUV imagery and related observations.

## Status

⚠️ **NOT YET IMPLEMENTED** ⚠️

This skill is currently in the planning phase. The functionality described below represents the intended capabilities, not current implementation.

## When to Use

This skill will be used when Claude needs to:
1. Train deep learning models on solar EUV images
2. Build solar flare prediction models
3. Perform image-to-image translation between solar instruments
4. Detect and segment coronal holes or active regions
5. Create PyTorch/TensorFlow dataloaders for FITS files
6. Evaluate ML models on solar observation data

## Triggers

This skill will be automatically invoked when users mention:
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

## Planned Features

### 1. Solar Image Datasets
- PyTorch/TensorFlow dataset classes for FITS files
- Automatic loading of preprocessed AIA data
- Multi-wavelength channel handling
- Time series dataset support

### 2. Model Architectures
- CNN-based models for classification and regression
- U-Net and variants for segmentation
- GAN architectures for image translation
- Transformer-based models for sequence prediction

### 3. Solar-Specific Tasks
- **Flare Prediction**: M/X-class flare forecasting
- **Coronal Hole Detection**: Segmentation of low-density regions
- **Active Region Detection**: Object detection and tracking
- **Instrument Translation**: Cross-instrument synthesis
- **Solar Wind Prediction**: Parameter forecasting from imagery

### 4. Training Utilities
- Solar-aware data augmentation
- Imbalanced data handling
- Physics-informed loss functions
- Multi-task learning support

### 5. Evaluation Metrics
- Solar physics specific metrics (TSS, HSS for flares)
- Standard ML metrics (accuracy, F1, IoU, etc.)
- Visualization of predictions

## Planned Dependencies

- PyTorch or TensorFlow
- torchvision / tf.keras
- scikit-learn
- pytorch-lightning (optional)
- timm (pre-trained models)
- segmentation-models-pytorch

## Implementation Roadmap

1. **Phase 1**: Dataset classes and dataloaders
2. **Phase 2**: Basic CNN models for classification
3. **Phase 3**: Segmentation models (U-Net)
4. **Phase 4**: Advanced architectures (GANs, Transformers)
5. **Phase 5**: Pre-trained model zoo

## Contributing

If you're interested in implementing this module, please:
1. Review the existing preprocessing pipeline in `ssw_tools.prep`
2. Ensure compatibility with preprocessed AIA FITS files
3. Follow solar physics best practices for ML applications
4. Include comprehensive documentation and examples

## Temporary Alternative

Until this module is implemented, users can:
1. Use the `ssw-prep` skill to preprocess data
2. Load preprocessed FITS files with SunPy
3. Create custom PyTorch/TensorFlow datasets
4. Use standard ML libraries directly

Example:
```python
from sunpy.map import Map
import torch
from torch.utils.data import Dataset

class AIADataset(Dataset):
    def __init__(self, file_list):
        self.files = file_list

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        aia_map = Map(self.files[idx])
        data = torch.from_numpy(aia_map.data)
        return data, aia_map.meta
```

## Related Skills

- **ssw-prep**: Preprocess data before ML training
- **ssw-download**: Obtain training datasets
- **ssw-viz**: (Planned) Visualize ML model predictions
