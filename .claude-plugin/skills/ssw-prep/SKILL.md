# ssw-prep

SDO/AIA solar data ML preprocessing pipeline for machine learning applications.

## Description

This skill provides a comprehensive preprocessing pipeline specifically designed to transform raw SDO/AIA Level 1 FITS files into ML-ready formats. It implements standard solar physics calibration procedures and normalization techniques optimized for deep learning applications.

## When to Use

Use this skill when Claude needs to:
1. Preprocess AIA Level 1 FITS data for machine learning
2. Calibrate solar images (pointing, degradation, exposure correction)
3. Register and normalize solar disk images
4. Batch convert raw FITS to ML-ready format
5. Standardize solar observation data for neural network training

## Triggers

This skill is automatically invoked when users mention:
- 'AIA preprocessing'
- 'solar data prep'
- 'FITS preprocessing'
- 'aia_prep_ml'
- 'ML-ready solar data'
- 'calibrate AIA'
- 'solar image registration'
- '태양 데이터 전처리'
- 'AIA 보정'
- 'ML 전처리'

## Preprocessing Steps

### 1. Level 1 to Level 1.5 Calibration
- **Pointing correction**: Align images to solar disk center
- **Degradation correction**: Compensate for instrument sensitivity changes over time
- **Exposure normalization**: Standardize exposure times across observations
- **Despiking**: Remove cosmic ray artifacts and bad pixels

### 2. Image Registration
- **Solar disk detection**: Locate and center the solar disk
- **Rotation compensation**: Account for solar rotation
- **Limb darkening**: Optional correction for intensity falloff at solar limb
- **Coordinate system**: Transform to helioprojective coordinates

### 3. Normalization for ML
- **Intensity scaling**: Map to [0, 1] or [-1, 1] range
- **Logarithmic transformation**: Handle wide dynamic range (optional)
- **Standardization**: Zero mean, unit variance per wavelength channel
- **Clipping**: Remove extreme outliers

### 4. Output Formatting
- **Data format**: NumPy arrays (.npy) or PyTorch tensors (.pt)
- **Metadata preservation**: Store observation time, wavelength, coordinates
- **Efficient storage**: Compressed formats for large datasets

## Usage Examples

### Basic preprocessing
```python
from ssw_tools.prep import aia_prep_ml

# Preprocess single FITS file
aia_prep_ml(
    input_file='aia_20230101_000000_171.fits',
    output_file='processed/aia_171_000.npy',
    normalize=True,
    clip_percentile=99.5
)
```

### Batch preprocessing
```python
import glob
from ssw_tools.prep import batch_prep_ml

# Process all FITS files in directory
fits_files = glob.glob('raw_data/*.fits')
batch_prep_ml(
    input_files=fits_files,
    output_dir='ml_ready/',
    normalize=True,
    log_scale=True,
    n_jobs=4  # Parallel processing
)
```

### Multi-wavelength preprocessing
```python
from ssw_tools.prep import prep_multi_wavelength

# Create aligned multi-channel images
wavelengths = [94, 131, 171, 193, 211, 304]
prep_multi_wavelength(
    base_dir='raw_data/',
    wavelengths=wavelengths,
    output_dir='ml_ready/multi_channel/',
    timestamp='2023-01-01T12:00:00',
    output_format='numpy'  # or 'torch'
)
```

### Custom preprocessing pipeline
```python
from ssw_tools.prep import PreprocessingPipeline

pipeline = PreprocessingPipeline(
    steps=[
        'calibrate',
        'register',
        'normalize',
        'resize'  # Optional: resize to 512x512
    ],
    normalize_method='minmax',  # or 'standardize'
    target_size=(512, 512),
    clip_percentile=99.0
)

processed = pipeline.process('input.fits')
pipeline.save(processed, 'output.npy')
```

## Configuration Options

### Normalization Methods
- **minmax**: Scale to [0, 1] range
- **standardize**: Zero mean, unit variance
- **log_minmax**: Logarithmic then min-max
- **robust**: Use median and IQR for outlier resistance

### Output Formats
- **numpy** (.npy): NumPy array format
- **torch** (.pt): PyTorch tensor format
- **zarr**: Compressed chunked array format for large datasets
- **hdf5**: HDF5 format with metadata

### Quality Control
- **Bad pixel detection**: Identify and interpolate bad pixels
- **Saturation handling**: Flag and handle saturated regions
- **Exposure filtering**: Remove under/over-exposed images
- **Coverage check**: Ensure full disk coverage

## Output Structure

Preprocessed files include:
```
output_dir/
├── images/
│   ├── 20230101_000000_171.npy
│   ├── 20230101_000500_171.npy
│   └── ...
├── metadata/
│   ├── 20230101_000000_171.json
│   └── ...
└── preprocessing_log.txt
```

Metadata JSON contains:
```json
{
    "original_file": "aia_20230101_000000_171.fits",
    "wavelength": 171,
    "observation_time": "2023-01-01T00:00:00",
    "normalization": "minmax",
    "clip_percentile": 99.5,
    "shape": [512, 512],
    "preprocessing_timestamp": "2023-01-15T10:30:00"
}
```

## Dependencies

- `sunpy`: Solar physics library with AIA prep routines
- `aiapy`: Specialized AIA preprocessing functions
- `astropy`: FITS file handling and coordinates
- `scikit-image`: Image processing utilities
- `numpy`: Array operations
- `torch` or `tensorflow`: Optional for direct tensor output

## Performance Considerations

- **Parallel processing**: Use `n_jobs` parameter for batch processing
- **Memory usage**: ~500 MB per 4K×4K image
- **Processing time**: ~2-5 seconds per image (CPU), ~0.5s (GPU)
- **Storage**: Compressed numpy arrays are ~10-20 MB per image

## Quality Assurance

The pipeline includes automatic checks for:
- Image quality metrics (contrast, sharpness)
- Calibration success verification
- Alignment accuracy assessment
- Outlier detection in intensity distributions

## Related Skills

- **ssw-download**: Download raw FITS files for preprocessing
- **ssw-viz**: Visualize before/after preprocessing comparison
- **ssw-ml**: Use preprocessed data for ML model training
