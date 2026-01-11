# Quick Start - Portugal Reservoir Dataset

## ✅ What You Have

Your **Portugal Reservoir Dataset** is ready with 36 matched Sentinel-1/Sentinel-2 pairs!

```
📁 custom_roi_dataset/
  ├── roi.geojson (2.9 KB) - Your custom polygon ROI
  └── matched_pairs.json (16 KB) - All 36 matched pairs metadata

📄 create_portugal_reservoir_dataset.py - Ready-to-run script
📄 PORTUGAL_RESERVOIR_RESULTS.md - Detailed analysis
```

## 🚀 Quick Start (3 Steps)

### Step 1: Run on Your Machine

```bash
# Clone the repo
git clone <your-repo-url>
cd BLU

# Install dependencies
pip install planetary-computer pystac-client rasterio shapely pandas

# Run the script
python create_portugal_reservoir_dataset.py
```

### Step 2: Or Use Google Colab

```python
# 1. Upload files to Colab
# 2. Install dependencies
!pip install planetary-computer pystac-client rasterio shapely pandas

# 3. Run
!python create_portugal_reservoir_dataset.py
```

### Step 3: View the Data

```python
import json

# Load the matched pairs
with open('custom_roi_dataset/matched_pairs.json') as f:
    data = json.load(f)

print(f"Total pairs: {data['matched_pairs_count']}")
print(f"First pair: {data['matched_pairs'][0]}")
```

## 📊 Your Dataset at a Glance

| Metric | Value |
|--------|-------|
| **ROI Location** | Portugal (38.01°N, 7.94°W) |
| **ROI Size** | 1.08 × 1.49 km |
| **Time Period** | 2016-2024 (9 years) |
| **Matched Pairs** | 36 |
| **S1 Images** | 52 total |
| **S2 Images** | 45 (<5% clouds) |
| **Avg Cloud Cover** | 2.7% |
| **Avg Time Diff** | 2.2 days |

## 🎯 Sample Pairs

**Best Quality (lowest cloud coverage):**
- 2018-03-22: S1 descending ↔ S2 0.93% clouds (0.7 days apart)

**Best Alignment (closest in time):**
- 2017-12-15: S1 ascending ↔ S2 0.58% clouds (0.3 days apart)

**Most Recent:**
- 2024-11-01: S1 ascending ↔ S2 4.68% clouds (0.4 days apart)

## 💾 Download Images

Once connected to the internet:

```python
from sentinel_dataset_mpc import export_matched_pairs
import json

# Load matched pairs
with open('custom_roi_dataset/matched_pairs.json') as f:
    data = json.load(f)

# Download first 10 pairs
export_matched_pairs(
    matched_pairs=data['matched_pairs'][:10],
    output_dir='./images',
    s2_bands=['B04', 'B03', 'B02'],  # RGB
    s1_bands=['vh', 'vv']             # SAR
)
```

## 📈 Analysis Examples

### Water Extent Time Series

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load your matched pairs
df = pd.DataFrame(data['matched_pairs'])
df['date'] = pd.to_datetime(df['s2_date'])

# Plot temporal distribution
df.groupby(df['date'].dt.year).size().plot(kind='bar')
plt.title('Matched Pairs by Year')
plt.xlabel('Year')
plt.ylabel('Number of Pairs')
plt.show()
```

### Cloud Coverage Analysis

```python
# Analyze cloud coverage trends
plt.hist(df['s2_cloud_cover'], bins=20)
plt.title('Cloud Coverage Distribution')
plt.xlabel('Cloud Cover (%)')
plt.ylabel('Frequency')
plt.show()
```

## 🗺️ View ROI in QGIS

1. Open QGIS
2. Layer → Add Layer → Add Vector Layer
3. Select `custom_roi_dataset/roi.geojson`
4. Your Portugal reservoir polygon will appear!

## 📚 Documentation

- **Detailed Analysis**: `PORTUGAL_RESERVOIR_RESULTS.md`
- **Main Guide**: `DATASET_CREATOR_README.md`
- **Technical Docs**: `README_SENTINEL_DATASET_MPC.md`
- **Installation**: `INSTALL.md`

## ⚡ One-Liner

```bash
python create_portugal_reservoir_dataset.py
```

That's it! Run on any machine with internet access.

## 🎓 What You Can Do

✅ **Monitoring**: Track water levels 2016-2024
✅ **Analysis**: Seasonal patterns, drought detection
✅ **Research**: Multi-temporal change detection
✅ **ML Training**: 36 paired multi-modal samples
✅ **Publications**: High-quality dataset for papers

## ❓ Need Help?

Check these files in order:
1. `QUICK_START.md` (this file) - Start here
2. `PORTUGAL_RESERVOIR_RESULTS.md` - Your specific dataset
3. `DATASET_CREATOR_README.md` - Full documentation

## 🔗 GitHub

Branch: `claude/satellite-imagery-dataset-uO5et`

All code committed and ready to use!

---

**Ready to go!** 🚀 Just run the script when you have internet access.
