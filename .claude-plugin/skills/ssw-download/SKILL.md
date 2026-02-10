# ssw-download

Solar observation data downloader for SDO, STEREO, and Solar Orbiter missions.

## Description

This skill provides comprehensive capabilities for downloading solar observation data from multiple space missions. It specializes in fetching EUV (Extreme Ultraviolet) imagery and associated metadata from major solar observation satellites.

## When to Use

Use this skill when Claude needs to:
1. Download SDO/AIA EUV data from JSOC (Joint Science Operations Center)
2. Download STEREO/SECCHI/EUVI data
3. Download Solar Orbiter/EUI/FSI data
4. Create multi-date time series of solar observations
5. Pair multi-wavelength observations for comparative analysis

## Triggers

This skill is automatically invoked when users mention:
- 'solar data download'
- 'SDO download'
- 'AIA data'
- 'STEREO data'
- 'Solar Orbiter data'
- 'FITS download'
- 'sun observation data'
- 'EUI data'
- 'EUVI data'
- '태양 데이터 다운로드'
- '태양 관측 데이터'

## Supported Missions

### SDO (Solar Dynamics Observatory)
- **Instrument**: AIA (Atmospheric Imaging Assembly)
- **Wavelengths**: 94Å, 131Å, 171Å, 193Å, 211Å, 304Å, 335Å, 1600Å, 1700Å, 4500Å
- **Cadence**: 12 seconds for EUV channels, 24 seconds for UV/continuum
- **Data Source**: JSOC at Stanford University

### STEREO (Solar Terrestrial Relations Observatory)
- **Instrument**: SECCHI/EUVI
- **Spacecraft**: STEREO-A and STEREO-B
- **Wavelengths**: 171Å, 195Å, 284Å, 304Å
- **Viewing Angle**: Provides stereoscopic views of the Sun

### Solar Orbiter
- **Instrument**: EUI (Extreme Ultraviolet Imager) / FSI (Full Sun Imager)
- **Wavelengths**: 174Å, 304Å
- **Special Features**: Variable distance observations, off-ecliptic views

## Usage Examples

### Download single SDO/AIA image
```python
from ssw_tools.download import download_aia_data

download_aia_data(
    start_time='2023-01-01 00:00:00',
    wavelength=171,
    output_dir='./data/aia'
)
```

### Download time series
```python
download_aia_data(
    start_time='2023-01-01 00:00:00',
    end_time='2023-01-01 01:00:00',
    wavelength=193,
    cadence='5m',  # 5 minute intervals
    output_dir='./data/timeseries'
)
```

### Download multi-wavelength data
```python
wavelengths = [94, 131, 171, 193, 211, 304]
for wl in wavelengths:
    download_aia_data(
        start_time='2023-01-01 12:00:00',
        wavelength=wl,
        output_dir=f'./data/multi_wl/{wl}'
    )
```

## Output Format

Downloaded files are in FITS (Flexible Image Transport System) format with:
- **Filename convention**: `aia_YYYYMMDDTHHMMSSz_WWWW.fits`
- **Header metadata**: Observation time, wavelength, exposure time, spacecraft coordinates
- **Image data**: 16-bit integer arrays (typically 4096×4096 pixels)

## Dependencies

- `sunpy`: Solar physics data analysis library
- `astropy`: Astronomy data handling
- `requests`: HTTP library for data retrieval
- `drms`: Python interface to JSOC data export system

## Notes

- JSOC downloads may require email registration for large batch requests
- Download speeds depend on JSOC server load
- Recommended to use cadence >= 1 minute for time series to avoid overwhelming servers
- FITS files can be large (10-50 MB per image)

## Related Skills

- **ssw-prep**: Preprocess downloaded FITS files for ML applications
- **ssw-viz**: Visualize downloaded solar observation data
- **ssw-ml**: Train ML models on downloaded datasets
