"""
Setup script for Sentinel Dataset Creator
"""
from setuptools import setup, find_packages

with open("DATASET_CREATOR_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sentinel-dataset-creator",
    version="1.0.0",
    author="BLU Team",
    description="Create temporally-aligned Sentinel-1 and Sentinel-2 datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[
        "sentinel_dataset",
        "sentinel_dataset_mpc",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.20.0",
        # MPC dependencies (optional)
        "planetary-computer",
        "pystac-client",
        "shapely>=2.0.0",
        "xarray",
        "rasterio>=1.3.0",
        # GEE dependencies (optional)
        "earthengine-api>=0.1.0",
    ],
    extras_require={
        "mpc": [
            "planetary-computer",
            "pystac-client",
            "shapely>=2.0.0",
            "xarray",
            "rasterio>=1.3.0",
        ],
        "gee": [
            "earthengine-api>=0.1.0",
            "geemap>=0.19.0",
        ],
        "all": [
            "planetary-computer",
            "pystac-client",
            "shapely>=2.0.0",
            "xarray",
            "rasterio>=1.3.0",
            "earthengine-api>=0.1.0",
            "geemap>=0.19.0",
            "matplotlib>=3.0.0",
            "jupyter",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
