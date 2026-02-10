# SSW Plugin for Claude Code

SolarSoft Workshop (SSW) plugin for Claude Code - A comprehensive toolkit for solar physics data analysis, preprocessing, machine learning, and visualization.

## Overview

This plugin provides four specialized skills for working with solar observation data:

1. **ssw-download**: Download solar observation data from SDO, STEREO, and Solar Orbiter
2. **ssw-prep**: Preprocess AIA Level 1 FITS data for machine learning applications
3. **ssw-ml**: Train and evaluate deep learning models on solar physics data
4. **ssw-viz**: Visualize solar EUV imagery, ML results, and analysis

## Installation

### Prerequisites

- Python 3.8 or higher
- Claude Code CLI

### Install Dependencies

```bash
pip install sunpy astropy numpy scipy matplotlib torch torchvision \
    scikit-image scikit-learn aiapy drms opencv-python tqdm
```

Or use the provided requirements file:

```bash
pip install -r requirements.txt
```

### Install Plugin

Copy the `.claude-plugin` directory to your Claude Code plugins folder:

```bash
# Linux/Mac
cp -r .claude-plugin ~/.claude/plugins/ssw-plugin

# Windows
xcopy .claude-plugin %USERPROFILE%\.claude\plugins\ssw-plugin /E /I
```

## Skills

### ssw-download

Download solar observation data from multiple missions.

**Example usage:**
```
Download SDO/AIA 171Å data from 2023-01-01
```

**Supported missions:**
- SDO/AIA (multiple wavelengths)
- STEREO/EUVI
- Solar Orbiter/EUI

### ssw-prep

Preprocess raw FITS files for machine learning.

**Example usage:**
```
Preprocess AIA 171Å images for ML training
```

**Features:**
- Calibration (pointing, degradation, exposure)
- Image registration
- Normalization
- Batch processing

### ssw-ml

Machine learning for solar physics.

**Example usage:**
```
Train a coronal hole detection model
Create a solar flare predictor
```

**Applications:**
- Solar flare prediction
- Coronal hole segmentation
- Active region detection
- Instrument-to-instrument translation
- Solar wind prediction

### ssw-viz

Visualize solar data and ML results.

**Example usage:**
```
Visualize AIA multi-wavelength observations
Create solar animation from time series
```

**Visualization types:**
- Single/multi-wavelength displays
- Time-lapse animations
- Before/after preprocessing comparisons
- ML prediction overlays
- Quantitative analysis plots

## Usage Examples

### Complete Workflow

```python
# 1. Download data
Download SDO/AIA 171Å and 193Å data from 2023-01-01 to 2023-01-02 with 1-hour cadence

# 2. Preprocess for ML
Preprocess the downloaded AIA images for machine learning, normalize and save as numpy arrays

# 3. Train ML model
Train a coronal hole detection model using the preprocessed 193Å images

# 4. Visualize results
Visualize the coronal hole detection results overlaid on the original images
```

### Quick Tasks

```python
# Download single observation
Download latest SDO/AIA 304Å image

# Show multi-wavelength comparison
Display AIA 94, 171, 193, 211, 304, and 335Å images side by side

# Create animation
Create a time-lapse animation of AIA 171Å for 2023-06-15
```

## Data Sources

- **JSOC (Joint Science Operations Center)**: SDO/AIA data
- **VSO (Virtual Solar Observatory)**: STEREO and Solar Orbiter data
- **Pre-trained Models**: Available through skill model zoo

## Documentation

Detailed documentation for each skill is available in the `skills/` directory:

- [ssw-download/SKILL.md](skills/ssw-download/SKILL.md)
- [ssw-prep/SKILL.md](skills/ssw-prep/SKILL.md)
- [ssw-ml/SKILL.md](skills/ssw-ml/SKILL.md)
- [ssw-viz/SKILL.md](skills/ssw-viz/SKILL.md)

## Requirements

### Python Packages

- **sunpy** (>=5.0.0): Solar physics data analysis
- **astropy** (>=5.0): Astronomy data handling
- **numpy** (>=1.21.0): Array operations
- **scipy** (>=1.7.0): Scientific computing
- **matplotlib** (>=3.4.0): Visualization
- **torch** (>=2.0.0): Deep learning framework
- **torchvision** (>=0.15.0): Computer vision models
- **scikit-image** (>=0.19.0): Image processing
- **scikit-learn** (>=1.0.0): Machine learning utilities
- **aiapy** (>=0.7.0): AIA-specific preprocessing
- **drms** (>=0.6.0): JSOC data access
- **opencv-python** (>=4.5.0): Video processing
- **tqdm** (>=4.62.0): Progress bars

### System Requirements

- **Disk space**: 10+ GB for data storage
- **RAM**: 16+ GB recommended for ML tasks
- **GPU**: CUDA-capable GPU recommended for ML training

## Contributing

Contributions are welcome! Please submit issues and pull requests on GitHub.

## License

MIT License - see LICENSE file for details

## Citation

If you use this plugin in your research, please cite:

```bibtex
@software{ssw_plugin,
  title = {SSW Plugin for Claude Code},
  author = {SSW Team},
  year = {2024},
  url = {https://github.com/yourusername/ssw-plugin}
}
```

## Support

For questions and support:
- GitHub Issues: https://github.com/yourusername/ssw-plugin/issues
- Email: support@example.com

## Acknowledgments

This plugin builds upon:
- SunPy Project
- AIA Team at NASA/SDO
- STEREO and Solar Orbiter missions
- SolarSoft (SSW) IDL library

---

**Note**: This plugin is designed for research and educational purposes. Always verify results independently for scientific publications.
