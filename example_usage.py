"""
Example Usage Script for Sentinel Dataset Creation

This script demonstrates how to use the sentinel_dataset module
to create temporally-aligned Sentinel-1 and Sentinel-2 datasets.
"""

import ee
from sentinel_dataset import (
    initialize_earth_engine,
    create_dataset,
    export_matched_images,
    get_sample_roi_geometry
)


def example_1_basic_usage():
    """Example 1: Basic dataset creation with default parameters"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80 + "\n")

    # Initialize Earth Engine
    initialize_earth_engine()

    # Define a simple rectangular ROI
    # Example: San Francisco Bay Area
    roi = ee.Geometry.Rectangle([-122.5, 37.5, -122.0, 38.0])

    # Create dataset with default parameters
    s1_collection, s2_collection, matched_pairs = create_dataset(
        roi=roi,
        start_date='2016-01-01',
        end_date='2016-06-30',  # 6 months for quick testing
        cloud_percentage=5.0,
        max_time_diff_days=3
    )

    print(f"\nFound {len(matched_pairs)} matched pairs!")


def example_2_custom_roi():
    """Example 2: Using a custom ROI from coordinates"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Custom ROI - Reservoir Area")
    print("="*80 + "\n")

    initialize_earth_engine()

    # Define custom ROI (example: a reservoir)
    # You can use ee.Geometry.Point, Polygon, Rectangle, etc.
    roi = ee.Geometry.Polygon([
        [
            [-8.4, 37.8],  # Top-left
            [-8.4, 37.7],  # Bottom-left
            [-8.3, 37.7],  # Bottom-right
            [-8.3, 37.8]   # Top-right
        ]
    ])

    # Create dataset
    s1_collection, s2_collection, matched_pairs = create_dataset(
        roi=roi,
        start_date='2020-01-01',
        end_date='2020-12-31',
        cloud_percentage=3.0,  # Very strict cloud filter
        max_time_diff_days=2,  # Require close temporal alignment
        output_dir='./reservoir_dataset'
    )


def example_3_with_orbit_filter():
    """Example 3: Filter Sentinel-1 by orbit direction"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Orbit Direction Filtering")
    print("="*80 + "\n")

    initialize_earth_engine()

    roi = get_sample_roi_geometry()

    # Create dataset with ascending orbit only
    s1_collection, s2_collection, matched_pairs = create_dataset(
        roi=roi,
        start_date='2019-01-01',
        end_date='2019-12-31',
        cloud_percentage=5.0,
        max_time_diff_days=3,
        s1_orbit='ASCENDING',  # Only ascending passes
        output_dir='./sentinel_dataset_ascending'
    )


def example_4_export_images():
    """Example 4: Create dataset and export images"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Create and Export Dataset")
    print("="*80 + "\n")

    initialize_earth_engine()

    roi = ee.Geometry.Rectangle([-9.0, 38.5, -8.5, 39.0])

    # Create dataset
    s1_collection, s2_collection, matched_pairs = create_dataset(
        roi=roi,
        start_date='2023-06-01',
        end_date='2023-08-31',  # Summer months
        cloud_percentage=5.0,
        max_time_diff_days=3,
        output_dir='./summer_dataset'
    )

    # Export first 5 matched pairs to Google Drive
    if matched_pairs and len(matched_pairs) > 0:
        print("\nExporting matched pairs to Google Drive...")
        export_matched_images(
            matched_pairs=matched_pairs[:5],  # Export first 5 pairs
            s1_collection=s1_collection,
            s2_collection=s2_collection,
            roi=roi,
            output_folder='Sentinel_Dataset_Summer_2023',
            scale=10,  # 10m resolution
            export_to='drive'
        )
        print("\nCheck your Google Drive for exported images!")
    else:
        print("\nNo matched pairs found to export.")


def example_5_multiple_years():
    """Example 5: Multi-year dataset creation"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Multi-Year Dataset (2016-2024)")
    print("="*80 + "\n")

    initialize_earth_engine()

    roi = get_sample_roi_geometry()

    # Create comprehensive multi-year dataset
    s1_collection, s2_collection, matched_pairs = create_dataset(
        roi=roi,
        start_date='2016-01-01',
        end_date='2024-12-31',
        cloud_percentage=5.0,
        max_time_diff_days=3,
        output_dir='./sentinel_dataset_multiyear'
    )

    # Print temporal distribution
    if matched_pairs:
        import pandas as pd

        df = pd.DataFrame(matched_pairs)
        df['s2_date'] = pd.to_datetime(df['s2_date'])
        df['year'] = df['s2_date'].dt.year

        print("\nTemporal Distribution by Year:")
        print(df['year'].value_counts().sort_index())

        print("\nTime Difference Statistics:")
        print(df['time_diff_days'].describe())


def example_6_point_based_roi():
    """Example 6: Create ROI from a point with buffer"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Point-based ROI with Buffer")
    print("="*80 + "\n")

    initialize_earth_engine()

    # Define a point location
    point = ee.Geometry.Point([-122.4, 37.8])  # San Francisco

    # Create a buffer around the point (10km radius)
    roi = point.buffer(10000)  # 10,000 meters = 10 km

    s1_collection, s2_collection, matched_pairs = create_dataset(
        roi=roi,
        start_date='2022-01-01',
        end_date='2022-12-31',
        cloud_percentage=5.0,
        max_time_diff_days=3,
        output_dir='./point_based_dataset'
    )


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║          SENTINEL-1 & SENTINEL-2 DATASET CREATION EXAMPLES                ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)

    print("\nAvailable examples:")
    print("  1. Basic Usage")
    print("  2. Custom ROI")
    print("  3. Orbit Direction Filtering")
    print("  4. Create and Export Dataset")
    print("  5. Multi-Year Dataset")
    print("  6. Point-based ROI with Buffer")

    # Uncomment the example you want to run:

    # example_1_basic_usage()
    # example_2_custom_roi()
    # example_3_with_orbit_filter()
    # example_4_export_images()
    # example_5_multiple_years()
    # example_6_point_based_roi()

    print("\nUncomment one of the example functions to run it!")
