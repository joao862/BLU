
# Sentinel-1 & Sentinel-2 Temporal Dataset Creator
## Microsoft Planetary Computer Version

This module provides tools to create temporally-aligned multi-modal satellite imagery datasets combining Sentinel-1 (SAR) and Sentinel-2 (optical) data using Microsoft Planetary Computer.

## Why Microsoft Planetary Computer?

- **No Authentication Required**: Unlike Google Earth Engine, MPC doesn't require complex authentication
- **Direct Data Access**: Download images directly to your local machine
- **STAC API**: Modern SpatioTemporal Asset Catalog interface
- **Free Access**: No quota limitations for data access
- **Cloud-Optimized**: Built on Azure with global CDN
- **Rich Collections**: Access to petabytes of environmental data

## Features

- **Dual-Sensor Data Acquisition**: Automatically fetch both Sentinel-1 and Sentinel-2 imagery
- **Temporal Alignment**: Match images from both sensors within a specified time window (default: 3 days)
- **Cloud Filtering**: Filter Sentinel-2 images by cloud coverage percentage (default: <5%)
- **Flexible Date Range**: Query data from 2016 onwards to present
- **Orbit Filtering**: Option to filter Sentinel-1 by orbit direction (ascending/descending)
- **Local Downloads**: Download matched pairs directly to your machine
- **Metadata Generation**: Automatically save dataset metadata in JSON format

## Installation

Install the required dependencies:

```bash
pip install planetary-computer pystac-client rasterio pandas shapely xarray
```

Or use the project requirements file:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from sentinel_dataset_mpc import create_dataset

# Define your bounding box (min_lon, min_lat, max_lon, max_lat)
bbox = (-122.5, 37.5, -122.0, 38.0)  # San Francisco Bay Area

# Create the dataset
s1_items, s2_items, matched_pairs = create_dataset(
    bbox=bbox,
    start_date='2023-01-01',
    end_date='2023-12-31',
    cloud_percentage=5.0,        # Max 5% cloud coverage
    max_time_diff_days=3,         # Max 3 days between S1 and S2
    output_dir='./my_dataset'
)

print(f"Found {len(matched_pairs)} temporally-aligned image pairs!")
```

### Downloading Images

```python
from sentinel_dataset_mpc import export_matched_pairs

# Download the first 10 matched pairs
export_matched_pairs(
    matched_pairs=matched_pairs[:10],
    output_dir='./my_dataset/images',
    s2_bands=['B04', 'B03', 'B02'],  # RGB bands
    s1_bands=['vh', 'vv']             # SAR polarizations
)
```

## Function Reference

### `create_dataset()`

Main function to create a temporally-aligned Sentinel-1/Sentinel-2 dataset.

**Parameters:**
- `bbox` (Tuple): Bounding box as (min_lon, min_lat, max_lon, max_lat)
- `start_date` (str): Start date in 'YYYY-MM-DD' format (default: '2016-01-01')
- `end_date` (str): End date in 'YYYY-MM-DD' format (default: today)
- `cloud_percentage` (float): Maximum cloud coverage for S2 (default: 5.0%)
- `max_time_diff_days` (int): Maximum temporal difference for pairing (default: 3 days)
- `output_dir` (str): Directory to save metadata (default: './sentinel_dataset_mpc')
- `orbit_direction` (str): S1 orbit direction ('ascending'/'descending'/None)

**Returns:**
- `s1_items` (List[Dict]): Sentinel-1 items with metadata
- `s2_items` (List[Dict]): Sentinel-2 items with metadata
- `matched_pairs` (List[Dict]): List of matched image pairs with metadata

### `export_matched_pairs()`

Download matched image pairs to local storage.

**Parameters:**
- `matched_pairs` (List[Dict]): List of matched pairs from `create_dataset()`
- `output_dir` (str): Output directory for downloaded images
- `max_pairs` (int): Maximum number of pairs to download (default: all)
- `s2_bands` (List[str]): Sentinel-2 bands to download (default: ['B04', 'B03', 'B02'])
- `s1_bands` (List[str]): Sentinel-1 bands to download (default: ['vh', 'vv'])

## Dataset Output Format

### Metadata JSON

The module creates a JSON file with the following structure:

```json
{
  "source": "Microsoft Planetary Computer",
  "bbox": [-122.5, 37.5, -122.0, 38.0],
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "cloud_percentage_threshold": 5.0,
  "max_time_diff_days": 3,
  "orbit_direction": null,
  "total_s1_images": 245,
  "total_s2_images": 156,
  "matched_pairs_count": 142,
  "matched_pairs": [
    {
      "s1_id": "S1A_IW_GRDH_1SDV_20230315T...",
      "s1_date": "2023-03-15",
      "s1_datetime": "2023-03-15 18:45:32",
      "s1_timestamp": 1678905932000,
      "s1_orbit": "ascending",
      "s2_id": "S2B_MSIL2A_20230317T...",
      "s2_date": "2023-03-17",
      "s2_datetime": "2023-03-17 11:23:41",
      "s2_timestamp": 1679053421000,
      "s2_cloud_cover": 2.34,
      "time_diff_days": 1.72
    }
  ]
}
```

## Usage Examples

### Example 1: Reservoir Monitoring Dataset

```python
# Define bbox for a reservoir area
bbox = (-8.4, 37.7, -8.3, 37.8)  # Reservoir in Portugal

# Create dataset with strict cloud filtering
s1_items, s2_items, pairs = create_dataset(
    bbox=bbox,
    start_date='2020-01-01',
    end_date='2023-12-31',
    cloud_percentage=3.0,  # Very strict
    max_time_diff_days=2,   # Close temporal alignment
    output_dir='./reservoir_monitoring'
)
```

### Example 2: Point-Based ROI with Buffer

```python
# Create bbox around a point
lon, lat = -122.4, 37.8  # San Francisco
buffer = 0.05  # ~5km

bbox = (lon - buffer, lat - buffer, lon + buffer, lat + buffer)

s1_items, s2_items, pairs = create_dataset(
    bbox=bbox,
    start_date='2022-01-01',
    cloud_percentage=5.0,
    output_dir='./point_dataset'
)
```

### Example 3: Orbit-Specific Dataset

```python
# Only use ascending Sentinel-1 passes
s1_items, s2_items, pairs = create_dataset(
    bbox=my_bbox,
    start_date='2023-01-01',
    end_date='2023-12-31',
    orbit_direction='ascending',
    output_dir='./ascending_only'
)
```

### Example 4: Download with Specific Bands

```python
# Download with NIR band for vegetation analysis
export_matched_pairs(
    matched_pairs=pairs[:10],
    output_dir='./vegetation_dataset',
    s2_bands=['B08', 'B04', 'B03'],  # NIR, Red, Green
    s1_bands=['vh', 'vv']
)
```

## Available Sentinel-2 Bands

| Band | Resolution | Wavelength | Description |
|------|-----------|------------|-------------|
| B01 | 60m | 443nm | Coastal aerosol |
| B02 | 10m | 490nm | Blue |
| B03 | 10m | 560nm | Green |
| B04 | 10m | 665nm | Red |
| B05 | 20m | 705nm | Red edge 1 |
| B06 | 20m | 740nm | Red edge 2 |
| B07 | 20m | 783nm | Red edge 3 |
| B08 | 10m | 842nm | NIR |
| B8A | 20m | 865nm | NIR narrow |
| B09 | 60m | 945nm | Water vapor |
| B11 | 20m | 1610nm | SWIR 1 |
| B12 | 20m | 2190nm | SWIR 2 |

## Available Sentinel-1 Bands

- **VV**: Vertical transmit, vertical receive polarization
- **VH**: Vertical transmit, horizontal receive polarization
- **HH**: Horizontal transmit, horizontal receive (some areas)
- **HV**: Horizontal transmit, vertical receive (some areas)

## Satellite Data Specifications

### Sentinel-1 (SAR)
- **Collection**: sentinel-1-rtc (Radiometrically Terrain Corrected)
- **Start Date**: 2014-10-03 (S1A), 2016-04-25 (S1B)
- **Resolution**: 10m (RTC product)
- **Revisit Time**: 6 days (with both satellites)
- **Weather**: All-weather capable (SAR)

### Sentinel-2 (Optical)
- **Collection**: sentinel-2-l2a (Level-2A Surface Reflectance)
- **Start Date**: 2015-06-23 (S2A), 2017-03-07 (S2B)
- **Bands**: 13 spectral bands (visible to SWIR)
- **Resolution**: 10m (visible/NIR), 20m (red edge/SWIR), 60m (coastal/cirrus)
- **Revisit Time**: 5 days (with both satellites)
- **Weather**: Clear sky required

## How to Define Bounding Boxes

### From Coordinates
```python
# Direct specification
bbox = (min_lon, min_lat, max_lon, max_lat)
bbox = (-122.5, 37.5, -122.0, 38.0)
```

### From Point with Buffer
```python
lon, lat = -122.4, 37.8
buffer_deg = 0.05  # ~5km
bbox = (lon - buffer_deg, lat - buffer_deg,
        lon + buffer_deg, lat + buffer_deg)
```

### From Place Names (using external geocoder)
```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode("San Francisco, CA")

buffer = 0.1
bbox = (location.longitude - buffer, location.latitude - buffer,
        location.longitude + buffer, location.latitude + buffer)
```

## Performance Tips

1. **Start Small**: Test with 3-6 months before processing years of data
2. **Optimize Bbox Size**: Smaller areas process and download faster
3. **Cloud Threshold**: Lower thresholds (1-5%) give better quality but fewer images
4. **Temporal Window**: 2-3 days balances quantity and temporal alignment
5. **Download in Batches**: Download 5-10 pairs at a time to monitor progress
6. **Band Selection**: Only download the bands you need to save time and storage

## Common Use Cases

- **Change Detection**: Monitor land cover changes with multi-modal data
- **Disaster Response**: Combine SAR (cloud-penetrating) with optical imagery
- **Agriculture**: Track crop growth with temporal multi-sensor data
- **Water Resources**: Monitor reservoirs, rivers, and wetlands
- **Machine Learning**: Create training datasets for multi-modal deep learning models
- **Environmental Monitoring**: Track deforestation, urban growth, etc.

## Troubleshooting

### No Matched Pairs Found
- **Solution**: Increase `cloud_percentage` or `max_time_diff_days`
- Check that your bbox has coverage from both sensors
- Verify date range includes operational periods for both satellites

### Too Few Images
- **Solution**: Expand date range or increase cloud coverage threshold
- Consider using `orbit_direction=None` to include both ascending and descending

### Download Errors
- **Solution**: Check your internet connection
- Reduce the number of pairs being downloaded at once
- Check if the bbox is too large

### Slow Downloads
- **Solution**: Reduce the number of bands
- Download fewer pairs at a time
- Check network bandwidth

## Comparison: Microsoft Planetary Computer vs Google Earth Engine

| Feature | MPC | GEE |
|---------|-----|-----|
| Authentication | Not required | Required (OAuth) |
| Data Access | Direct download | Cloud processing |
| Processing | Local | Server-side |
| Storage | Local machine | Google Drive/Cloud |
| Quota | None for access | Limited compute units |
| Setup Complexity | Simple | Moderate |
| Best For | Direct data access | Large-scale analysis |

## References

- [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/)
- [Planetary Computer Data Catalog](https://planetarycomputer.microsoft.com/catalog)
- [STAC API Documentation](https://stacspec.org/)
- [Sentinel-1 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar)
- [Sentinel-2 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi)

## License

This module is part of the BLU Reservoir Monitoring Platform.

## Contributing

To add new features or report issues, please contribute to the main repository.
