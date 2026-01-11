"""
Example Usage Script for Sentinel Dataset Creation
Using Microsoft Planetary Computer

This script demonstrates how to use the sentinel_dataset_mpc module
to create temporally-aligned Sentinel-1 and Sentinel-2 datasets.
"""

from sentinel_dataset_mpc import (
    create_dataset,
    export_matched_pairs,
    get_sample_bbox
)


def example_1_basic_usage():
    """Example 1: Basic dataset creation with default parameters"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80 + "\n")

    # Define a bounding box (min_lon, min_lat, max_lon, max_lat)
    # Example: San Francisco Bay Area
    bbox = (-122.5, 37.5, -122.0, 38.0)

    # Create dataset with default parameters
    s1_items, s2_items, matched_pairs = create_dataset(
        bbox=bbox,
        start_date='2023-01-01',
        end_date='2023-03-31',  # 3 months for quick testing
        cloud_percentage=5.0,
        max_time_diff_days=3
    )

    print(f"\nFound {len(matched_pairs)} matched pairs!")


def example_2_custom_bbox():
    """Example 2: Using a custom bounding box for a reservoir"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Custom Bounding Box - Reservoir Area")
    print("="*80 + "\n")

    # Define custom bbox for a reservoir area
    # Example: A reservoir in Portugal
    bbox = (-8.4, 37.7, -8.3, 37.8)

    # Create dataset
    s1_items, s2_items, matched_pairs = create_dataset(
        bbox=bbox,
        start_date='2020-01-01',
        end_date='2020-12-31',
        cloud_percentage=3.0,  # Very strict cloud filter
        max_time_diff_days=2,  # Require close temporal alignment
        output_dir='./reservoir_dataset_mpc'
    )


def example_3_with_orbit_filter():
    """Example 3: Filter Sentinel-1 by orbit direction"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Orbit Direction Filtering")
    print("="*80 + "\n")

    bbox = get_sample_bbox()

    # Create dataset with ascending orbit only
    s1_items, s2_items, matched_pairs = create_dataset(
        bbox=bbox,
        start_date='2023-01-01',
        end_date='2023-12-31',
        cloud_percentage=5.0,
        max_time_diff_days=3,
        orbit_direction='ascending',  # Only ascending passes
        output_dir='./sentinel_dataset_ascending_mpc'
    )


def example_4_download_images():
    """Example 4: Create dataset and download images locally"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Create and Download Dataset")
    print("="*80 + "\n")

    # Small bbox for faster download
    bbox = (-9.0, 38.5, -8.5, 39.0)

    # Create dataset
    s1_items, s2_items, matched_pairs = create_dataset(
        bbox=bbox,
        start_date='2023-06-01',
        end_date='2023-08-31',  # Summer months
        cloud_percentage=5.0,
        max_time_diff_days=3,
        output_dir='./summer_dataset_mpc'
    )

    # Download first 3 matched pairs to local storage
    if matched_pairs and len(matched_pairs) > 0:
        print("\nDownloading matched pairs...")
        export_matched_pairs(
            matched_pairs=matched_pairs[:3],  # Download first 3 pairs
            output_dir='./summer_dataset_mpc/images',
            s2_bands=['B04', 'B03', 'B02'],  # RGB bands
            s1_bands=['vh', 'vv']  # SAR polarizations
        )
        print("\nDownload complete!")
    else:
        print("\nNo matched pairs found to download.")


def example_5_multiple_years():
    """Example 5: Multi-year dataset creation"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Multi-Year Dataset (2020-2023)")
    print("="*80 + "\n")

    bbox = get_sample_bbox()

    # Create comprehensive multi-year dataset
    s1_items, s2_items, matched_pairs = create_dataset(
        bbox=bbox,
        start_date='2020-01-01',
        end_date='2023-12-31',
        cloud_percentage=5.0,
        max_time_diff_days=3,
        output_dir='./sentinel_dataset_multiyear_mpc'
    )

    # Print temporal distribution
    if matched_pairs:
        import pandas as pd

        df = pd.DataFrame(matched_pairs)
        df['s2_datetime'] = pd.to_datetime(df['s2_datetime'])
        df['year'] = df['s2_datetime'].dt.year

        print("\nTemporal Distribution by Year:")
        print(df['year'].value_counts().sort_index())

        print("\nTime Difference Statistics:")
        print(df['time_diff_days'].describe())


def example_6_point_based_roi():
    """Example 6: Create bbox from a point with buffer"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Point-based ROI with Buffer")
    print("="*80 + "\n")

    # Define a point location
    lon, lat = -122.4, 37.8  # San Francisco

    # Create a buffer around the point
    buffer_deg = 0.05  # approximately 5km
    bbox = (lon - buffer_deg, lat - buffer_deg,
            lon + buffer_deg, lat + buffer_deg)

    s1_items, s2_items, matched_pairs = create_dataset(
        bbox=bbox,
        start_date='2022-01-01',
        end_date='2022-12-31',
        cloud_percentage=5.0,
        max_time_diff_days=3,
        output_dir='./point_based_dataset_mpc'
    )


def example_7_large_area_sampling():
    """Example 7: Sample specific dates for large area"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Seasonal Sampling - Large Area")
    print("="*80 + "\n")

    # Larger bounding box
    bbox = (-123.0, 37.0, -121.5, 38.5)

    # Create dataset for specific seasons
    seasons = [
        ('2023-03-01', '2023-05-31', 'spring'),
        ('2023-06-01', '2023-08-31', 'summer'),
        ('2023-09-01', '2023-11-30', 'fall')
    ]

    all_pairs = []

    for start, end, season in seasons:
        print(f"\nProcessing {season}...")
        s1_items, s2_items, pairs = create_dataset(
            bbox=bbox,
            start_date=start,
            end_date=end,
            cloud_percentage=5.0,
            max_time_diff_days=3,
            output_dir=f'./seasonal_dataset_mpc/{season}'
        )
        all_pairs.extend(pairs)

    print(f"\nTotal matched pairs across all seasons: {len(all_pairs)}")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║       SENTINEL-1 & SENTINEL-2 DATASET CREATION EXAMPLES                   ║
    ║              Microsoft Planetary Computer Version                         ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)

    print("\nAvailable examples:")
    print("  1. Basic Usage")
    print("  2. Custom Bounding Box")
    print("  3. Orbit Direction Filtering")
    print("  4. Create and Download Dataset")
    print("  5. Multi-Year Dataset")
    print("  6. Point-based ROI with Buffer")
    print("  7. Seasonal Sampling - Large Area")

    # Uncomment the example you want to run:

    # example_1_basic_usage()
    # example_2_custom_bbox()
    # example_3_with_orbit_filter()
    # example_4_download_images()
    # example_5_multiple_years()
    # example_6_point_based_roi()
    # example_7_large_area_sampling()

    print("\nUncomment one of the example functions to run it!")
