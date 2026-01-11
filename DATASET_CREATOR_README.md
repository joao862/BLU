# Sentinel-1 & Sentinel-2 Temporal Dataset Creator

Create temporally-aligned multi-modal satellite imagery datasets combining Sentinel-1 (SAR) and Sentinel-2 (optical) data.

## 🎯 Overview

This project provides tools to:
- Fetch Sentinel-1 and Sentinel-2 satellite imagery
- Filter images since 2016 with cloud coverage < 5%
- Match images that are within 2-3 days apart
- Create datasets for machine learning, change detection, and environmental monitoring

## 📦 Two Implementations Available

### 1. Microsoft Planetary Computer (Recommended)
**Files:** `sentinel_dataset_mpc.py`, `example_usage_mpc.py`, `sentinel_dataset_mpc_notebook.ipynb`

**Advantages:**
- ✅ No authentication required
- ✅ Direct download to local machine
- ✅ No quota limitations
- ✅ Simple setup
- ✅ Modern STAC API

**Best for:** Direct data access, local analysis, small to medium datasets

See: [`README_SENTINEL_DATASET_MPC.md`](README_SENTINEL_DATASET_MPC.md)

### 2. Google Earth Engine
**Files:** `sentinel_dataset.py`, `example_usage.py`, `sentinel_dataset_notebook.ipynb`

**Advantages:**
- ✅ Cloud-based processing
- ✅ Handle very large areas
- ✅ Export to Google Drive
- ✅ Integrated with GEE ecosystem

**Best for:** Large-scale analysis, cloud processing, existing GEE workflows

See: [`SENTINEL_DATASET_README.md`](SENTINEL_DATASET_README.md)

## 🚀 Quick Start

### Microsoft Planetary Computer (Easiest)

```python
from sentinel_dataset_mpc import create_dataset

# Define bounding box (min_lon, min_lat, max_lon, max_lat)
bbox = (-122.5, 37.5, -122.0, 38.0)

# Create dataset
s1_items, s2_items, matched_pairs = create_dataset(
    bbox=bbox,
    start_date='2023-01-01',
    end_date='2023-12-31',
    cloud_percentage=5.0,
    max_time_diff_days=3
)

print(f"Found {len(matched_pairs)} matched pairs!")
```

### Google Earth Engine

```python
import ee
from sentinel_dataset import initialize_earth_engine, create_dataset

# Initialize
initialize_earth_engine()

# Define ROI
roi = ee.Geometry.Rectangle([-122.5, 37.5, -122.0, 38.0])

# Create dataset
s1_coll, s2_coll, matched_pairs = create_dataset(
    roi=roi,
    start_date='2023-01-01',
    cloud_percentage=5.0,
    max_time_diff_days=3
)
```

## 📋 Installation

### For Microsoft Planetary Computer

```bash
pip install planetary-computer pystac-client rasterio pandas shapely xarray
```

### For Google Earth Engine

```bash
pip install earthengine-api
ee authenticate
ee initialize
```

### Install All Dependencies

```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
BLU/
├── sentinel_dataset_mpc.py              # MPC implementation
├── sentinel_dataset.py                   # GEE implementation
├── example_usage_mpc.py                  # MPC examples
├── example_usage.py                      # GEE examples
├── sentinel_dataset_mpc_notebook.ipynb   # MPC Jupyter notebook
├── sentinel_dataset_notebook.ipynb       # GEE Jupyter notebook
├── README_SENTINEL_DATASET_MPC.md        # MPC documentation
├── SENTINEL_DATASET_README.md            # GEE documentation
├── DATASET_CREATOR_README.md             # This file
└── requirements.txt                      # Python dependencies
```

## 🎓 Features

### Data Acquisition
- **Sentinel-1**: SAR imagery (all-weather, day/night)
- **Sentinel-2**: Optical imagery (13 spectral bands)
- **Date Range**: 2016 onwards to present
- **Global Coverage**: Any location worldwide

### Filtering
- ☁️ Cloud coverage threshold (default: <5%)
- 📅 Temporal alignment (default: ±3 days)
- 🛰️ Orbit direction (ascending/descending)
- 📍 Region of Interest (bbox or geometry)

### Output
- 📊 JSON metadata with matched pairs
- 📈 CSV export for analysis
- 🖼️ Direct image download (MPC)
- ☁️ Google Drive export (GEE)

## 📊 Use Cases

### 🌾 Agriculture
Monitor crop growth with temporal multi-sensor data
- Combine SAR for soil moisture with optical for vegetation health
- Track seasonal changes across growing seasons

### 💧 Water Resources
Monitor reservoirs, rivers, and wetlands
- SAR works through clouds for continuous monitoring
- Optical provides detailed water extent mapping

### 🌲 Environmental Monitoring
Track deforestation, urban growth, and land use change
- Multi-temporal analysis for change detection
- Multi-modal data for robust classification

### 🤖 Machine Learning
Create training datasets for deep learning models
- Paired multi-modal imagery
- Temporally consistent labels
- Large-scale dataset generation

### 🔥 Disaster Response
Rapid damage assessment and monitoring
- SAR penetrates clouds and smoke
- Optical provides detailed visual assessment

## 📖 Documentation

- **Microsoft Planetary Computer**: See [README_SENTINEL_DATASET_MPC.md](README_SENTINEL_DATASET_MPC.md)
- **Google Earth Engine**: See [SENTINEL_DATASET_README.md](SENTINEL_DATASET_README.md)
- **Examples**: Check `example_usage_mpc.py` and `example_usage.py`
- **Interactive**: Open the Jupyter notebooks for hands-on exploration

## 🔧 Example Workflows

### Workflow 1: Reservoir Monitoring

```python
# Define reservoir area
bbox = (-8.4, 37.7, -8.3, 37.8)

# Get multi-year dataset
s1, s2, pairs = create_dataset(
    bbox=bbox,
    start_date='2016-01-01',
    end_date='2024-12-31',
    cloud_percentage=5.0,
    max_time_diff_days=3
)

# Analyze temporal patterns
# Download images for detailed analysis
# Calculate water extent from both sensors
```

### Workflow 2: Seasonal Analysis

```python
# Compare different seasons
seasons = {
    'winter': ('2023-12-01', '2024-02-28'),
    'spring': ('2024-03-01', '2024-05-31'),
    'summer': ('2024-06-01', '2024-08-31'),
    'fall': ('2024-09-01', '2024-11-30')
}

for season_name, (start, end) in seasons.items():
    s1, s2, pairs = create_dataset(
        bbox=my_bbox,
        start_date=start,
        end_date=end,
        output_dir=f'./datasets/{season_name}'
    )
```

### Workflow 3: Training Data for ML

```python
# Create large dataset for model training
s1, s2, pairs = create_dataset(
    bbox=large_area_bbox,
    start_date='2020-01-01',
    end_date='2023-12-31',
    cloud_percentage=3.0,
    max_time_diff_days=1  # Strict temporal matching
)

# Download paired images
export_matched_pairs(
    matched_pairs=pairs,
    output_dir='./ml_training_data',
    s2_bands=['B04', 'B03', 'B02', 'B08'],  # RGB + NIR
    s1_bands=['vh', 'vv']
)
```

## 🌐 Data Sources

### Sentinel-1 (SAR)
- **Agency**: European Space Agency (ESA)
- **Launch**: 2014 (S1A), 2016 (S1B)
- **Resolution**: 10m
- **Revisit**: 6 days (both satellites)
- **Bands**: VV, VH (or HH, HV)

### Sentinel-2 (Optical)
- **Agency**: European Space Agency (ESA)
- **Launch**: 2015 (S2A), 2017 (S2B)
- **Resolution**: 10m (visible), 20m (NIR/SWIR)
- **Revisit**: 5 days (both satellites)
- **Bands**: 13 spectral bands

## 🤝 Contributing

This is part of the BLU Reservoir Monitoring Platform. Contributions are welcome!

## 📄 License

See main repository for license information.

## 🔗 Resources

- [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/)
- [Google Earth Engine](https://earthengine.google.com/)
- [Sentinel-1 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar)
- [Sentinel-2 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi)
- [Copernicus Open Access Hub](https://scihub.copernicus.eu/)

## ❓ FAQ

**Q: Which implementation should I use?**
A: Use Microsoft Planetary Computer for direct downloads and local analysis. Use Google Earth Engine for large-scale cloud processing.

**Q: How much storage do I need?**
A: Each image pair is typically 100-400 MB depending on area size and bands selected.

**Q: Can I use this commercially?**
A: Sentinel data is free and open. Check the Copernicus license terms for details.

**Q: What if I don't find enough matched pairs?**
A: Increase `cloud_percentage`, increase `max_time_diff_days`, or expand your date range.

**Q: Can I filter by other criteria?**
A: Yes! Modify the search functions to add custom filters for specific platforms, orbits, or quality metrics.

---

**Made with ❤️ for the remote sensing community**
