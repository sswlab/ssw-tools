# ssw-viz

Solar observation data visualization for EUV imagery, ML results, and analysis.

## Description

This skill provides comprehensive visualization capabilities for solar observation data, preprocessing results, and machine learning model outputs. It offers specialized plotting functions designed for solar physics data with proper color maps, coordinate systems, and physical units.

## When to Use

Use this skill when Claude needs to:
1. Display solar EUV images from FITS files
2. Create multi-wavelength comparison panels
3. Make before/after preprocessing comparisons
4. Visualize ML model predictions on solar data
5. Create solar time-lapse animations
6. Plot intensity distributions of solar images

## Triggers

This skill is automatically invoked when users mention:
- 'solar visualization'
- 'solar image display'
- 'FITS visualization'
- 'EUV image plot'
- 'multi-wavelength comparison'
- 'solar animation'
- 'sun image'
- '태양 이미지 시각화'
- '태양 시각화'
- 'solar plot'

## Visualization Types

### 1. Single Image Display
Display individual solar EUV observations with proper color mapping and annotations.

### 2. Multi-Wavelength Panels
Create side-by-side or grid comparisons of different wavelength observations.

### 3. Time Series Visualization
Show temporal evolution of solar features through image sequences or animations.

### 4. Preprocessing Comparison
Before/after views of preprocessing steps (calibration, normalization, registration).

### 5. ML Prediction Overlay
Visualize model predictions (segmentation masks, detection boxes) overlaid on input images.

### 6. Quantitative Analysis Plots
- Intensity distributions and histograms
- Radial profiles
- Light curves
- Feature tracking

## Usage Examples

### Display Single FITS Image
```python
from ssw_tools.viz import plot_solar_image

# Load and display AIA 171Å image
plot_solar_image(
    'aia_20230101_000000_171.fits',
    cmap='sdoaia171',  # Standard AIA color map
    title='SDO/AIA 171Å',
    colorbar=True,
    grid=True,
    save='output/aia171.png'
)
```

### Multi-Wavelength Comparison
```python
from ssw_tools.viz import plot_multi_wavelength

wavelengths = [94, 131, 171, 193, 211, 304]
files = [f'aia_20230101_000000_{wl}.fits' for wl in wavelengths]

plot_multi_wavelength(
    files,
    wavelengths=wavelengths,
    layout=(2, 3),  # 2 rows, 3 columns
    figsize=(15, 10),
    share_colorbar=False,  # Individual colorbars
    save='output/multi_wavelength.png'
)
```

### Before/After Preprocessing
```python
from ssw_tools.viz import plot_preprocessing_comparison

plot_preprocessing_comparison(
    before='raw/aia_171_raw.fits',
    after='processed/aia_171_processed.npy',
    titles=['Raw Level 1', 'Preprocessed ML-ready'],
    cmap='sdoaia171',
    save='output/preprocessing_comparison.png'
)
```

### ML Segmentation Overlay
```python
from ssw_tools.viz import plot_segmentation_overlay

# Display coronal hole detection results
plot_segmentation_overlay(
    image='aia_193.npy',
    mask='predictions/ch_mask.npy',
    overlay_alpha=0.4,
    mask_color='cyan',
    cmap='sdoaia193',
    title='Coronal Hole Detection (193Å)',
    save='output/ch_detection.png'
)
```

### Active Region Detection Boxes
```python
from ssw_tools.viz import plot_detection_boxes

# Visualize AR detection results
plot_detection_boxes(
    image='magnetogram.fits',
    boxes=detection_results['boxes'],
    labels=detection_results['labels'],
    scores=detection_results['scores'],
    threshold=0.5,  # Confidence threshold
    cmap='hmimag',  # Magnetogram color map
    save='output/ar_detection.png'
)
```

### Time-Lapse Animation
```python
from ssw_tools.viz import create_animation

# Create movie from image sequence
create_animation(
    image_files=sorted(glob.glob('timeseries/*.fits')),
    output='animations/solar_evolution.mp4',
    fps=10,
    cmap='sdoaia171',
    title_template='SDO/AIA 171Å - {timestamp}',
    colorbar=True,
    dpi=150
)
```

### Intensity Distribution
```python
from ssw_tools.viz import plot_intensity_histogram

# Analyze intensity distribution
plot_intensity_histogram(
    'aia_171.fits',
    bins=100,
    log_scale=True,  # Logarithmic intensity scale
    show_stats=True,  # Display mean, median, std
    save='output/intensity_dist.png'
)
```

### Radial Profile
```python
from ssw_tools.viz import plot_radial_profile

# Plot intensity as function of radius from disk center
plot_radial_profile(
    'aia_193.fits',
    center='auto',  # Automatically detect disk center
    rmax=1.3,  # Extend to 1.3 solar radii
    nbins=100,
    title='193Å Radial Intensity Profile',
    save='output/radial_profile.png'
)
```

### Difference Image
```python
from ssw_tools.viz import plot_difference_image

# Show temporal changes
plot_difference_image(
    image1='aia_t0.fits',
    image2='aia_t1.fits',
    method='running',  # or 'base'
    cmap='RdBu_r',  # Diverging colormap
    symmetric=True,  # Center colorbar at zero
    title='Running Difference (ΔT = 5 min)',
    save='output/difference.png'
)
```

## Standard AIA Color Maps

Wavelength-specific color tables:
- **sdoaia94**: Teal (hot corona)
- **sdoaia131**: Purple (flare plasma)
- **sdoaia171**: Gold/yellow (quiet corona)
- **sdoaia193**: Bronze (hot active regions)
- **sdoaia211**: Pink (active regions)
- **sdoaia304**: Red (chromosphere)
- **sdoaia335**: Blue (active region corona)
- **sdoaia1600**: Yellow-white (UV continuum)
- **sdoaia1700**: White (temperature minimum)

Magnetogram:
- **hmimag**: Gray scale for line-of-sight magnetic field

## Advanced Visualization

### Interactive Plotting
```python
from ssw_tools.viz import interactive_viewer

# Launch interactive viewer with zoom, pan, intensity inspection
viewer = interactive_viewer('aia_171.fits')
viewer.add_contours(threshold=0.5)
viewer.add_coordinate_grid()
viewer.launch()
```

### Composite RGB Images
```python
from ssw_tools.viz import create_rgb_composite

# Create false-color RGB composite
create_rgb_composite(
    red='aia_211.fits',    # Hot active regions
    green='aia_193.fits',  # Coronal loops
    blue='aia_171.fits',   # Quiet corona
    output='composite_rgb.png',
    enhance=True,  # Contrast enhancement
    align=True     # Align images
)
```

### Feature Tracking Visualization
```python
from ssw_tools.viz import plot_feature_tracking

# Visualize tracked features over time
plot_feature_tracking(
    image_sequence=images,
    tracks=tracking_results,
    feature_type='coronal_hole',
    color_by='id',  # Color by feature ID
    show_velocity=True,
    save='output/tracking.png'
)
```

### ML Model Attention Maps
```python
from ssw_tools.viz import plot_attention_map

# Visualize what ML model focuses on
plot_attention_map(
    input_image='aia_171.npy',
    attention=gradcam_output,
    overlay_alpha=0.5,
    cmap_attention='jet',
    title='Model Attention for Flare Prediction',
    save='output/attention.png'
)
```

## Coordinate Systems

Supports proper solar coordinate transformations:
- **Helioprojective-Cartesian (HPC)**: Arcseconds from disk center
- **Heliographic-Stonyhurst (HGS)**: Latitude/longitude on solar surface
- **Heliographic-Carrington (HGC)**: Rotating coordinate system

```python
from ssw_tools.viz import plot_with_coordinates

plot_with_coordinates(
    'aia_171.fits',
    coord_system='heliographic',
    grid_spacing=10,  # 10-degree grid
    draw_limb=True,
    draw_equator=True
)
```

## Export Formats

Supported output formats:
- **PNG**: High-quality raster (default)
- **PDF**: Vector format for publications
- **SVG**: Scalable vector graphics
- **FITS**: Annotated FITS with overlays
- **MP4/GIF**: Animations

## Publication-Ready Figures

```python
from ssw_tools.viz import publication_plot

# Generate publication-quality figure
publication_plot(
    'aia_171.fits',
    figsize=(8, 8),
    dpi=300,
    fontsize=12,
    title='SDO/AIA 171 Å Observation',
    timestamp_format='%Y-%m-%d %H:%M:%S UT',
    colorbar_label='Intensity [DN/s]',
    save='figures/publication_fig.pdf'
)
```

## Dependencies

- **matplotlib**: Core plotting library
- **sunpy**: Solar physics visualization tools
- **astropy**: FITS file handling and coordinates
- **numpy**: Array operations
- **scipy**: Image processing
- **opencv-python**: Video/animation creation
- **plotly**: Interactive visualizations (optional)

## Performance Tips

- Use downsampling for quick preview of large images
- Enable caching for repeated visualizations
- Use vector formats (PDF/SVG) for small datasets
- Parallel rendering for batch visualization

## Customization

```python
from ssw_tools.viz import set_visualization_defaults

# Set global visualization preferences
set_visualization_defaults(
    style='publication',  # or 'presentation', 'web'
    cmap_default='sdoaia171',
    figsize=(10, 10),
    dpi=150,
    colorbar=True,
    grid=False
)
```

## Related Skills

- **ssw-download**: Download data to visualize
- **ssw-prep**: Preprocess data before visualization
- **ssw-ml**: Visualize ML model predictions and training results
