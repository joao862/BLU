# Installation Guide

## Quick Start

### Option 1: Use Without Installation (Easiest)

If you're in a Jupyter notebook or Python script in the same directory:

```python
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

# Now import works
from sentinel_dataset_mpc import create_dataset
```

### Option 2: Install Dependencies Only

Install just the required packages:

```bash
# For Microsoft Planetary Computer (recommended)
pip install planetary-computer pystac-client pandas rasterio shapely xarray matplotlib

# For Google Earth Engine
pip install earthengine-api geemap

# Or install all dependencies
pip install -r requirements.txt
```

### Option 3: Install as Package

Install the modules as a Python package:

```bash
# From the BLU directory
pip install -e .
```

This allows you to import from anywhere:

```python
from sentinel_dataset_mpc import create_dataset
```

## Verify Installation

Test if everything works:

```python
# Test Microsoft Planetary Computer version
from sentinel_dataset_mpc import create_dataset, get_sample_bbox

bbox = get_sample_bbox()
print(f"✓ Import successful! Sample bbox: {bbox}")
```

## Troubleshooting

### Import Error: No module named 'sentinel_dataset_mpc'

**Solution 1:** Add to Python path (recommended for notebooks)
```python
import sys
import os
sys.path.insert(0, os.getcwd())
```

**Solution 2:** Install as package
```bash
pip install -e .
```

**Solution 3:** Run from the same directory
```bash
cd /path/to/BLU
python your_script.py
```

### Import Error: No module named 'planetary_computer'

Install the missing dependency:
```bash
pip install planetary-computer pystac-client
```

### Import Error: No module named 'rasterio'

Rasterio requires GDAL. Install with:
```bash
# On Ubuntu/Debian
sudo apt-get install gdal-bin libgdal-dev

# Then install rasterio
pip install rasterio
```

Or use conda:
```bash
conda install -c conda-forge rasterio
```

## Running Examples

### Python Script

```bash
cd /path/to/BLU
python example_usage_mpc.py
```

### Jupyter Notebook

```bash
cd /path/to/BLU
jupyter notebook sentinel_dataset_mpc_notebook.ipynb
```

Make sure to run the first cell that adds the path!

## Development Installation

For development with auto-reload:

```bash
pip install -e ".[all]"
```

This installs all dependencies including optional ones for both MPC and GEE.

## Docker Installation (Alternative)

If you have issues with dependencies, use the dev container:

```bash
# Open in VS Code with Dev Containers extension
# Or build manually:
docker build -t sentinel-dataset .
docker run -it -v $(pwd):/workspace sentinel-dataset
```

## Testing Your Setup

Create a test file `test_setup.py`:

```python
#!/usr/bin/env python3
import sys

print("Testing imports...")

try:
    import pandas
    print("✓ pandas")
except ImportError:
    print("✗ pandas - run: pip install pandas")

try:
    import planetary_computer
    print("✓ planetary_computer")
except ImportError:
    print("✗ planetary_computer - run: pip install planetary-computer")

try:
    import pystac_client
    print("✓ pystac_client")
except ImportError:
    print("✗ pystac_client - run: pip install pystac-client")

try:
    from sentinel_dataset_mpc import create_dataset
    print("✓ sentinel_dataset_mpc")
except ImportError as e:
    print(f"✗ sentinel_dataset_mpc - {e}")
    print("  Solution: Run from BLU directory or add to path")

print("\nSetup test complete!")
```

Run it:
```bash
python test_setup.py
```

## Next Steps

Once installed, check out:
- `DATASET_CREATOR_README.md` - Main documentation
- `README_SENTINEL_DATASET_MPC.md` - MPC-specific docs
- `example_usage_mpc.py` - Usage examples
- `sentinel_dataset_mpc_notebook.ipynb` - Interactive tutorial
