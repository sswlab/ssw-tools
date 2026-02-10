# ssw-prep

SDO/AIA solar data preprocessing pipeline for machine learning applications.

## Description

This skill provides a comprehensive preprocessing pipeline specifically designed to transform raw SDO/AIA Level 1 FITS files into ML-ready Level 2 format. It implements standard solar physics calibration procedures (pointing correction, image registration, degradation correction) and normalization techniques optimized for deep learning applications.

## When to Use

Use this skill when Claude needs to:
1. Preprocess SDO/AIA Level 1 FITS data for machine learning
2. Calibrate AIA images (pointing, degradation, exposure correction)
3. Register and center solar disk images to standard resolution
4. Convert raw FITS to ML-ready FITS format
5. Batch process directories of AIA observations

## Triggers

This skill is automatically invoked when users mention:
- 'AIA preprocessing'
- 'SDO preprocessing'
- 'aia_prep_ml'
- 'ML-ready AIA data'
- 'calibrate AIA'
- 'solar image registration'
- '태양 데이터 전처리'
- 'AIA 보정'

## Core Function: `aia_prep_ml()`

```python
from ssw_tools.prep.sdo_aia import aia_prep_ml
from sunpy.map import Map
from astropy.table import QTable

# Load AIA map
aia_map = Map('aia_lev1_171a_2023_01_01t00_00_00.fits')

# Load calibration tables
pointing_table = QTable.read('pointing_table.ecsv', format='ascii.ecsv')
correction_table = QTable.read('correction_table.ecsv', format='ascii.ecsv')

# Preprocess
aia_map_prep = aia_prep_ml(
    aia_map,
    pointing_table=pointing_table,
    correction_table=correction_table,
    resolution=1024,
    padding_factor=0.1
)

# Save preprocessed map
aia_map_prep.save('aia_lev2_171a_2023_01_01t00_00_00.fits')
```

## Preprocessing Steps

The `aia_prep_ml()` function performs these steps in order:

### 1. Pointing Correction (Optional)
- Updates spacecraft pointing information using calibration table
- Corrects for spacecraft jitter and pointing errors
- Uses `aiapy.calibrate.update_pointing()`

### 2. Image Registration
Implemented in `register_ml()`:
- **NaN handling**: Replace NaN values with 0
- **Negative clipping**: Set negative values to 0
- **Data type**: Convert to float32 for efficiency
- **Solar rotation**: Rotate so solar north is up
- **Centering**: Align solar center with image center
- **Scaling**: Resize so `resolution/2 = (1 + padding_factor) × R_sun`
- **Cropping**: Extract centered `resolution × resolution` region
- **Padding**: Add padding if image is smaller than target resolution

### 3. Degradation Correction (Optional)
- Compensates for instrument sensitivity degradation over time
- Uses wavelength-specific correction factors
- Implemented in `degradation_correction()`
- Adds `deg_corr` metadata field

### 4. Exposure Normalization
- Normalizes by exposure time to get DN/s units
- Ensures consistent brightness across different exposures

## Parameters

```python
aia_prep_ml(
    aia_map,                    # Input SunPy Map object
    pointing_table=None,        # Pointing calibration table (optional)
    correction_table=None,      # Degradation correction table (optional)
    resolution=1024,            # Output image size (pixels)
    padding_factor=0.1          # Padding around solar disk (fraction of R_sun)
)
```

- `aia_map`: SunPy Map object loaded from Level 1 FITS file
- `pointing_table`: QTable from `pointing_table.ecsv` (optional but recommended)
- `correction_table`: QTable from `correction_table.ecsv` (optional but recommended)
- `resolution`: Output image dimensions (default: 1024×1024)
- `padding_factor`: Extra space around disk as fraction of solar radius (default: 0.1)

## Utility Functions

### `nan_to_num_clip()`
```python
nan_to_num_clip(data, nan=0, a_min=0, a_max=None)
```
Replaces NaN values and clips data to valid range.

### `register_ml()`
```python
register_ml(smap, resolution=2048, padding_factor=0.2)
```
Registers and normalizes solar disk to standard format.

### `degradation_correction()`
```python
degradation_correction(smap, correction_table=correction_table)
```
Applies instrument degradation correction.

## Batch Processing Script

The module includes a command-line script for batch processing:

```bash
python -m ssw_tools.prep.sdo_aia \
    --path_raw F:/data/raw/sdo/aia \
    --path_prep F:/data/prep/sdo/aia \
    --resolution 1024 \
    --padding_factor 0.1
```

**Script behavior:**
1. Searches for all `*.fits` files in `path_raw` recursively
2. Loads pointing and correction tables from `path_prep`
3. Processes each file with `aia_prep_ml()`
4. Saves to same relative path under `path_prep`
5. Skips files that already exist in output directory
6. Logs progress to `path_prep/aia_prep.log`
7. Continues processing even if individual files fail

## Command-Line Arguments

- `--path_raw`: Input directory containing raw Level 1 FITS files
- `--path_prep`: Output directory for preprocessed FITS files
- `--resolution`: Output image resolution (default: 1024)
- `--padding_factor`: Padding around solar disk (default: 0.1)

## Output Format

### Preprocessed FITS Files
Output files have:
- **Resolution**: Square images of specified size (e.g., 1024×1024)
- **Data type**: float32 (BITPIX=-32)
- **Units**: DN/s (exposure normalized)
- **Coordinate system**: Heliographic with solar center at image center
- **Level**: LVL_NUM=2.0 in header

### Updated Metadata
Key FITS header updates:
```
BITPIX = -32          # 32-bit floating point
LVL_NUM = 2.0         # Processing level
R_SUN = <pixels>      # Solar radius in pixels
CRPIX1 = resolution/2 + 0.5  # Center X
CRPIX2 = resolution/2 + 0.5  # Center Y
CRVAL1 = 0            # Solar center X
CRVAL2 = 0            # Solar center Y
PC1_1 = 1, PC1_2 = 0  # Rotation matrix
PC2_1 = 0, PC2_2 = 1
CROTA = 0             # No rotation
deg_corr = <value>    # Degradation correction factor
```

## Required Calibration Files

Place in `path_prep` before running batch processing:

1. **pointing_table.ecsv**: Pointing correction table
   - Generated using `aiapy.calibrate.fetch_spikes` or similar

2. **correction_table.ecsv**: Degradation correction table
   - Generated using `aiapy.calibrate.degradation` lookup tables

## Dependencies

- **sunpy**: Solar physics library (Map class, FITS I/O)
- **aiapy**: AIA-specific calibration routines
  - `aiapy.calibrate.update_pointing`
  - `aiapy.calibrate.degradation`
- **astropy**: FITS handling, coordinate transforms, units
- **numpy**: Array operations
- **loguru**: Logging (batch processing)
- **tqdm**: Progress bars (batch processing)
- **pathlib**: Path manipulation

## Example Workflow

### Single File Processing
```python
from sunpy.map import Map
from astropy.table import QTable
from ssw_tools.prep.sdo_aia import aia_prep_ml

# Load calibration tables (download once, reuse)
pointing_table = QTable.read('pointing_table.ecsv', format='ascii.ecsv')
correction_table = QTable.read('correction_table.ecsv', format='ascii.ecsv')

# Process single observation
aia_map = Map('aia_lev1_171a_2023_01_01t00_00_00.fits')
aia_prep = aia_prep_ml(
    aia_map,
    pointing_table=pointing_table,
    correction_table=correction_table,
    resolution=512,
    padding_factor=0.15
)

# Access processed data
print(aia_prep.data.shape)  # (512, 512)
print(aia_prep.data.dtype)  # float32
aia_prep.save('output.fits')
```

### Batch Processing
```bash
# Prepare directory structure
mkdir -p /data/prep/sdo/aia

# Download calibration tables (one-time setup)
# (Use aiapy utilities or pre-downloaded tables)

# Run batch preprocessing
python -m ssw_tools.prep.sdo_aia \
    --path_raw /data/raw/sdo/aia \
    --path_prep /data/prep/sdo/aia \
    --resolution 1024 \
    --padding_factor 0.1
```

## Performance Considerations

- **Processing time**: ~2-5 seconds per image (CPU)
- **Memory usage**: ~500 MB per 4K×4K input image
- **Output size**: ~4 MB per 1024×1024 float32 image
- **Parallelization**: Script processes files sequentially (can be parallelized externally)

## References

Based on methodology from:
- **InstrumentToInstrument**: https://github.com/RobertJaro/InstrumentToInstrument/
- Standard SDO/AIA Level 1.5 processing procedures
- AIA Instrument Guide and calibration papers

## Notes

- Pointing and degradation corrections are optional but strongly recommended for ML applications
- The `padding_factor` controls how much context around the solar disk is included
- Lower resolution (e.g., 512) is faster and sufficient for many ML tasks
- The script preserves directory structure from `path_raw` to `path_prep`
- Failed files are logged but don't stop batch processing

## Related Skills

- **ssw-download**: Download raw SDO/AIA FITS files (note: current download module supports STEREO/SolO only)
- **ssw-viz**: (Planned) Visualize before/after preprocessing comparison
- **ssw-ml**: (Planned) Use preprocessed data for ML model training
