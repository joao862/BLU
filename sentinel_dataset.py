"""
Sentinel-1 and Sentinel-2 Dataset Creation Module

This module provides functions to:
1. Acquire Sentinel-1 (SAR) and Sentinel-2 (optical) imagery
2. Filter images based on cloud coverage and temporal criteria
3. Create temporally-aligned multi-modal satellite datasets
"""

import ee
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import os
import json


def initialize_earth_engine():
    """Initialize Google Earth Engine API."""
    try:
        ee.Initialize()
        print("Earth Engine initialized successfully")
    except Exception as e:
        print(f"Error initializing Earth Engine: {e}")
        print("Attempting to authenticate...")
        ee.Authenticate()
        ee.Initialize()


def get_sentinel2_collection(roi: ee.Geometry,
                             start_date: str = '2016-01-01',
                             end_date: Optional[str] = None,
                             cloud_percentage: float = 5.0) -> ee.ImageCollection:
    """
    Get Sentinel-2 image collection filtered by ROI, date range, and cloud coverage.

    Args:
        roi: Region of Interest as ee.Geometry
        start_date: Start date in 'YYYY-MM-DD' format (default: '2016-01-01')
        end_date: End date in 'YYYY-MM-DD' format (default: today)
        cloud_percentage: Maximum cloud coverage percentage (default: 5.0)

    Returns:
        ee.ImageCollection: Filtered Sentinel-2 image collection
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_percentage))

    return collection


def get_sentinel1_collection(roi: ee.Geometry,
                             start_date: str = '2016-01-01',
                             end_date: Optional[str] = None,
                             instrument_mode: str = 'IW',
                             orbit: Optional[str] = None) -> ee.ImageCollection:
    """
    Get Sentinel-1 SAR image collection filtered by ROI and date range.

    Args:
        roi: Region of Interest as ee.Geometry
        start_date: Start date in 'YYYY-MM-DD' format (default: '2016-01-01')
        end_date: End date in 'YYYY-MM-DD' format (default: today)
        instrument_mode: Instrument mode (IW, EW, SM) (default: 'IW')
        orbit: Orbit direction ('ASCENDING' or 'DESCENDING') (default: None - both)

    Returns:
        ee.ImageCollection: Filtered Sentinel-1 image collection
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.eq('instrumentMode', instrument_mode))

    if orbit:
        collection = collection.filter(ee.Filter.eq('orbitProperties_pass', orbit))

    return collection


def get_image_dates(collection: ee.ImageCollection) -> List[Dict]:
    """
    Extract image dates and metadata from a collection.

    Args:
        collection: Earth Engine ImageCollection

    Returns:
        List of dictionaries containing image metadata
    """
    def extract_info(img):
        return ee.Feature(None, {
            'system_index': img.get('system:index'),
            'date': ee.Date(img.get('system:time_start')).format('YYYY-MM-dd'),
            'timestamp': img.get('system:time_start')
        })

    features = collection.map(extract_info)
    info_list = features.getInfo()['features']

    return [feat['properties'] for feat in info_list]


def match_temporal_pairs(s1_dates: List[Dict],
                        s2_dates: List[Dict],
                        max_time_diff_days: int = 3) -> List[Dict]:
    """
    Match Sentinel-1 and Sentinel-2 images that are within max_time_diff_days.

    Args:
        s1_dates: List of Sentinel-1 image metadata
        s2_dates: List of Sentinel-2 image metadata
        max_time_diff_days: Maximum time difference in days (default: 3)

    Returns:
        List of matched image pairs with metadata
    """
    matched_pairs = []

    # Convert to pandas DataFrames for easier manipulation
    s1_df = pd.DataFrame(s1_dates)
    s2_df = pd.DataFrame(s2_dates)

    if s1_df.empty or s2_df.empty:
        print("Warning: One or both collections are empty")
        return matched_pairs

    s1_df['datetime'] = pd.to_datetime(s1_df['date'])
    s2_df['datetime'] = pd.to_datetime(s2_df['date'])

    # Sort by date
    s1_df = s1_df.sort_values('datetime').reset_index(drop=True)
    s2_df = s2_df.sort_values('datetime').reset_index(drop=True)

    # For each Sentinel-2 image, find the closest Sentinel-1 image
    for idx, s2_row in s2_df.iterrows():
        s2_date = s2_row['datetime']

        # Calculate time differences
        s1_df['time_diff'] = abs((s1_df['datetime'] - s2_date).dt.total_seconds() / 86400)

        # Find images within the time threshold
        valid_matches = s1_df[s1_df['time_diff'] <= max_time_diff_days]

        if not valid_matches.empty:
            # Get the closest match
            closest_match = valid_matches.loc[valid_matches['time_diff'].idxmin()]

            matched_pairs.append({
                's1_index': closest_match['system_index'],
                's1_date': closest_match['date'],
                's1_timestamp': int(closest_match['timestamp']),
                's2_index': s2_row['system_index'],
                's2_date': s2_row['date'],
                's2_timestamp': int(s2_row['timestamp']),
                'time_diff_days': float(closest_match['time_diff'])
            })

    print(f"Found {len(matched_pairs)} matched pairs within {max_time_diff_days} days")
    return matched_pairs


def create_dataset(roi: ee.Geometry,
                  start_date: str = '2016-01-01',
                  end_date: Optional[str] = None,
                  cloud_percentage: float = 5.0,
                  max_time_diff_days: int = 3,
                  output_dir: str = './sentinel_dataset',
                  s1_orbit: Optional[str] = None) -> Tuple[ee.ImageCollection, ee.ImageCollection, List[Dict]]:
    """
    Create a temporally-aligned dataset of Sentinel-1 and Sentinel-2 images.

    Args:
        roi: Region of Interest as ee.Geometry
        start_date: Start date in 'YYYY-MM-DD' format (default: '2016-01-01')
        end_date: End date in 'YYYY-MM-DD' format (default: today)
        cloud_percentage: Maximum cloud coverage for Sentinel-2 (default: 5.0%)
        max_time_diff_days: Maximum time difference for pairing (default: 3 days)
        output_dir: Directory to save dataset metadata (default: './sentinel_dataset')
        s1_orbit: Sentinel-1 orbit direction ('ASCENDING'/'DESCENDING'/None)

    Returns:
        Tuple of (s1_collection, s2_collection, matched_pairs)
    """
    print("=" * 80)
    print("CREATING SENTINEL-1 & SENTINEL-2 TEMPORAL DATASET")
    print("=" * 80)
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date or 'today'}")
    print(f"Cloud Coverage Threshold: {cloud_percentage}%")
    print(f"Max Temporal Difference: {max_time_diff_days} days")
    print(f"Sentinel-1 Orbit: {s1_orbit or 'Both'}")
    print("-" * 80)

    # Get Sentinel-2 collection
    print("\n[1/4] Fetching Sentinel-2 images...")
    s2_collection = get_sentinel2_collection(roi, start_date, end_date, cloud_percentage)
    s2_count = s2_collection.size().getInfo()
    print(f"Found {s2_count} Sentinel-2 images with <{cloud_percentage}% cloud coverage")

    # Get Sentinel-1 collection
    print("\n[2/4] Fetching Sentinel-1 images...")
    s1_collection = get_sentinel1_collection(roi, start_date, end_date, orbit=s1_orbit)
    s1_count = s1_collection.size().getInfo()
    print(f"Found {s1_count} Sentinel-1 images")

    if s1_count == 0 or s2_count == 0:
        print("\nWarning: No images found in one or both collections!")
        return s1_collection, s2_collection, []

    # Extract dates
    print("\n[3/4] Extracting image dates...")
    s1_dates = get_image_dates(s1_collection)
    s2_dates = get_image_dates(s2_collection)
    print(f"Extracted {len(s1_dates)} S1 dates and {len(s2_dates)} S2 dates")

    # Match temporal pairs
    print(f"\n[4/4] Matching temporal pairs (max {max_time_diff_days} days apart)...")
    matched_pairs = match_temporal_pairs(s1_dates, s2_dates, max_time_diff_days)

    # Save metadata
    os.makedirs(output_dir, exist_ok=True)
    metadata_file = os.path.join(output_dir, 'matched_pairs.json')

    metadata = {
        'roi': roi.getInfo(),
        'start_date': start_date,
        'end_date': end_date or datetime.now().strftime('%Y-%m-%d'),
        'cloud_percentage_threshold': cloud_percentage,
        'max_time_diff_days': max_time_diff_days,
        's1_orbit': s1_orbit,
        'total_s1_images': s1_count,
        'total_s2_images': s2_count,
        'matched_pairs_count': len(matched_pairs),
        'matched_pairs': matched_pairs
    }

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'=' * 80}")
    print("DATASET SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total Sentinel-1 images: {s1_count}")
    print(f"Total Sentinel-2 images: {s2_count}")
    print(f"Matched pairs: {len(matched_pairs)}")
    print(f"\nMetadata saved to: {metadata_file}")
    print(f"{'=' * 80}\n")

    return s1_collection, s2_collection, matched_pairs


def export_matched_images(matched_pairs: List[Dict],
                         s1_collection: ee.ImageCollection,
                         s2_collection: ee.ImageCollection,
                         roi: ee.Geometry,
                         output_folder: str = 'sentinel_dataset',
                         scale: int = 10,
                         export_to: str = 'drive'):
    """
    Export matched image pairs to Google Drive or Cloud Storage.

    Args:
        matched_pairs: List of matched image pairs
        s1_collection: Sentinel-1 image collection
        s2_collection: Sentinel-2 image collection
        roi: Region of Interest
        output_folder: Output folder name (default: 'sentinel_dataset')
        scale: Export scale in meters (default: 10m for S2 resolution)
        export_to: Export destination ('drive' or 'cloud') (default: 'drive')
    """
    print(f"\n{'=' * 80}")
    print(f"EXPORTING {len(matched_pairs)} MATCHED IMAGE PAIRS")
    print(f"{'=' * 80}")
    print(f"Export destination: Google {export_to.upper()}")
    print(f"Resolution: {scale}m")
    print(f"Output folder: {output_folder}")
    print("-" * 80)

    tasks = []

    for i, pair in enumerate(matched_pairs):
        pair_name = f"pair_{i:04d}_diff_{pair['time_diff_days']:.2f}d"

        # Get Sentinel-1 image
        s1_img = s1_collection.filter(
            ee.Filter.eq('system:index', pair['s1_index'])
        ).first()

        # Get Sentinel-2 image
        s2_img = s2_collection.filter(
            ee.Filter.eq('system:index', pair['s2_index'])
        ).first()

        # Export Sentinel-1
        s1_export_name = f"{pair_name}_S1_{pair['s1_date']}"
        if export_to == 'drive':
            task_s1 = ee.batch.Export.image.toDrive(
                image=s1_img.clip(roi),
                description=s1_export_name,
                folder=output_folder,
                scale=scale,
                region=roi,
                maxPixels=1e13
            )
        else:
            task_s1 = ee.batch.Export.image.toCloudStorage(
                image=s1_img.clip(roi),
                description=s1_export_name,
                bucket=output_folder,
                scale=scale,
                region=roi,
                maxPixels=1e13
            )

        # Export Sentinel-2
        s2_export_name = f"{pair_name}_S2_{pair['s2_date']}"
        if export_to == 'drive':
            task_s2 = ee.batch.Export.image.toDrive(
                image=s2_img.clip(roi),
                description=s2_export_name,
                folder=output_folder,
                scale=scale,
                region=roi,
                maxPixels=1e13
            )
        else:
            task_s2 = ee.batch.Export.image.toCloudStorage(
                image=s2_img.clip(roi),
                description=s2_export_name,
                bucket=output_folder,
                scale=scale,
                region=roi,
                maxPixels=1e13
            )

        task_s1.start()
        task_s2.start()

        tasks.append({
            'pair': pair_name,
            's1_task': task_s1,
            's2_task': task_s2
        })

        print(f"[{i+1}/{len(matched_pairs)}] Submitted: {pair_name}")

    print(f"\n{'=' * 80}")
    print(f"All {len(matched_pairs)} pairs submitted for export!")
    print("Check your Google Drive or Cloud Storage for the exported images.")
    print(f"{'=' * 80}\n")

    return tasks


def get_sample_roi_geometry() -> ee.Geometry:
    """
    Get a sample ROI geometry for testing (San Francisco Bay Area).

    Returns:
        ee.Geometry: Sample region of interest
    """
    return ee.Geometry.Rectangle([-122.5, 37.5, -122.0, 38.0])


# Example usage
if __name__ == "__main__":
    # Initialize Earth Engine
    initialize_earth_engine()

    # Define ROI (example: rectangular area)
    # You can replace this with your own geometry
    roi = get_sample_roi_geometry()

    # Create dataset
    s1_collection, s2_collection, matched_pairs = create_dataset(
        roi=roi,
        start_date='2016-01-01',
        end_date='2024-12-31',
        cloud_percentage=5.0,
        max_time_diff_days=3,
        output_dir='./sentinel_dataset'
    )

    # Optional: Export the first 10 matched pairs
    if matched_pairs and len(matched_pairs) > 0:
        print("\nTo export images, uncomment the following lines:")
        print("# export_matched_images(")
        print("#     matched_pairs=matched_pairs[:10],  # First 10 pairs")
        print("#     s1_collection=s1_collection,")
        print("#     s2_collection=s2_collection,")
        print("#     roi=roi,")
        print("#     output_folder='sentinel_dataset',")
        print("#     scale=10")
        print("# )")
