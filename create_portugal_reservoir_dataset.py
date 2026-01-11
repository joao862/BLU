"""
Custom ROI Dataset Creator - Portugal Reservoir
This script creates a Sentinel-1 & Sentinel-2 dataset for your specific ROI.
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sentinel_dataset_mpc import create_dataset

# Your custom ROI (Portugal reservoir)
roi_geojson = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-7.937365, 38.022977], [-7.937064, 38.021946], [-7.937, 38.020559],
                [-7.936227, 38.01897], [-7.935197, 38.018227], [-7.933974, 38.017483],
                [-7.935734, 38.016587], [-7.936013, 38.015606], [-7.936013, 38.014947],
                [-7.935026, 38.014491], [-7.934511, 38.014], [-7.935326, 38.012513],
                [-7.935777, 38.011633], [-7.936141, 38.010687], [-7.936893, 38.009875],
                [-7.939661, 38.009655], [-7.941999, 38.01018], [-7.943716, 38.01116],
                [-7.943716, 38.0128], [-7.942901, 38.012783], [-7.941914, 38.012783],
                [-7.941334, 38.012614], [-7.940412, 38.013544], [-7.94024, 38.014626],
                [-7.93906, 38.015353], [-7.938995, 38.016283], [-7.942042, 38.017635],
                [-7.941356, 38.017838], [-7.940519, 38.01777], [-7.939296, 38.017348],
                [-7.938159, 38.018734], [-7.938673, 38.020238], [-7.938867, 38.02176],
                [-7.93803, 38.023044], [-7.937365, 38.022977]
            ]]
        }
    }]
}


def get_bbox_from_geojson(geojson):
    """Extract bounding box from GeoJSON polygon."""
    coordinates = geojson['features'][0]['geometry']['coordinates'][0]
    lons = [coord[0] for coord in coordinates]
    lats = [coord[1] for coord in coordinates]
    return (min(lons), min(lats), max(lons), max(lats))


def main():
    """Create dataset for the Portugal reservoir ROI."""
    print("="*80)
    print("CREATING SENTINEL-1 & SENTINEL-2 DATASET")
    print("Custom ROI: Portugal Reservoir")
    print("="*80)

    # Extract bounding box
    bbox = get_bbox_from_geojson(roi_geojson)

    print(f"\nROI Details:")
    print(f"  Location: Portugal")
    print(f"  Polygon vertices: {len(roi_geojson['features'][0]['geometry']['coordinates'][0])}")
    print(f"  Bounding box: {bbox}")
    print(f"  Area: ~1.08 km × 1.49 km")

    # Save ROI
    output_dir = './portugal_reservoir_dataset'
    os.makedirs(output_dir, exist_ok=True)

    roi_file = os.path.join(output_dir, 'roi.geojson')
    with open(roi_file, 'w') as f:
        json.dump(roi_geojson, f, indent=2)
    print(f"\n✓ ROI saved to: {roi_file}")

    # Configuration
    config = {
        'start_date': '2016-01-01',
        'end_date': '2024-12-31',
        'cloud_percentage': 5.0,
        'max_time_diff_days': 3,
        'orbit_direction': None  # Both ascending and descending
    }

    print(f"\nDataset Configuration:")
    print(f"  Start date: {config['start_date']}")
    print(f"  End date: {config['end_date']}")
    print(f"  Cloud coverage threshold: {config['cloud_percentage']}%")
    print(f"  Max temporal difference: {config['max_time_diff_days']} days")
    print(f"  Orbit filter: {config['orbit_direction'] or 'Both'}")

    print(f"\n{'='*80}")
    print("FETCHING SATELLITE DATA...")
    print(f"{'='*80}\n")

    try:
        # Create dataset
        s1_items, s2_items, matched_pairs = create_dataset(
            bbox=bbox,
            start_date=config['start_date'],
            end_date=config['end_date'],
            cloud_percentage=config['cloud_percentage'],
            max_time_diff_days=config['max_time_diff_days'],
            output_dir=output_dir,
            orbit_direction=config['orbit_direction']
        )

        print(f"\n{'='*80}")
        print("SUCCESS!")
        print(f"{'='*80}")
        print(f"\n✓ Dataset created successfully!")
        print(f"✓ Total matched pairs: {len(matched_pairs)}")
        print(f"✓ Output directory: {output_dir}")

        if matched_pairs:
            print(f"\nSample of first 5 matched pairs:")
            for i, pair in enumerate(matched_pairs[:5], 1):
                print(f"\n  Pair {i}:")
                print(f"    S1: {pair['s1_date']} ({pair['s1_orbit']})")
                print(f"    S2: {pair['s2_date']} (cloud: {pair['s2_cloud_cover']:.2f}%)")
                print(f"    Time diff: {pair['time_diff_days']:.2f} days")

            print(f"\n✓ Full metadata saved to: {output_dir}/matched_pairs.json")

            # Option to download images
            print(f"\n{'='*80}")
            print("NEXT STEPS")
            print(f"{'='*80}")
            print("\nTo download the actual satellite images, uncomment and run:")
            print("""
from sentinel_dataset_mpc import export_matched_pairs

export_matched_pairs(
    matched_pairs=matched_pairs[:10],  # Download first 10 pairs
    output_dir='./portugal_reservoir_dataset/images',
    s2_bands=['B04', 'B03', 'B02'],  # RGB
    s1_bands=['vh', 'vv']             # SAR polarizations
)
            """)

        return matched_pairs

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\nIf you see a network error, make sure you have:")
        print("  1. Internet access to Microsoft Planetary Computer")
        print("  2. All dependencies installed: pip install -r requirements.txt")
        raise


if __name__ == "__main__":
    matched_pairs = main()
