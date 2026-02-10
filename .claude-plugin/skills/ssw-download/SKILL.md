# ssw-download

Solar observation data downloader for STEREO and Solar Orbiter missions.

## Description

This skill provides data download capabilities for STEREO and Solar Orbiter solar observation missions. It uses SunPy's Fido interface to fetch EUV imagery and automatically pairs multi-wavelength observations taken within a specified time tolerance.

## When to Use

Use this skill when Claude needs to:
1. Download STEREO/SECCHI/EUVI data (171Å and 304Å)
2. Download Solar Orbiter/EUI/FSI data (174Å and 304Å)
3. Create time series of paired multi-wavelength observations
4. Find and download observations closest to a specific target time

## Triggers

This skill is automatically invoked when users mention:
- 'STEREO data download'
- 'Solar Orbiter download'
- 'EUVI data'
- 'EUI data'
- 'FSI data'
- 'solar observation download'
- '태양 데이터 다운로드'
- '태양 관측 데이터'

## Supported Missions

### STEREO (Solar Terrestrial Relations Observatory)
- **Instrument**: SECCHI/EUVI
- **Spacecraft**: STEREO-A
- **Wavelengths**: 171Å, 304Å
- **Data Source**: SSC (Solar Data Analysis Center)
- **Implementation**: `stereo_down.py`

### Solar Orbiter
- **Instrument**: EUI (Extreme Ultraviolet Imager) / FSI (Full Sun Imager)
- **Wavelengths**: 174Å, 304Å
- **Data Source**: SOAR (Solar Orbiter Archive)
- **Implementation**: `solo_down.py`

## Core Functions

### STEREO Download: `run_stereo()`
```python
from ssw_tools.download_data.stereo_down import run_stereo
from datetime import datetime

run_stereo(
    start_date=datetime(2012, 7, 15, 0, 0),
    end_date=datetime(2012, 7, 16, 0, 0),
    delta_hours=12,              # Search window: ±12 hours
    out_path="./data/stereo/",
    level=1,                     # Data processing level
    tolerance_min=15,            # Pairing tolerance: 15 minutes
    cadence_min=1440             # Download every 24 hours
)
```

**Parameters:**
- `start_date`: Start time for data search
- `end_date`: End time (optional, defaults to start_date)
- `delta_hours`: Time window around target time for searching
- `out_path`: Output directory for downloaded FITS files
- `level`: Data processing level (1 or 2)
- `tolerance_min`: Maximum time difference for wavelength pairing
- `cadence_min`: Time interval between downloads (in minutes)

**Output Structure:**
```
out_path/
├── stereo-174/
│   └── [downloaded 171Å FITS files]
└── stereo-304/
    └── [downloaded 304Å FITS files]
```

### Solar Orbiter Download: `run_solo()`
```python
from ssw_tools.download_data.solo_down import run_solo
from datetime import datetime

run_solo(
    start_date=datetime(2022, 3, 1, 0, 0),
    end_date=datetime(2022, 3, 2, 0, 0),
    delta_hours=12,
    out_path="./data/solo/",
    level=2,
    tolerance_min=15,
    cadence_min=1440
)
```

**Output Structure:**
```
out_path/
├── solo/174/
│   └── [downloaded 174Å FITS files]
└── solo/304/
    └── [downloaded 304Å FITS files]
```

## Command-Line Interface

### Unified Interface (main.py)
```bash
# Download STEREO data
python -m ssw_tools.download_data.main \
    --target stereo-a \
    --start_date 2012-07-15T00:00 \
    --end_date 2012-07-16T00:00 \
    --delta_hours 12 \
    --out_path ./data/ \
    --level 1 \
    --tolerance_min 15 \
    --cadence_min 1440

# Download Solar Orbiter data
python -m ssw_tools.download_data.main \
    --target solo \
    --start_date 2022-03-01T00:00 \
    --delta_hours 12 \
    --out_path ./data/
```

### Individual Module Execution
```bash
# STEREO download
python -m ssw_tools.download_data.stereo_down \
    --start_date 2012-07-15T00:00 \
    --end_date 2012-07-16T00:00 \
    --out_path ./data/

# Solar Orbiter download
python -m ssw_tools.download_data.solo_down \
    --start_date 2022-03-01T00:00 \
    --out_path ./data/
```

## Key Features

### 1. Automatic Wavelength Pairing
The system automatically finds and pairs observations from different wavelengths (e.g., 171Å and 304Å) taken within the specified tolerance window (default: 15 minutes).

### 2. Nearest Time Selection
When multiple observation pairs exist, the system selects the pair closest to the target `start_date`.

### 3. Time Series Support
Use `end_date` and `cadence_min` to download sequences of observations over extended periods.

### 4. Robust Search
The `delta_hours` parameter defines a search window around each target time to find available observations.

## Algorithm

For each target time:
1. Query both wavelengths within ±`delta_hours` window
2. Convert results to pandas DataFrames with timestamps
3. Use `merge_asof` to pair observations within `tolerance_min`
4. Select the pair closest to the target time
5. Download both FITS files
6. Advance by `cadence_min` and repeat until `end_date`

## Output Format

Downloaded files are FITS (Flexible Image Transport System) format containing:
- **Image data**: EUV observations (typically 2048×2048 or 4096×4096 pixels)
- **Header metadata**: Observation time, wavelength, spacecraft position, exposure time, etc.

## Dependencies

- `sunpy`: Solar physics data analysis library
- `sunpy-soar`: Solar Orbiter Archive interface
- `astropy`: Astronomy data handling
- `pandas`: Data manipulation for pairing
- `dateutil`: Date/time utilities

## Limitations

- **No SDO/AIA support**: This module does NOT download SDO/AIA data (use JSOC tools separately)
- **STEREO-A only**: Currently only STEREO-A is supported (not STEREO-B)
- **Fixed wavelengths**: Only supports 171/174Å and 304Å pairs
- **Pairing requirement**: Both wavelengths must be available within tolerance

## Notes

- Download speeds depend on server availability (SSC for STEREO, SOAR for Solar Orbiter)
- SOAR may be slower for recent data
- Use level=2 for higher-quality calibrated data when available
- Large time ranges with small cadence can result in many downloads

## Related Skills

- **ssw-prep**: Preprocess downloaded FITS files for ML applications
- **ssw-viz**: (Planned) Visualize downloaded solar observation data
- **ssw-ml**: (Planned) Train ML models on downloaded datasets
