# Sentinel-1 & Sentinel-2 Temporal Dataset Creator

This module provides tools to create temporally-aligned multi-modal satellite imagery datasets combining Sentinel-1 (SAR) and Sentinel-2 (optical) data.

## Features

- **Dual-Sensor Data Acquisition**: Automatically fetch both Sentinel-1 and Sentinel-2 imagery
- **Temporal Alignment**: Match images from both sensors within a specified time window (default: 3 days)
- **Cloud Filtering**: Filter Sentinel-2 images by cloud coverage percentage (default: <5%)
- **Flexible Date Range**: Query data from 2016 onwards to present
- **Orbit Filtering**: Option to filter Sentinel-1 by orbit direction (ascending/descending)
- **Export Capability**: Export matched pairs to Google Drive or Cloud Storage
- **Metadata Generation**: Automatically save dataset metadata in JSON format

## Installation

Ensure you have the required dependencies installed:

```bash
pip install earthengine-api pandas
```

## Authentication

Before using this module, authenticate with Google Earth Engine:

```python
import ee
ee.Authenticate()
ee.Initialize()
```

## Quick Start

### Basic Usage

```python
import ee
from sentinel_dataset import initialize_earth_engine, create_dataset

# Initialize Earth Engine
initialize_earth_engine()

# Define your Region of Interest (ROI)
roi = ee.Geometry.Rectangle([-122.5, 37.5, -122.0, 38.0])

# Create the dataset
s1_collection, s2_collection, matched_pairs = create_dataset(
    roi=roi,
    start_date='2016-01-01',
    end_date='2024-12-31',
    cloud_percentage=5.0,        # Max 5% cloud coverage
    max_time_diff_days=3,         # Max 3 days between S1 and S2
    output_dir='./my_dataset'
)

print(f"Found {len(matched_pairs)} temporally-aligned image pairs!")
```

### Exporting Images

```python
from sentinel_dataset import export_matched_images

# Export the first 10 matched pairs to Google Drive
export_matched_images(
    matched_pairs=matched_pairs[:10],
    s1_collection=s1_collection,
    s2_collection=s2_collection,
    roi=roi,
    output_folder='Sentinel_Dataset',
    scale=10,  # 10m resolution
    export_to='drive'
)
```

## Function Reference

### `create_dataset()`

Main function to create a temporally-aligned Sentinel-1/Sentinel-2 dataset.

**Parameters:**
- `roi` (ee.Geometry): Region of Interest
- `start_date` (str): Start date in 'YYYY-MM-DD' format (default: '2016-01-01')
- `end_date` (str): End date in 'YYYY-MM-DD' format (default: today)
- `cloud_percentage` (float): Maximum cloud coverage for S2 (default: 5.0%)
- `max_time_diff_days` (int): Maximum temporal difference for pairing (default: 3 days)
- `output_dir` (str): Directory to save metadata (default: './sentinel_dataset')
- `s1_orbit` (str): S1 orbit direction ('ASCENDING'/'DESCENDING'/None)

**Returns:**
- `s1_collection` (ee.ImageCollection): Sentinel-1 image collection
- `s2_collection` (ee.ImageCollection): Sentinel-2 image collection
- `matched_pairs` (List[Dict]): List of matched image pairs with metadata

### `export_matched_images()`

Export matched image pairs to Google Drive or Cloud Storage.

**Parameters:**
- `matched_pairs` (List[Dict]): List of matched pairs from `create_dataset()`
- `s1_collection` (ee.ImageCollection): Sentinel-1 collection
- `s2_collection` (ee.ImageCollection): Sentinel-2 collection
- `roi` (ee.Geometry): Region of Interest
- `output_folder` (str): Output folder name
- `scale` (int): Export resolution in meters (default: 10m)
- `export_to` (str): 'drive' or 'cloud' (default: 'drive')

## Dataset Output Format

### Metadata JSON

The module creates a JSON file with the following structure:

```json
{
  "roi": {...},
  "start_date": "2016-01-01",
  "end_date": "2024-12-31",
  "cloud_percentage_threshold": 5.0,
  "max_time_diff_days": 3,
  "s1_orbit": null,
  "total_s1_images": 245,
  "total_s2_images": 156,
  "matched_pairs_count": 142,
  "matched_pairs": [
    {
      "s1_index": "S1A_IW_GRDH_1SDV_20160315T...",
      "s1_date": "2016-03-15",
      "s1_timestamp": 1458086400000,
      "s2_index": "20160317T185742_20160317T...",
      "s2_date": "2016-03-17",
      "s2_timestamp": 1458259062000,
      "time_diff_days": 2.15
    },
    ...
  ]
}
```

## Usage Examples

### Example 1: Reservoir Monitoring Dataset

```python
# Define reservoir location
reservoir_roi = ee.Geometry.Polygon([
    [[-8.4, 37.8], [-8.4, 37.7], [-8.3, 37.7], [-8.3, 37.8]]
])

# Create dataset with strict cloud filtering
s1_coll, s2_coll, pairs = create_dataset(
    roi=reservoir_roi,
    start_date='2020-01-01',
    end_date='2023-12-31',
    cloud_percentage=3.0,  # Very strict
    max_time_diff_days=2,   # Close temporal alignment
    output_dir='./reservoir_monitoring'
)
```

### Example 2: Point-Based ROI with Buffer

```python
# Create ROI around a point with 10km buffer
point = ee.Geometry.Point([-122.4, 37.8])
roi = point.buffer(10000)

s1_coll, s2_coll, pairs = create_dataset(
    roi=roi,
    start_date='2022-01-01',
    cloud_percentage=5.0,
    output_dir='./point_dataset'
)
```

### Example 3: Orbit-Specific Dataset

```python
# Only use ascending Sentinel-1 passes
s1_coll, s2_coll, pairs = create_dataset(
    roi=my_roi,
    start_date='2019-01-01',
    end_date='2019-12-31',
    s1_orbit='ASCENDING',
    output_dir='./ascending_only'
)
```

## Satellite Data Specifications

### Sentinel-1 (SAR)
- **Collection**: COPERNICUS/S1_GRD
- **Start Date**: 2014-10-03 (S1A), 2016-04-25 (S1B)
- **Bands**: VV, VH (or HH, HV depending on mode)
- **Resolution**: ~10m (IW mode)
- **Revisit Time**: 6 days (with both satellites)
- **Weather**: All-weather capable (SAR)

### Sentinel-2 (Optical)
- **Collection**: COPERNICUS/S2_SR (Surface Reflectance)
- **Start Date**: 2015-06-23 (S2A), 2017-03-07 (S2B)
- **Bands**: 13 spectral bands (visible to SWIR)
- **Resolution**: 10m (visible/NIR), 20m (red edge/SWIR), 60m (coastal/cirrus)
- **Revisit Time**: 5 days (with both satellites)
- **Weather**: Clear sky required

## Temporal Matching Algorithm

The module matches Sentinel-1 and Sentinel-2 images using the following process:

1. **Filter Collections**: Both collections are filtered by ROI, date range, and quality criteria
2. **Extract Timestamps**: Image acquisition times are extracted
3. **Nearest Neighbor Matching**: For each S2 image, find the closest S1 image
4. **Time Threshold**: Only pairs within `max_time_diff_days` are kept
5. **Metadata Export**: Matched pairs are saved with timing information

## Performance Tips

1. **Start Small**: Test with a short date range (e.g., 6 months) before processing years of data
2. **Optimize ROI Size**: Smaller ROIs process faster; consider tiling large areas
3. **Cloud Threshold**: Lower cloud thresholds (1-5%) give better quality but fewer images
4. **Temporal Window**: A 2-3 day window balances quantity and temporal alignment
5. **Export Limits**: Export in batches (10-20 pairs) to avoid timeouts

## Common Use Cases

- **Change Detection**: Monitor land cover changes with multi-modal data
- **Disaster Response**: Combine SAR (cloud-penetrating) with optical imagery
- **Agriculture**: Track crop growth with temporal multi-sensor data
- **Water Resources**: Monitor reservoirs, rivers, and wetlands
- **Machine Learning**: Create training datasets for multi-modal deep learning models

## Troubleshooting

### No Matched Pairs Found
- **Solution**: Increase `cloud_percentage` or `max_time_diff_days`
- Check that your ROI has coverage from both sensors
- Verify date range includes operational periods for both satellites

### Too Few Images
- **Solution**: Expand date range or increase cloud coverage threshold
- Consider using `s1_orbit=None` to include both ascending and descending

### Export Errors
- **Solution**: Reduce `scale` parameter or ROI size
- Ensure you're authenticated with Google Earth Engine
- Check Google Drive storage quota

## References

- [Google Earth Engine Documentation](https://developers.google.com/earth-engine)
- [Sentinel-1 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar)
- [Sentinel-2 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi)

## License

This module is part of the BLU Reservoir Monitoring Platform.

## Contributing

To add new features or report issues, please contribute to the main repository.
