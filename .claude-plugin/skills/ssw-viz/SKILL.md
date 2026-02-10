# ssw-viz

Solar observation data visualization for EUV imagery and analysis (PLANNED).

## Description

This skill is planned to provide comprehensive visualization capabilities for solar observation data, preprocessing results, and machine learning model outputs. It will offer specialized plotting functions designed for solar physics data with proper color maps, coordinate systems, and physical units.

## Status

⚠️ **NOT YET IMPLEMENTED** ⚠️

This skill is currently in the planning phase. The functionality described below represents the intended capabilities, not current implementation.

## When to Use

This skill will be used when Claude needs to:
1. Display solar EUV images from FITS files
2. Create multi-wavelength comparison panels
3. Make before/after preprocessing comparisons
4. Visualize ML model predictions on solar data
5. Create solar time-lapse animations
6. Plot intensity distributions of solar images

## Triggers

This skill will be automatically invoked when users mention:
- 'solar visualization'
- 'solar image display'
- 'FITS visualization'
- 'EUV image plot'
- 'multi-wavelength comparison'
- 'solar animation'
- '태양 이미지 시각화'
- '태양 시각화'

## Planned Features

### 1. Basic Image Display
- Single FITS file visualization
- Automatic wavelength-specific colormaps
- Coordinate grid overlay
- Solar limb marking
- Colorbar with proper units

### 2. Multi-Wavelength Panels
- Side-by-side comparisons
- Grid layouts for multiple wavelengths
- Synchronized colorbars
- Time-matched observations

### 3. Preprocessing Comparison
- Before/after preprocessing views
- Difference images
- Split-view comparisons
- Quality metrics overlay

### 4. Time Series and Animations
- Image sequences as video/GIF
- Running difference movies
- Feature tracking visualization
- Customizable frame rate and resolution

### 5. Analysis Plots
- Intensity histograms
- Radial profiles from disk center
- Light curves at selected regions
- Power spectra

### 6. ML Visualization
- Segmentation mask overlays
- Detection bounding boxes
- Attention/activation maps
- Prediction confidence heatmaps

## Planned Standard Color Maps

### AIA Wavelengths
- **171Å**: Gold/yellow (quiet corona)
- **193Å**: Bronze (hot active regions)
- **211Å**: Pink (active regions)
- **304Å**: Red (chromosphere)

### STEREO/EUVI Wavelengths
- **171Å**: Similar to AIA 171
- **195Å**: Similar to AIA 193
- **284Å**: Green tones
- **304Å**: Red (chromosphere)

### Solar Orbiter/EUI
- **174Å**: Similar to AIA 171
- **304Å**: Red (chromosphere)

## Planned API Examples

### Single Image Display
```python
from ssw_tools.viz import plot_solar_image

plot_solar_image(
    'aia_lev2_171a_2023_01_01t00_00_00.fits',
    cmap='sdoaia171',
    title='SDO/AIA 171Å',
    colorbar=True,
    grid=True,
    save='aia_171.png'
)
```

### Multi-Wavelength Comparison
```python
from ssw_tools.viz import plot_multi_wavelength

files = [
    'aia_171.fits',
    'aia_193.fits',
    'aia_211.fits',
    'aia_304.fits'
]

plot_multi_wavelength(
    files,
    wavelengths=[171, 193, 211, 304],
    layout=(2, 2),
    figsize=(12, 12),
    save='multi_wavelength.png'
)
```

### Preprocessing Comparison
```python
from ssw_tools.viz import plot_preprocessing_comparison

plot_preprocessing_comparison(
    before='aia_lev1_171.fits',
    after='aia_lev2_171.fits',
    titles=['Raw Level 1', 'Preprocessed Level 2'],
    save='preprocessing_comparison.png'
)
```

### Animation
```python
from ssw_tools.viz import create_animation

create_animation(
    image_files=sorted(glob.glob('timeseries/*.fits')),
    output='solar_evolution.mp4',
    fps=10,
    cmap='sdoaia171'
)
```

## Planned Dependencies

- matplotlib: Core plotting
- sunpy: Solar-specific visualization utilities
- astropy: FITS handling and WCS
- numpy: Array operations
- scipy: Image processing
- opencv-python: Video creation (optional)
- plotly: Interactive visualizations (optional)

## Implementation Roadmap

1. **Phase 1**: Basic FITS image display with proper colormaps
2. **Phase 2**: Multi-panel layouts and comparisons
3. **Phase 3**: Preprocessing visualization tools
4. **Phase 4**: Animation and time series
5. **Phase 5**: ML prediction visualization
6. **Phase 6**: Interactive plotting

## Temporary Alternative

Until this module is implemented, users can use SunPy's built-in visualization:

```python
from sunpy.map import Map
import matplotlib.pyplot as plt

# Basic display
aia_map = Map('aia_lev2_171a.fits')
fig = plt.figure(figsize=(10, 10))
aia_map.plot()
plt.colorbar()
plt.show()

# Save to file
aia_map.plot()
plt.savefig('aia_171.png', dpi=150, bbox_inches='tight')
plt.close()
```

For multi-wavelength:
```python
import matplotlib.pyplot as plt
from sunpy.map import Map

files = ['aia_171.fits', 'aia_193.fits', 'aia_211.fits']
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, file in zip(axes, files):
    smap = Map(file)
    smap.plot(axes=ax)
    ax.set_title(f'{smap.wavelength}')

plt.tight_layout()
plt.savefig('multi_wavelength.png', dpi=150)
plt.close()
```

## Contributing

If you're interested in implementing this module, please:
1. Use SunPy's Map.plot() as foundation
2. Implement standard solar physics colormaps
3. Support both preprocessed and raw FITS files
4. Include coordinate system handling
5. Provide both scripting API and command-line interface

## Related Skills

- **ssw-download**: Download data to visualize
- **ssw-prep**: Preprocess data before visualization
- **ssw-ml**: (Planned) Visualize ML predictions
