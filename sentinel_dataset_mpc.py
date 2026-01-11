"""
Sentinel-1 and Sentinel-2 Dataset Creation Module using Microsoft Planetary Computer

This module provides functions to:
1. Acquire Sentinel-1 (SAR) and Sentinel-2 (optical) imagery from Microsoft Planetary Computer
2. Filter images based on cloud coverage and temporal criteria
3. Create temporally-aligned multi-modal satellite datasets
"""

import planetary_computer as pc
from pystac_client import Client
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import os
import json
from shapely.geometry import box, Point, Polygon, mapping
import warnings
warnings.filterwarnings('ignore')


def get_planetary_computer_client() -> Client:
    """
    Initialize Microsoft Planetary Computer STAC client.

    Returns:
        Client: STAC API client
    """
    catalog = Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=pc.sign_inplace
    )
    print("Microsoft Planetary Computer client initialized successfully")
    return catalog


def create_bbox_from_geometry(geometry: Dict) -> Tuple[float, float, float, float]:
    """
    Create bounding box from geometry dictionary.

    Args:
        geometry: Geometry dictionary with 'type' and 'coordinates'

    Returns:
        Tuple of (min_lon, min_lat, max_lon, max_lat)
    """
    if geometry['type'] == 'Point':
        lon, lat = geometry['coordinates']
        buffer = 0.1  # ~11km buffer
        return (lon - buffer, lat - buffer, lon + buffer, lat + buffer)

    elif geometry['type'] == 'Polygon':
        coords = geometry['coordinates'][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        return (min(lons), min(lats), max(lons), max(lats))

    elif geometry['type'] == 'bbox':
        return tuple(geometry['coordinates'])

    else:
        raise ValueError(f"Unsupported geometry type: {geometry['type']}")


def search_sentinel2(catalog: Client,
                     bbox: Tuple[float, float, float, float],
                     start_date: str = '2016-01-01',
                     end_date: Optional[str] = None,
                     cloud_percentage: float = 5.0) -> List[Dict]:
    """
    Search Sentinel-2 imagery using Microsoft Planetary Computer.

    Args:
        catalog: STAC client
        bbox: Bounding box (min_lon, min_lat, max_lon, max_lat)
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (default: today)
        cloud_percentage: Maximum cloud coverage percentage (default: 5.0)

    Returns:
        List of Sentinel-2 items with metadata
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    print(f"\nSearching Sentinel-2 imagery...")
    print(f"  Date range: {start_date} to {end_date}")
    print(f"  Cloud coverage: <{cloud_percentage}%")

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{start_date}/{end_date}",
        query={
            "eo:cloud_cover": {"lt": cloud_percentage}
        }
    )

    items = list(search.items())
    print(f"  Found {len(items)} Sentinel-2 scenes")

    return [
        {
            'id': item.id,
            'datetime': item.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'date': item.datetime.strftime('%Y-%m-%d'),
            'timestamp': int(item.datetime.timestamp() * 1000),
            'cloud_cover': item.properties.get('eo:cloud_cover', 0),
            'item': item
        }
        for item in items
    ]


def search_sentinel1(catalog: Client,
                     bbox: Tuple[float, float, float, float],
                     start_date: str = '2016-01-01',
                     end_date: Optional[str] = None,
                     orbit_direction: Optional[str] = None) -> List[Dict]:
    """
    Search Sentinel-1 SAR imagery using Microsoft Planetary Computer.

    Args:
        catalog: STAC client
        bbox: Bounding box (min_lon, min_lat, max_lon, max_lat)
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (default: today)
        orbit_direction: Orbit direction ('ascending' or 'descending') (default: None - both)

    Returns:
        List of Sentinel-1 items with metadata
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    print(f"\nSearching Sentinel-1 imagery...")
    print(f"  Date range: {start_date} to {end_date}")
    print(f"  Orbit direction: {orbit_direction or 'Both'}")

    query_params = {}
    if orbit_direction:
        query_params["sat:orbit_state"] = {"eq": orbit_direction.lower()}

    search = catalog.search(
        collections=["sentinel-1-rtc"],
        bbox=bbox,
        datetime=f"{start_date}/{end_date}",
        query=query_params if query_params else None
    )

    items = list(search.items())
    print(f"  Found {len(items)} Sentinel-1 scenes")

    return [
        {
            'id': item.id,
            'datetime': item.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'date': item.datetime.strftime('%Y-%m-%d'),
            'timestamp': int(item.datetime.timestamp() * 1000),
            'orbit_direction': item.properties.get('sat:orbit_state', 'unknown'),
            'item': item
        }
        for item in items
    ]


def match_temporal_pairs(s1_items: List[Dict],
                        s2_items: List[Dict],
                        max_time_diff_days: int = 3) -> List[Dict]:
    """
    Match Sentinel-1 and Sentinel-2 images that are within max_time_diff_days.

    Args:
        s1_items: List of Sentinel-1 item metadata
        s2_items: List of Sentinel-2 item metadata
        max_time_diff_days: Maximum time difference in days (default: 3)

    Returns:
        List of matched image pairs with metadata
    """
    if not s1_items or not s2_items:
        print("Warning: One or both collections are empty")
        return []

    print(f"\nMatching temporal pairs (max {max_time_diff_days} days apart)...")

    # Convert to pandas DataFrames
    s1_df = pd.DataFrame(s1_items)
    s2_df = pd.DataFrame(s2_items)

    s1_df['datetime_obj'] = pd.to_datetime(s1_df['datetime'])
    s2_df['datetime_obj'] = pd.to_datetime(s2_df['datetime'])

    # Sort by datetime
    s1_df = s1_df.sort_values('datetime_obj').reset_index(drop=True)
    s2_df = s2_df.sort_values('datetime_obj').reset_index(drop=True)

    matched_pairs = []

    # For each Sentinel-2 image, find the closest Sentinel-1 image
    for idx, s2_row in s2_df.iterrows():
        s2_time = s2_row['datetime_obj']

        # Calculate time differences in days
        s1_df['time_diff'] = abs((s1_df['datetime_obj'] - s2_time).dt.total_seconds() / 86400)

        # Find images within the time threshold
        valid_matches = s1_df[s1_df['time_diff'] <= max_time_diff_days]

        if not valid_matches.empty:
            # Get the closest match
            closest_match = valid_matches.loc[valid_matches['time_diff'].idxmin()]

            matched_pairs.append({
                's1_id': closest_match['id'],
                's1_date': closest_match['date'],
                's1_datetime': closest_match['datetime'],
                's1_timestamp': int(closest_match['timestamp']),
                's1_orbit': closest_match['orbit_direction'],
                's1_item': closest_match['item'],
                's2_id': s2_row['id'],
                's2_date': s2_row['date'],
                's2_datetime': s2_row['datetime'],
                's2_timestamp': int(s2_row['timestamp']),
                's2_cloud_cover': float(s2_row['cloud_cover']),
                's2_item': s2_row['item'],
                'time_diff_days': float(closest_match['time_diff'])
            })

    print(f"  Found {len(matched_pairs)} matched pairs")
    return matched_pairs


def create_dataset(bbox: Tuple[float, float, float, float],
                  start_date: str = '2016-01-01',
                  end_date: Optional[str] = None,
                  cloud_percentage: float = 5.0,
                  max_time_diff_days: int = 3,
                  output_dir: str = './sentinel_dataset_mpc',
                  orbit_direction: Optional[str] = None) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Create a temporally-aligned dataset of Sentinel-1 and Sentinel-2 images
    using Microsoft Planetary Computer.

    Args:
        bbox: Bounding box (min_lon, min_lat, max_lon, max_lat)
        start_date: Start date in 'YYYY-MM-DD' format (default: '2016-01-01')
        end_date: End date in 'YYYY-MM-DD' format (default: today)
        cloud_percentage: Maximum cloud coverage for Sentinel-2 (default: 5.0%)
        max_time_diff_days: Maximum time difference for pairing (default: 3 days)
        output_dir: Directory to save dataset metadata (default: './sentinel_dataset_mpc')
        orbit_direction: Sentinel-1 orbit ('ascending'/'descending'/None)

    Returns:
        Tuple of (s1_items, s2_items, matched_pairs)
    """
    print("=" * 80)
    print("CREATING SENTINEL-1 & SENTINEL-2 TEMPORAL DATASET")
    print("Using Microsoft Planetary Computer")
    print("=" * 80)
    print(f"Bounding Box: {bbox}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date or 'today'}")
    print(f"Cloud Coverage Threshold: {cloud_percentage}%")
    print(f"Max Temporal Difference: {max_time_diff_days} days")
    print(f"Sentinel-1 Orbit: {orbit_direction or 'Both'}")
    print("-" * 80)

    # Initialize catalog
    catalog = get_planetary_computer_client()

    # Search Sentinel-2
    s2_items = search_sentinel2(
        catalog, bbox, start_date, end_date, cloud_percentage
    )

    # Search Sentinel-1
    s1_items = search_sentinel1(
        catalog, bbox, start_date, end_date, orbit_direction
    )

    if not s1_items or not s2_items:
        print("\nWarning: No images found in one or both collections!")
        return s1_items, s2_items, []

    # Match temporal pairs
    matched_pairs = match_temporal_pairs(s1_items, s2_items, max_time_diff_days)

    # Save metadata
    os.makedirs(output_dir, exist_ok=True)
    metadata_file = os.path.join(output_dir, 'matched_pairs.json')

    # Prepare metadata (without STAC item objects)
    pairs_metadata = []
    for pair in matched_pairs:
        pairs_metadata.append({
            's1_id': pair['s1_id'],
            's1_date': pair['s1_date'],
            's1_datetime': pair['s1_datetime'],
            's1_timestamp': pair['s1_timestamp'],
            's1_orbit': pair['s1_orbit'],
            's2_id': pair['s2_id'],
            's2_date': pair['s2_date'],
            's2_datetime': pair['s2_datetime'],
            's2_timestamp': pair['s2_timestamp'],
            's2_cloud_cover': pair['s2_cloud_cover'],
            'time_diff_days': pair['time_diff_days']
        })

    metadata = {
        'source': 'Microsoft Planetary Computer',
        'bbox': bbox,
        'start_date': start_date,
        'end_date': end_date or datetime.now().strftime('%Y-%m-%d'),
        'cloud_percentage_threshold': cloud_percentage,
        'max_time_diff_days': max_time_diff_days,
        'orbit_direction': orbit_direction,
        'total_s1_images': len(s1_items),
        'total_s2_images': len(s2_items),
        'matched_pairs_count': len(matched_pairs),
        'matched_pairs': pairs_metadata
    }

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'=' * 80}")
    print("DATASET SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total Sentinel-1 images: {len(s1_items)}")
    print(f"Total Sentinel-2 images: {len(s2_items)}")
    print(f"Matched pairs: {len(matched_pairs)}")
    print(f"\nMetadata saved to: {metadata_file}")
    print(f"{'=' * 80}\n")

    return s1_items, s2_items, matched_pairs


def download_image(item, output_path: str, bands: Optional[List[str]] = None):
    """
    Download a single STAC item to local storage.

    Args:
        item: STAC Item object
        output_path: Path to save the downloaded file
        bands: List of bands to download (default: all available)
    """
    import rasterio
    from rasterio.merge import merge
    import numpy as np

    print(f"Downloading {item.id}...")

    if bands is None:
        # Get all asset keys except metadata
        bands = [key for key in item.assets.keys()
                if key not in ['thumbnail', 'metadata', 'info']]

    # Download and merge bands if multiple
    datasets = []
    for band in bands[:3]:  # Limit to first 3 bands for example
        if band in item.assets:
            href = item.assets[band].href
            datasets.append(rasterio.open(href))

    if datasets:
        mosaic, out_trans = merge(datasets)

        out_meta = datasets[0].meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
            "count": mosaic.shape[0]
        })

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(mosaic)

        for dataset in datasets:
            dataset.close()

        print(f"  Saved to: {output_path}")


def export_matched_pairs(matched_pairs: List[Dict],
                        output_dir: str = './sentinel_dataset_mpc/images',
                        max_pairs: Optional[int] = None,
                        s2_bands: Optional[List[str]] = None,
                        s1_bands: Optional[List[str]] = None):
    """
    Download matched image pairs to local storage.

    Args:
        matched_pairs: List of matched pairs from create_dataset()
        output_dir: Output directory for downloaded images
        max_pairs: Maximum number of pairs to download (default: all)
        s2_bands: Sentinel-2 bands to download (default: ['B04', 'B03', 'B02'])
        s1_bands: Sentinel-1 bands to download (default: ['vh', 'vv'])
    """
    if s2_bands is None:
        s2_bands = ['B04', 'B03', 'B02']  # RGB
    if s1_bands is None:
        s1_bands = ['vh', 'vv']

    pairs_to_download = matched_pairs[:max_pairs] if max_pairs else matched_pairs

    print(f"\n{'=' * 80}")
    print(f"DOWNLOADING {len(pairs_to_download)} MATCHED IMAGE PAIRS")
    print(f"{'=' * 80}")
    print(f"Output directory: {output_dir}")
    print(f"Sentinel-2 bands: {s2_bands}")
    print(f"Sentinel-1 bands: {s1_bands}")
    print("-" * 80)

    os.makedirs(output_dir, exist_ok=True)

    for i, pair in enumerate(pairs_to_download):
        pair_name = f"pair_{i:04d}_diff_{pair['time_diff_days']:.2f}d"

        print(f"\n[{i+1}/{len(pairs_to_download)}] Processing {pair_name}")

        # Download Sentinel-1
        s1_output = os.path.join(output_dir, f"{pair_name}_S1_{pair['s1_date']}.tif")
        try:
            download_image(pair['s1_item'], s1_output, s1_bands)
        except Exception as e:
            print(f"  Error downloading S1: {e}")

        # Download Sentinel-2
        s2_output = os.path.join(output_dir, f"{pair_name}_S2_{pair['s2_date']}.tif")
        try:
            download_image(pair['s2_item'], s2_output, s2_bands)
        except Exception as e:
            print(f"  Error downloading S2: {e}")

    print(f"\n{'=' * 80}")
    print(f"Download complete! Images saved to: {output_dir}")
    print(f"{'=' * 80}\n")


def get_sample_bbox() -> Tuple[float, float, float, float]:
    """
    Get a sample bounding box for testing (San Francisco Bay Area).

    Returns:
        Tuple: (min_lon, min_lat, max_lon, max_lat)
    """
    return (-122.5, 37.5, -122.0, 38.0)


# Example usage
if __name__ == "__main__":
    # Define bounding box (example: San Francisco Bay Area)
    bbox = get_sample_bbox()

    # Create dataset
    s1_items, s2_items, matched_pairs = create_dataset(
        bbox=bbox,
        start_date='2023-01-01',
        end_date='2023-03-31',  # 3 months for testing
        cloud_percentage=5.0,
        max_time_diff_days=3,
        output_dir='./sentinel_dataset_mpc'
    )

    # Optional: Download first 5 matched pairs
    if matched_pairs:
        print("\nTo download images, uncomment the following lines:")
        print("# export_matched_pairs(")
        print("#     matched_pairs=matched_pairs[:5],")
        print("#     output_dir='./sentinel_dataset_mpc/images'")
        print("# )")
