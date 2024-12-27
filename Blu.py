#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:38:58 2024

@author: joaopimenta
"""

import os
import streamlit as st
import geemap.foliumap as geemap
import ee
import geopandas as gpd
import tempfile
import uuid
import fiona
from datetime import datetime
import base64
import rasterio
from rasterio.plot import show
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import pyproj
from shapely.geometry import Polygon
from rasterio.features import shapes
import pandas as pd
from skimage import measure
from shapely.geometry import Polygon, box,  MultiPolygon
import matplotlib.pyplot as plt
import requests
from io import StringIO
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Set page configuration
st.set_page_config(layout="wide")


# Define the custom CSS style for the title and subtitle
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap');

    .title-custom-style {
        font-family: 'SpaceGrotesk-Light';
        font-size: 64px;
        font-weight: 500;
        color: #fff;
        margin-bottom: 25px;
        margin-top: 125px;
        margin-left: 280px;
        text-shadow: 2px 2px 4px rgba(1, 1, 1, 1);
    }

    .subtitle-custom-style {
        font-family: 'SpaceGrotesk-Medium';
        max-width: 620px;
        margin-left: 280px;
        font-weight: 20;
        text-transform: uppercase;
        color: #fff;
        font-size: 15px;
    }
</style>
"""

import streamlit as st
import time
from streamlit_navigation_bar import st_navbar

pages = ["Home", "About", "Tutorial", "Worldwide Analysis", "Portugal Analysis"]

styles = {
    "nav": {
        "background-color": "rgba(0, 0, 0, 0.5)",
        # Add 50% transparency
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.26rem",
        "color": "rgb(255    ,255,    255)",
        "margin": "0 0.225rem",
        "padding": "0.375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(0    ,0,    200, 0.95)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.95)",
    },
}

page = st_navbar(pages, styles=styles)
page = st.sidebar.selectbox("",pages)
# Apply the custom CSS style and HTML title using Markdown
st.markdown(f"{custom_css}<h1 class='title-custom-style'>Real-Time Reservoir Monitoring Platform</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle-custom-style'>This software allows you to monitorize the volume storage of almost any water body at your choice. It is still in beta version.</h2>", unsafe_allow_html=True)

# Function to process uploaded GeoJSON or KML file and return a GeoDataFrame
def process_uploaded_file(data):
    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.read())  # Use data.read() to write file content

    if file_extension.lower() == ".kml":
        fiona.drvsupport.supported_drivers["KML"] = "rw"
        gdf = gpd.read_file(file_path, driver="KML")
    elif file_extension.lower() in [".geojson", ".json"]:
        gdf = gpd.read_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    return gdf

import streamlit as st

# Sidebar customization
st.sidebar.title("About")

st.sidebar.markdown(
    """
    This Beta version allows you to visualize the volume storage, water surface elevation and other infor of the majority of reservoirs and lakes worlddwide, in real time using remote sensing,
    created by João Pimenta
    """
)
# Create unique keys for each st.radio widget
world_key = "Worldwide anaysis"
if page == 'Home':
    import streamlit as st
    import requests
    import base64

# Video URL (ensure it's accessible)
    video_url = "https://raw.githubusercontent.com/joao862/BLU/main/1851190-uhd_3840_2160_25fps.mp4"

# Fetch the video from the URL
    response = requests.get(video_url)

# Check if the request was successful
    if response.status_code == 200:
        video_bytes = response.content
    
    # Convert the video bytes to Base64
        video_base64 = base64.b64encode(video_bytes).decode("utf-8")
    
    # Set the background video using CSS
        st.markdown(
           f"""
           <style>
           .stApp {{
               background-image: url('data:video/mp4;base64,{video_base64}');
               background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Failed to load video. Please check the URL or your internet connection.")
	    
elif page == "Worldwide Analysis":
    st.title("Worldwide Analysis")
    import toml
    import json
    import json
    import streamlit as st
    # Recupera configuração de secrets
    firebase_settings = st.secrets["firebase"]["my_project_settings"]
    # Corrigir o formato do JSON substituindo "=" por ":"
    config_str = config_str.replace("=", ":")
    st.write("What the hell is wrong here?")
    st.write(config_str)
# Tente converter para JSON
    try:
        firebase_settings_json = json.loads(config_str)
        st.write("Firebase Config:", firebase_settings_json)
    except json.JSONDecodeError as e:
        st.error(f"Erro ao decodificar JSON: {e}")
    # File uploader for GeoJSON or KML
    uploaded_file = st.file_uploader("Upload a GeoJSON or KML File")

    HydroLakes = ee.FeatureCollection('projects/ee-joaopedromateusp/assets/HydroLAKES')
    # List of feature collections
    datasets = [
        ee.FeatureCollection('projects/ee-joaopedromateusp/assets/SWOT_files/SWOT_EU_21'),
        ee.FeatureCollection('projects/ee-joaopedromateusp/assets/SWOT_files/SWOT_EU_22'),
        ee.FeatureCollection('projects/ee-joaopedromateusp/assets/SWOT_files/SWOT_EU_23'),
        ee.FeatureCollection('projects/ee-joaopedromateusp/assets/SWOT_files/SWOT_EU_24'),
        ee.FeatureCollection('projects/ee-joaopedromateusp/assets/SWOT_files/SWOT_EU_25'),
        ee.FeatureCollection('projects/ee-joaopedromateusp/assets/SWOT_files/SWOT_EU_26'),
        ee.FeatureCollection('projects/ee-joaopedromateusp/assets/SWOT_files/SWOT_EU_27'),
        ee.FeatureCollection('projects/ee-joaopedromateusp/assets/SWOT_files/SWOT_EU_29'),
        
        # Add more datasets 
    ]
    
    # Initialize with the first dataset in the list
    merged_dataset = datasets[0]
    
    # Loop through and merge each subsequent dataset
    for dataset in datasets[1:]:
        merged_dataset = merged_dataset.merge(dataset)

    night_mode = 'CartoDB.DarkMatter'
    normal_mode = 'HYBRID'
    
    # Options for confirming the reservoir selection
    modes = ['day theme', 'night theme']

        # Select box to confirm selection
    confirmation_mode = st.sidebar.selectbox("Choose this lake/reservoir", modes)
    if confirmation_mode == 'day theme':
        mode = normal_mode
    else:
        mode = normal_mode
    # Step 1: Create a geemap Map object with the required plugins
    m = geemap.Map(
        basemap=mode,
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
        plugin_LatLngPopup=True
    )
    
    m.set_center(13.5352, 48.8069, 5)

    from streamlit_folium import st_folium
    import folium
    import json
        
    # Define visualization parameters to color the polygons blue or yellow
    vis_params = {'color': 'Blue'}
    
    #m.addLayer(HydroLakes.style(**vis_params), {}, 'HydroLakes')
    # Add the HydroLakes layer to the map
    m.addLayer(merged_dataset.style(**vis_params), {}, 'Europe')
    
    # JavaScript for click events to set session state
    click_js = """
        function addClickHandler(map) {
            map.on('click', function(e) {
                const latlng = e.latlng;
                const coords = [latlng.lat, latlng.lng];
                window.parent.postMessage(coords, '*');
            });
        }
        addClickHandler(window.map);
    """

    # Add JavaScript to the map
    m.add_child(folium.Element(f'<script>{click_js}</script>'))

    # Display the map in Streamlit
    st_data = st_folium(m, height=800, width=1600)
            
    # Initialize session state for the selected ROI
    if 'roi' not in st.session_state:
        st.session_state['roi'] = None
            
    if st_data['last_clicked']:
        lat, lng = st_data['last_clicked']['lat'], st_data['last_clicked']['lng']
        point = ee.Geometry.Point([lng, lat])
        filtered = merged_dataset.filterBounds(point)
        info = filtered.getInfo()
        features = info['features']
        if features:
            properties = features[0]['properties']
            coordinates = features[0]['geometry']['coordinates']
            # Extracting the required fields
            lake_name = properties.get('names', 'N/A')
            lake_id = properties.get('lake_id', 'N/A')
            latitude = properties.get('lat', 'N/A')
            longitude = properties.get('lon', 'N/A')
            ref_area = properties.get('ref_area', 'N/A')
            storage = properties.get('storage', 'N/A')
            
            # Display metrics in Streamlit
            st.title("Lake Information")
            # Using Streamlit columns for a clean layout
            #col1, col2 = st.columns(2)
            #with col1:
                #st.metric("Lake Name", lake_name)
                #st.metric("Lake ID", lake_id)
            #with col2:
                #st.metric("Latitude", round(latitude, 4))
                #st.metric("Longitude", round(longitude, 4))
            
            # Display reference area with one decimal for clarity
            #st.metric("Reference Area (sq km)", f"{ref_area:.1f}")
            # Ensure coordinates are in the correct format for GeoJSON (swapping lon, lat to lat, lon)
            #if isinstance(coordinates[0][0], list):  # Check if it's a nested list (MultiPolygon or Polygon)
                # Swap lon and lat if necessary
                #coordinates = [list(map(lambda coord: [coord[1], coord[0]], sub_coord)) for sub_coord in coordinates]
            
            # Create the Earth Engine geometry (assuming Polygon type)
            aoi = ee.Geometry.Polygon(coordinates)
            
            roi = aoi
            
            globathy_dataset = ee.FeatureCollection("projects/ee-joaopedromateusp/assets/HydroLAKES")
            
            # Add the HydroLakes layer to the map
            m.addLayer(globathy_dataset.style(**vis_params), {}, 'Globathy')
            
            point = ee.Geometry.Point([lng, lat])
            filtered = globathy_dataset.filterBounds(point)
            info = filtered.getInfo()
            features = info['features']
            if features:
                properties = features[0]['properties']
                hydrolakes_id = properties.get('Hylak_id', 'N/A')
                Vol_res = properties.get('Vol_res','N/A')
                Grand_id = properties.get('Grand_id','N/A')
                # Using Streamlit columns for a clean layout
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Hydrolakes ID", hydrolakes_id)
                    st.metric("Maximum Volume", Vol_res)
                with col2:
                    st.metric("GranD ID", Grand_id)
    
            import ee
            import geemap
            import os
            import matplotlib.pyplot as plt
            import rasterio
            from rasterio.plot import show
            from skimage import measure
            from shapely.geometry import Polygon, box
            from shapely.ops import transform
            import numpy as np
            import json
    
           # Filter Sentinel-2 images
            sentinelImageCollection = ee.ImageCollection('COPERNICUS/S2') \
               .filterBounds(roi) \
               .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5)) \
               .sort('system:time_start', False)  # Sort by time_start in descending order
    
           # Get the latest (first) image from the sorted collection
            latest_image = sentinelImageCollection.first()
            
            previous_image = sentinelImageCollection.toList(sentinelImageCollection.size()).get(1)
            previous_image = ee.Image(previous_image)
    
           # Define a function to calculate NDWI and mask
            def calculate_ndwi_and_mask(image):
               ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
               ndwi_threshold = ndwi.gte(0.0)
               ndwi_mask = ndwi_threshold.updateMask(ndwi_threshold)
               return ndwi_mask
    
           # Apply the function to the latest image to calculate NDWI mask
            ndwi_mask = calculate_ndwi_and_mask(latest_image)
            ndwi_prev_mask = calculate_ndwi_and_mask(previous_image)
    
           # Define a function to calculate water area
            def calculate_water_area(image):
               water_area = image.multiply(ee.Image.pixelArea()).reduceRegion(
                   reducer=ee.Reducer.sum(),
                   geometry=roi,
                   scale=5
               ).get('NDWI')
               return image.set('water_area', water_area)
    
            # Calculate water area for the NDWI mask
            ndwi_mask_with_area = calculate_water_area(ndwi_mask)
            ndwi_pre_mask_with_area = calculate_water_area(ndwi_prev_mask)
           
            m.add_marker(lat=lat, lon=lng, location=[lat, lng])
            m.set_center(lng, lat, 14)
            
            globathy_dataset = ee.FeatureCollection("projects/ee-joaopedromateusp/assets/HydroLAKES")
            
            # Add the HydroLakes layer to the map
            m.addLayer(globathy_dataset.style(**vis_params), {}, 'Globathy')
            
            point = ee.Geometry.Point([lng, lat])
            filtered = globathy_dataset.filterBounds(point)
            info = filtered.getInfo()
            features = info['features']
            if features:
                properties = features[0]['properties']
                hydrolakes_id = properties.get('Hylak_id', 'N/A')
                Vol_res = properties.get('Vol_res','N/A')
                Grand_id = properties.get('Grand_id','N/A')
                Country = properties.get('Country','N/A')
                try:
           # Get the water area information
                    water_area_info = ndwi_mask_with_area.get('water_area').getInfo()
                    pre_water_area_info = ndwi_pre_mask_with_area.get('water_area').getInfo()
                    prev = round((pre_water_area_info / 1e6), 2)
                    water_area_km2 = round((water_area_info / 1e6), 2)
                    variance = round(((water_area_km2 - prev) / prev) * 100, 2)  # Calculate variance as a percentage
                    import netCDF4 as nc
                    import numpy as np
                    
                    # Open the NetCDF file
                    nc_file = nc.Dataset('/Users/joaopimenta/Downloads/Master thesis/GLOBathy_hAV_relationships.nc')
                    
                    # Specify the lake ID you want to search for
                    target_lake_id = hydrolakes_id  # Replace this with the actual lake ID you're interested in
                                                                                    
                    # Find the index of the lake based on the lake ID
                    lake_ids = nc_file.variables['lake_id'][:]
                    
                    # Check if the target lake ID exists in the lake_id variable
                    lake_index = np.where(lake_ids == target_lake_id)[0]
                    
                    if len(lake_index) == 0:
                        st.write("Lake not found in the dataset.")
                    else:
                        lake_index = lake_index[0]  # Use the first match if found
                    
                        # Extract coefficients of the area-storage equation for the identified lake
                        area_storage_coeffs = nc_file.variables['f_hA'][lake_index, :]
                        lon_lat = nc_file.variables['lon_lat'][lake_index, :]
                        import numpy as np
                        # Coefficients obtained from the NetCDF dataset
                        a = area_storage_coeffs[0]
                        b = area_storage_coeffs[1]
                        # Calculate the volume using the area-storage equation
                        volume = ((water_area_info/1e6) / a) ** (1 / b)
                        volume_prev = ((pre_water_area_info/1e6) / a) ** (1 / b)
                        vol_variance = round(((volume - volume_prev) / volume_prev) * 100, 2)
                except Exception as e:
                 st.write("Error retrieving water area information:", e)
                # Using Streamlit columns for a clean layout
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Lake Name", lake_name)
                    st.metric("Lake ID", lake_id)
                    st.metric("Hydrolakes ID", hydrolakes_id)
                    st.metric("Maximum Volume(10⁸ m³)", Vol_res/10)
                with col2:
                    # Display metric with variance as delta
                    st.metric(
                        label="Current Water Area",
                        value=f"{water_area_km2} km²",
                        delta=f"{variance}%",  # Add percentage change as delta
                        delta_color="normal",
                        help=None,
                        label_visibility="visible",
                    )
                    st.metric(
                        label="Current Water Volume",
                        value=f"{round(volume,2)} x10⁸m³",
                        delta=f"{vol_variance}%",  # Add percentage change as delta
                        delta_color="normal",
                        help=None,
                        label_visibility="visible",
                    )
                    st.metric("Country",Country)
                    st.metric("GranD ID", Grand_id)
            else:
                st.write("No features were selected")
            # Highlight the selected lake
            m.addLayer(ee.Image().paint(aoi, 1, 3), {'palette': 'red'}, 'Selected Lake')
        
        else:
            st.write('No polygon found at clicked location.')
        
        # Function to export ROI as GeoJSON
        def export_roi_as_geojson(roi):
            if roi:
                roi_geojson = roi.getInfo()
                if roi_geojson.get('type') == 'Polygon':
                    geojson_str = json.dumps(roi_geojson)
                    return geojson_str
                else:
                    st.error("GeoJSON type is not supported.")
                    return None
            else:
                st.error("No ROI available.")
                return None
        
        geojson_str = export_roi_as_geojson(aoi)
        if geojson_str:
            st.download_button(
                label="Download ROI as GeoJSON",
                data=geojson_str,
                file_name="roi.geojson",
                mime="application/geo+json"
            )
        # Options for confirming the reservoir selection
        box_reservoir = ['No', 'Yes']

        # Select box to confirm selection
        confirmation = st.selectbox("Choose this lake/reservoir", box_reservoir)

        # Handle the selection
        if confirmation == 'Yes':
            st.session_state['roi'] = aoi  # Store the selected ROI in session state
            roi = aoi  # Set the roi for further processing
            st.success("Reservoir selected successfully!")
        else:
            st.warning("No reservoir selected yet.")

    # If a region of interest (ROI) is available, provide download
    if uploaded_file is not None:
        try:
            gdf = process_uploaded_file(uploaded_file)

            if not gdf.empty:
                roi_fc = geemap.geopandas_to_ee(gdf)
                roi_geometry = roi_fc.geometry()
                aoi = roi_geometry
                st.session_state['roi'] = aoi  # Store the selected ROI in session state
                roi = aoi  # Set the roi for further processing
                st.success("Reservoir selected successfully!")
                                
                # Add markers for each feature in the GeoDataFrame
                for index, row in gdf.iterrows():
                    
                    latitude, longitude = row.geometry.centroid.coords[0]  # Get centroid coordinates
                    m.add_marker(location =[lng,lat])
                    # Set the map center and zoom level based on the selected location
                    m.set_center(lat, lng, 12)
                    globathy_dataset = ee.FeatureCollection("projects/ee-joaopedromateusp/assets/HydroLAKES")
            
                    # Add the HydroLakes layer to the map
                    m.addLayer(globathy_dataset.style(**vis_params), {}, 'Globathy')
                    
                    point = ee.Geometry.Point([lng, lat])
                    filtered = globathy_dataset.filterBounds(point)
                    info = filtered.getInfo()
                    features = info['features']
                    if features:
                        properties = features[0]['properties']
                        hydrolakes_id = properties.get('Hylak_id', 'N/A')
                        Vol_res = properties.get('Vol_res','N/A')
                        Grand_id = properties.get('Grand_id','N/A')
                        # Using Streamlit columns for a clean layout
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Hydrolakes ID", hydrolakes_id)
                            st.metric("Maximum Volume", Vol_res)
                        with col2:
                            st.metric("GranD ID", Grand_id)
                m.addLayer(roi_fc, {}, "Uploaded Data")
        except Exception as e:
            st.write(f"Error processing uploaded file: {e}")
                     
    if 'roi' in st.session_state and 'aoi' in locals():
                           
                    roi = aoi  # Use the selected ROI
                   # Create a select box for choosing the area-volume relationship method
                    opt = ["Don't have that info", "Write the A-V function of your reservoir", "upload excel sheet", "upload the DEM"]
                    method = st.sidebar.selectbox(
                        "Choose the area-volume relationship input",
                        opt,
                        key="method")
                    
                    if method == ("Write the A-V function of your reservoir"):
                                            volumes =[]
                                            column1, column2 = st.sidebar.columns(2)
                                            with column1:
                                                a = st.number_input("Coefficient a")
                                            with column2 :
                                                b = st.number_input("Coefficient b")
                                                
                    elif method == ("upload excel sheet"):                                            
                                            # File uploader for Excel files
                                            uploaded_file = st.file_uploader("Upload an Excel File", type=["xlsx"])
                                            
                                            if uploaded_file is not None:
                                                
                                                # Add an input box for the user to enter a sheet index number
                                                sheet_index = int(st.number_input("Enter the index of the Excel sheet (first sheet is 0)", min_value=0))
                                                st.write("You entered sheet index:", sheet_index)
                                                
                                                try:
                                                    # Load the Excel file into a DataFrame from the specified sheet
                                                    df = pd.read_excel(uploaded_file, sheet_name=sheet_index)
                                            
                                                    # Check if the required columns are present
                                                    if 'ÁREA (m2)' not in df.columns or 'VOLUME (m3)' not in df.columns:
                                                        st.error("Required columns 'ÁREA (m2)' or 'VOLUME (m3)' not found in the sheet.")
                                                    else:
                                                        # Drop rows with NaN values in the required columns
                                                        df = df.dropna(subset=['ÁREA (m2)', 'VOLUME (m3)'])
                                                        
                                                        # Initialize a dictionary
                                                        dictionary = {}
                                                        
                                                        # Populate the dictionary with 'ÁREA (m2)' as keys and 'VOLUME (m3)' as values
                                                        for index, row in df.iterrows():
                                                            area = row['ÁREA (m2)']
                                                            volume = row['VOLUME (m3)']
                                                            dictionary[area] = volume
                                                        
                                                        # Display the created dictionary
                                                        st.write("dictionary =", dictionary)
                                            
                                                except ValueError as e:
                                                    st.error(f"Error reading sheet index {sheet_index}: {e}")
                                                except Exception as e:
                                                    st.error(f"An error occurred: {e}")
        
                    elif method == "upload the DEM":
                        
                       import rasterio
                       import numpy as np
                       import matplotlib.pyplot as plt
                       from mpl_toolkits.axes_grid1 import make_axes_locatable
                       
                       # File uploader for GeoTIFF
                       dem_file = st.file_uploader("Upload a GeoTIFF File")
        
                       if dem_file is not None:
                           
                           with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                                tmp_file.write(dem_file.getbuffer())
                                tmp_file_path = tmp_file.name
                                
                           # Load the raster data
                           lakeRst = rasterio.open(tmp_file_path)
                           st.write("Number of bands:", lakeRst.count)
        
                           # Raster resolution
                           resolution = lakeRst.res
                           st.write("Resolution:", resolution)
        
                           # Read the first band (assuming single band raster)
                           lakeBottom = lakeRst.read(1)
                           st.write("Sample raster data:\n", lakeBottom[:5, :5])
        
                           # Replace no-data value with np.nan
                           noDataValue = np.copy(lakeBottom[0, 0])
                           lakeBottom = lakeBottom.astype(float)
                           lakeBottom[lakeBottom == noDataValue] = np.nan
        
                           # Display the raster data
                           plt.figure(figsize=(12, 12))
                           plt.imshow(lakeBottom, cmap='viridis')
                           plt.title('Lake Bottom Elevation')
                           plt.colorbar(label='Elevation (masl)')
                           st.pyplot(plt)
        
                           # Calculate minimum and maximum elevation
                           minElev = np.nanmin(lakeBottom)
                           maxElev = np.nanmax(lakeBottom)
                           st.write('Min bottom elevation: %.2f m, Max bottom elevation: %.2f m' % (minElev, maxElev))
        
                           # Define the number of steps for calculation
                           nSteps = 20
        
                           # Generate elevation steps
                           elevSteps = np.round(np.linspace(minElev, maxElev, nSteps), 2)
                           st.write("Elevation steps:", elevSteps)
        
                           # Define function to calculate volume at a given elevation step
                           def calculateVol(elevStep, elevDem, lakeRst):
                               tempDem = elevStep - elevDem[elevDem < elevStep]
                               tempVol = tempDem.sum() * lakeRst.res[0] * lakeRst.res[1]
                               return tempVol
        
                           # Define function to calculate inundated area for a given elevation
                           def calculateArea(elevStep, elevDem):
                               inundated_mask = np.where(elevDem <= elevStep, 1, 0)
                               area = np.sum(inundated_mask) * resolution[0] * resolution[1]
                               return area
        
                           # Calculate volumes and areas for each elevation step
                           volArray = []
                           areaArray = []
                           for elev in elevSteps:
                               tempVol = calculateVol(elev, lakeBottom, lakeRst)
                               tempArea = calculateArea(elev, lakeBottom)
                               volArray.append(tempVol)
                               areaArray.append(tempArea)
                               st.write(f"Elevation: {elev}, Area: {tempArea}, Volume: {tempVol / 1e6} MCM")
        
                           # Convert volumes to million cubic meters
                           volArrayMCM = [round(vol / 1e6, 2) for vol in volArray]
        
                           # Print results
                           st.write("Elevation steps (m):", elevSteps)
                           st.write("Volumes (MCM):", volArrayMCM)
        
                           # Plot elevation vs volume
                           fig, ax = plt.subplots(figsize=(12, 5))
                           ax.plot(volArrayMCM, elevSteps, label='Lake Volume Curve')
                           ax.grid(True)
                           ax.legend()
                           ax.set_xlabel('Volume (MCM)')
                           ax.set_ylabel('Elevation (masl)')
                           st.pyplot(fig)
        
                           # Plot lake bottom elevation and volume curve side by side
                           fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(20, 8), gridspec_kw={'width_ratios': [2, 1]})
                           ax1.set_title('Lake Bottom Elevation')
                           botElev = ax1.imshow(lakeBottom, cmap='viridis')
        
                           divider = make_axes_locatable(ax1)
                           cax = divider.append_axes('bottom', size='5%', pad=0.5)
                           fig.colorbar(botElev, cax=cax, orientation='horizontal', label='Elevation (masl)')
        
                           ax2.plot(volArrayMCM, elevSteps, label='Lake Volume Curve')
                           ax2.grid(True)
                           ax2.legend()
                           ax2.set_xlabel('Volume (MCM)')
                           ax2.set_ylabel('Elevation (masl)')
                           st.pyplot(fig)
        
                           # Print elevation and corresponding inundated area
                           st.write("Elevation (m)   Inundated Area (sq. meters)")
                           for elev, area in zip(elevSteps, areaArray):
                               st.write("{:.2f}              {:.2f}".format(elev, area))
        
                           st.write("Inundated Area (sq. meters)    Volume (MCM)")
                           for area, vol in zip(areaArray, volArrayMCM):
                               st.write("{:.2f}                      {:.2f}".format(area, vol))
        
                           # Plot the inundated area-volume curve
                           fig, ax = plt.subplots(figsize=(10, 6))
                           ax.plot(areaArray, volArrayMCM, label='Inundated Area-Volume Curve')
                           ax.set_xlabel('Inundated Area (square meters)')
                           ax.set_ylabel('Volume (MCM)')
                           ax.grid(True)
                           ax.legend()
                           plt.title('Inundated Area-Volume Curve')
                           st.pyplot(fig)
                           # Create and display area-volume curve dictionary
                           area_volume_curve = {}
                           for area,vol in zip(areaArray, volArrayMCM):
                               area_volume_curve[float(area)]= vol
                               
                           st.write(area_volume_curve)
                        
                    import datetime
                    # Date input for filtering Sentinel-2 images
                    startDate = st.sidebar.date_input("Start Date", value=None, min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
                    endDate = st.sidebar.date_input("End Date", value=datetime.datetime.now(), min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
                    # Sidebar selection for output
                    output = st.sidebar.multiselect("Select the output", 
                                                      ["Water Area", "Water Surface Elevation", "Water Volume", 
                                                       "Bathymetry file", "Timelapse", "Storage-Capacity curve" 
                                                       ])
                                            
                    st.sidebar.info("Choose the cloud coverage percentage of the satellite images")
                    threshold = st.sidebar.slider("Cloud Percentage Threshold", 0, 20, 5)
                    
                    if st.sidebar.button("Start computing") and startDate and endDate and threshold:
                        if "Timelapse" in output:
                            with st.spinner('Creating Timelapse...'):   
                                # Export the GIF
                                import geemap
                                gif_path = "/Users/joaopimenta/Downloads/Master thesis/Python scripts/Test_gee/ndwi_timelapse.gif"
                                Map = geemap.Map()
                                Map.add_landsat_ts_gif(layer_name='Timelapse', roi=roi, label=f'{lat}, {lng}', start_year=2021, end_year=2024, start_date='06-10', end_date='09-20', bands=['SWIR1', 'NIR', 'Red'], vis_params=None, dimensions=768, frames_per_second=2, font_size=30, font_color='white', add_progress_bar=True, progress_bar_color='white', progress_bar_height=5, out_gif=gif_path, download=True, apply_fmask=True, nd_bands=None, nd_threshold=0, nd_palette=['black', 'blue'])
                                file_ = open(gif_path, "rb")
                                contents = file_.read()
                                data_url = base64.b64encode(contents).decode("utf-8")
                                file_.close()

                                st.markdown(
                                    f'<img src="data:image/gif;base64,{data_url}" alt="timelapse gif">',
                                    unsafe_allow_html=True,
                                )                    
                        # Convert the date objects to strings in the format expected by EE
                        start_date_str = startDate.strftime('%Y-%m-%d')
                        end_date_str = endDate.strftime('%Y-%m-%d')
                        
                        sentinel_image_collection = ee.ImageCollection('COPERNICUS/S2') \
                            .filterBounds(roi) \
                            .filterDate(start_date_str, end_date_str)
                            
                        sentinel_image = sentinel_image_collection \
                            .sort('CLOUDY_PIXEL_PERCENTAGE') \
                            .first() \
                            .clip(roi)
                            
                        # Visualize using RGB
                        m.addLayer(sentinel_image, 
                                     {'min': 0.0, 'max': 2000, 'bands': ['B4', 'B3', 'B2']}, 
                                     'RGB')
                        ndwi = sentinel_image.normalizedDifference(['B3', 'B8']).rename('NDWI')
                        m.addLayer(ndwi, 
                                     {'palette': ['red', 'yellow', 'green', 'cyan', 'blue']}, 
                                     'NDWI')
     
                        # Create NDWI mask
                        ndwi_threshold = ndwi.gte(0.0)
                        ndwi_mask = ndwi_threshold.updateMask(ndwi_threshold)
                        m.addLayer(ndwi_threshold, 
                                     {'palette': ['black', 'white']}, 
                                     'NDWI Binary Mask')
                        m.addLayer(ndwi_mask, 
                                     {'palette': ['blue']}, 
                                     'NDWI Mask')
                        if "Water Surface Elevation" in output:
                            # Send a request to the Hydrocron API to get lake data in CSV format
                            url = (
                                "https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries?"
                                "feature=PriorLake"
                                f"&feature_id={lake_id}"
                                f"&start_time={start_date_str}T00:00:00Z"
                                f"&end_time={end_date_str}T00:00:00Z"
                                "&output=csv"
                                "&fields=time_str,wse"
                            )
                            # Request the data
                            hydrocron_response = requests.get(url).json()
                            
                            # Extract CSV data from the response
                            csv_str = hydrocron_response['results']['csv']
                            
                            # Convert the CSV string into a pandas DataFrame
                            df = pd.read_csv(StringIO(csv_str))
                            
                            # Prepare to plot water surface elevation (WSE) and area
                            # Convert 'time_str' column to datetime format
                            df['time_str'] = pd.to_datetime(df['time_str'], errors='coerce')
                            
                            # Filter and store dates and elevations
                            df_filtered = df.dropna(subset=['time_str', 'wse'])
                            df_filtered['wse'] = pd.to_numeric(df_filtered['wse'], errors='coerce')
                            df_filtered = df_filtered.dropna(subset=['wse'])
                            
                            # Plot water surface elevation (WSE) over time
                            plt.figure(figsize=(10, 5))
                            plt.plot(df_filtered['time_str'], df_filtered['wse'], marker='o', linestyle='-')
                            plt.xlabel('Date')
                            plt.ylabel('Water Surface Elevation (m)')
                            plt.title(f'Water Surface Elevation for Lake {lake_name}')
                            plt.xticks(rotation=45)
                            plt.grid(True)
                        
                            # Show the plot in Streamlit
                            st.pyplot(plt)
                        
                            # Display the filtered DataFrame
                            st.write(df_filtered[['time_str', 'wse']])
                                                     
                        with st.spinner('Retrieving satilite images...'):
                             #Define a function to calculate NDWI
                            def calculate_ndwi(image):
                                     ndwi = image.normalizedDifference(["B8", "B3"])  # B8 is NIR and B3 is green
                                     return ndwi
                                  # Filter Sentinel-2 images
                            sentinelImageCollection = ee.ImageCollection('COPERNICUS/S2') \
                                      .filterBounds(roi) \
                                      .filterDate(start_date_str, end_date_str) \
                                      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', threshold)) \
                                      
                            # Check if images are available
                            num_images = sentinelImageCollection.size().getInfo()
                            st.write("Number of images:", num_images)
                            volumes = []
                            # Alternatively, convert acquisition times to readable format (if needed)
                            acquisition_times = sentinelImageCollection.aggregate_array('system:time_start').getInfo()
                            acquisition_dates = [datetime.datetime.utcfromtimestamp(time / 1000).strftime('%Y-%m-%d') for time in acquisition_times]
                            
                            if num_images == 0:
                                st.warning("No images available within the specified date range.")
                            else:
                                if threshold >= 15:
                                    st.write("CLoudless Algorithm will identify and remove the effects of clouds and shadows")

                                    START_DATE = start_date_str
                                    END_DATE = end_date_str
                                    CLOUD_FILTER = 40
                                    CLD_PRB_THRESH = 70
                                    NIR_DRK_THRESH = 0.15
                                    CLD_PRJ_DIST = 2
                                    BUFFER = 100
                                    # Function to get Sentinel-2 surface reflectance and cloud probability collections
                                    def get_s2_sr_cld_col(aoi, start_date, end_date):
                                        s2_sr_col = (ee.ImageCollection('COPERNICUS/S2_SR')
                                                     .filterBounds(aoi)
                                                     .filterDate(start_date, end_date)
                                                     .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', CLOUD_FILTER)))
        
                                        s2_cloudless_col = (ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')
                                                            .filterBounds(aoi)
                                                            .filterDate(start_date, end_date))
        
                                        return ee.ImageCollection(ee.Join.saveFirst('s2cloudless').apply(**{
                                            'primary': s2_sr_col,
                                            'secondary': s2_cloudless_col,
                                            'condition': ee.Filter.equals(**{
                                                'leftField': 'system:index',
                                                'rightField': 'system:index'
                                            })
                                        }))
        
                                    # Apply the function to build the collection
                                    s2_sr_cld_col = get_s2_sr_cld_col(roi, START_DATE, END_DATE)
        
                                    # Function to get cloud cover percentage for an image
                                    def get_cloud_cover_percentage(image):
                                        cloud_cover = ee.Image(image).get('CLOUDY_PIXEL_PERCENTAGE')
                                        return ee.Feature(None, {'cloud_cover': cloud_cover, 'image_id': image.id()})
        
                                    # Apply the function to the collection
                                    image_list = s2_sr_cld_col.map(get_cloud_cover_percentage).getInfo()
        
                                    # Debug: Print the properties of the first image to inspect the available properties
                                    print("Inspecting the first image's properties:")
                                    print(image_list['features'][0]['properties'])
        
                                    # Extract the image ids, cloud covers, and dates (if available)
                                    image_info = []
                                    for f in image_list['features']:
                                        image_id = f['properties'].get('image_id', 'Unknown')
                                        cloud_cover = f['properties'].get('cloud_cover', 'Unknown')
                                        timestamp = f['properties'].get('system:time_start', None)
                                        
                                        # If timestamp is None, we'll set it to 'Unknown'
                                        if timestamp:
                                            date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
                                        else:
                                            date = 'Unknown'
                                        
                                        image_info.append((image_id, cloud_cover, date))
        
                                    print("Available images and their cloud cover percentages:")
                                    for idx, (image_id, cloud_cover, date) in enumerate(image_info):
                                        print(f"{idx}: Image ID: {image_id}, Date: {date}, Cloud Cover: {cloud_cover}%")
        
                                    water_area_info = []
                                    # Count the number of images in the collection
                                    num_images = s2_sr_cld_col.size().getInfo()
                                    print(f"Total number of images in the collection: {num_images}")
                                    # Loop through each image in the collection and print its cloud cover
                                    for i in range(num_images):
                                        selected_idx = i
                                        selected_image_id = image_info[selected_idx][0]
                                        cloud_cover = image_info[selected_idx][1]  # Get the cloud cover for the selected image
                                        selected_image = ee.Image(s2_sr_cld_col.filter(ee.Filter.eq('system:index', selected_image_id)).first())
                                        print(f"Image ID: {selected_image_id}, Cloud Cover: {cloud_cover}%")
                                        if cloud_cover >= 15:
                                            # Define functions to add cloud and shadow bands
                                            def add_cloud_bands(img):
                                                cld_prb = ee.Image(img.get('s2cloudless')).select('probability')
                                                is_cloud = cld_prb.gt(CLD_PRB_THRESH).rename('clouds')
                                                return img.addBands(ee.Image([cld_prb, is_cloud]))
                                            
                                            def add_shadow_bands(img):
                                                not_water = img.select('SCL').neq(6)
                                                SR_BAND_SCALE = 1e4
                                                dark_pixels = img.select('B8').lt(NIR_DRK_THRESH * SR_BAND_SCALE).multiply(not_water).rename('dark_pixels')
                                                shadow_azimuth = ee.Number(90).subtract(ee.Number(img.get('MEAN_SOLAR_AZIMUTH_ANGLE')))
                                                cld_proj = (img.select('clouds').directionalDistanceTransform(shadow_azimuth, CLD_PRJ_DIST * 10)
                                                            .reproject(crs=img.select(0).projection(), scale=100)
                                                            .select('distance').mask().rename('cloud_transform'))
                                                shadows = cld_proj.multiply(dark_pixels).rename('shadows')
                                                return img.addBands(ee.Image([dark_pixels, cld_proj, shadows]))
                                            
                                            def add_cld_shdw_mask(img):
                                                img_cloud = add_cloud_bands(img)
                                                img_cloud_shadow = add_shadow_bands(img_cloud)
                                                is_cld_shdw = img_cloud_shadow.select('clouds').add(img_cloud_shadow.select('shadows')).gt(0)
                                                is_cld_shdw = (is_cld_shdw.focalMin(2).focalMax(BUFFER * 2 / 20)
                                                               .reproject(crs=img.select([0]).projection(), scale=20)
                                                               .rename('cloudmask'))
                                                return img_cloud_shadow.addBands(is_cld_shdw)
                                            
                                            # Define the function to apply the cloud and shadow mask
                                            def apply_cld_shdw_mask(img):
                                                not_cld_shdw = img.select('cloudmask').Not()
                                                return img.select('B.*').updateMask(not_cld_shdw)
                                            
                                            # Add cloud and shadow bands, apply the mask
                                            selected_image_with_mask = add_cld_shdw_mask(selected_image)
                                            cloud_free_image = apply_cld_shdw_mask(selected_image_with_mask)
                                            
                                            # Define a function to calculate NDWI and mask
                                            def calculate_ndwi_and_mask(image):
                                                ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
                                                ndwi_threshold = ndwi.gte(0.0)
                                                ndwi_mask = ndwi_threshold.updateMask(ndwi_threshold)
                                                return ndwi_mask
        
                                            # Apply the function to the latest image to calculate NDWI mask
                                            ndwi_mask = calculate_ndwi_and_mask(selected_image)
        
                                            # Define a function to calculate water area
                                            def calculate_water_area(image):
                                                water_area = image.multiply(ee.Image.pixelArea()).reduceRegion(
                                                    reducer=ee.Reducer.sum(),
                                                    geometry=roi,
                                                    scale=5
                                                ).get('NDWI')
                                                return image.set('water_area', water_area)
        
                                            # Calculate water area for the NDWI mask
                                            ndwi_mask_with_area = calculate_water_area(ndwi_mask)
                                            
                                            waterarea = ndwi_mask_with_area.get('water_area').getInfo()
                                            w = waterarea
                                            #print(f"This is the water area of the NDWI image:{w}")
                                            # Load the bathymetry dataset from Earth Engine
                                            globathy = ee.Image("projects/sat-io/open-datasets/GLOBathy/GLOBathy_bathymetry")
                                            
                                            # Export the data as an image
                                            out_dir = "/Users/joaopimenta/Desktop/GEE_test"  # Specify the output directory
                                            if not os.path.exists(out_dir):
                                                os.makedirs(out_dir)
                                            out_image_path = os.path.join(out_dir, "globathy_bathymetry.tif")  # Specify the output image path
                                            
                                            # Export the image
                                            geemap.ee_export_image(globathy, filename=out_image_path, scale=10, region=roi)
                                            
                                            # Load Bathymetry image
                                            bathymetry_path = out_image_path
                                            bathymetry_dataset = rasterio.open(bathymetry_path)
                                                    
                                            #print(f"This is the ndwi area of the lake {ndwi_masked_area}")
                                            # Export the binary water mask to a GeoTIFF file
                                            folder_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_dam_volume_images_tif"
                                            directory = "/Users/joaopimenta/Desktop"
                                            folder_path = os.path.join(directory, folder_name)
                                            os.makedirs(folder_path)
                                            
                                            geemap.ee_export_image(
                                                ndwi_mask,
                                                filename=os.path.join(folder_path, "binary_NDWI.tif"),
                                                region=roi,
                                                scale=10
                                            )
                                            
                                            file_name = "binary_NDWI.tif"
                                            file_path = os.path.join(folder_path, file_name)
                                            
                                            # Load NDWI image
                                            ndwi_path = file_path  # Update this path
                                            ndwi_dataset = rasterio.open(ndwi_path)
                                            ndwi = ndwi_dataset.read(1)
                                            
                                            with rasterio.open(file_path) as src:
                                                ndwi_data = src.read(1)  # Read the first band
                                                transform = src.transform
                                            
                                            # Convert NDWI to binary format for visualization
                                            binary_ndwi = np.where(ndwi_data == 1, 255, 0).astype(np.uint8)
                                            
                                            # Calculate the area of the detected water bodies from binary mask
                                            def calculate_area(image, transform):
                                                # Mask the image to include only water
                                                water_mask = image == 0
                                                
                                                # Compute the area in square meters
                                                pixel_area = abs(transform[0] * transform[4])  # pixel size (in square meters)
                                                water_area_pixels = np.sum(water_mask)
                                                total_area_m2 = water_area_pixels * pixel_area
                                                return total_area_m2
                                            
                                            # Calculate the area using the converted binary mask
                                            total_area_m2 = calculate_area(binary_ndwi, transform)/ 1e3
                                            #print(f"Total area calculated from binary mask: {total_area_m2 :.2f} km²")
                                            
                                            # Plot the results
                                            plt.figure(figsize=(15, 10))
                                            
                                            # Binary NDWI (K-means method)
                                            plt.subplot(1, 2, 1)
                                            plt.imshow(binary_ndwi, cmap='gray')
                                            plt.title('Binary NDWI (K-means)')
                                            
                                            # Identified contour (K-means method)
                                            plt.subplot(1, 2, 2)
                                            contour_image = np.zeros_like(binary_ndwi)
                                            contours, _ = cv2.findContours(binary_ndwi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                            if contours:
                                                cv2.drawContours(contour_image, [max(contours, key=cv2.contourArea)], -1, (255), 2)
                                            plt.imshow(contour_image, cmap='gray')
                                            plt.title('Identified Dam Contour (K-means)')
                                            
                                            plt.show()
                                            # Check for cloud pixels within the dam (ROI)
                                            cloud_pixels_in_roi = selected_image_with_mask.select('cloudmask').reduceRegion(
                                                reducer=ee.Reducer.sum(),
                                                geometry=roi,
                                                scale=10
                                            ).get('cloudmask').getInfo()
                                            
                                            print(f"This is the cloud pixels in the ROI:{cloud_pixels_in_roi}")
                                            # Export the cloud mask
                                            geemap.ee_export_image(
                                                selected_image_with_mask.select('cloudmask'),
                                                filename=os.path.join(folder_path, "cloud_mask.tif"),
                                                region=roi,
                                                scale=10
                                            )
                                            
                                            cloud_mask_path = os.path.join(folder_path, "cloud_mask.tif")
                                            cloud_mask_dataset = rasterio.open(cloud_mask_path)
                                            cloud_mask = cloud_mask_dataset.read(1)
                                            
                                            # Reproject the cloud mask to match NDWI resolution
                                            resampled_cloud_mask = np.empty_like(ndwi)
                                            
                                            reproject(
                                                source=cloud_mask,
                                                destination=resampled_cloud_mask,
                                                src_transform=cloud_mask_dataset.transform,
                                                src_crs=cloud_mask_dataset.crs,
                                                dst_transform=ndwi_dataset.transform,
                                                dst_crs=ndwi_dataset.crs,
                                                resampling=Resampling.nearest)
                                            
                                            # Mask the NDWI image by removing cloud pixels
                                            ndwi_masked = np.where(resampled_cloud_mask == 0, ndwi, np.nan)
                                            
                                            # Load Bathymetry image
                                            bathymetry_dataset = rasterio.open(bathymetry_path)
                                            
                                            # Reproject Bathymetry to the NDWI CRS
                                            dst_crs = ndwi_dataset.crs
                                            
                                            transform, width, height = calculate_default_transform(
                                                bathymetry_dataset.crs, dst_crs, bathymetry_dataset.width,
                                                bathymetry_dataset.height, *bathymetry_dataset.bounds)
                                            kwargs = bathymetry_dataset.meta.copy()
                                            kwargs.update({
                                                'crs': dst_crs,
                                                'transform': transform,
                                                'width': width,
                                                'height': height
                                            })
                                            
                                            reprojected_bathymetry = np.empty((height, width), dtype=np.float32)
                                            
                                            reproject(
                                                source=rasterio.band(bathymetry_dataset, 1),
                                                destination=reprojected_bathymetry,
                                                src_transform=bathymetry_dataset.transform,
                                                src_crs=bathymetry_dataset.crs,
                                                dst_transform=transform,
                                                dst_crs=dst_crs,
                                                resampling=Resampling.nearest)
                                            
                                            # Resample Bathymetry to match NDWI resolution
                                            resampled_bathymetry = np.empty_like(ndwi)
                                            
                                            reproject(
                                                source=reprojected_bathymetry,
                                                destination=resampled_bathymetry,
                                                src_transform=transform,
                                                src_crs=dst_crs,
                                                dst_transform=ndwi_dataset.transform,
                                                dst_crs=dst_crs,
                                                resampling=Resampling.bilinear)
                                            
                                            # Plot the images
                                            fig, ax = plt.subplots(figsize=(10, 10))
                                            
                                            # Plot the NDWI image
                                            ndwi_extent = (ndwi_dataset.bounds.left, ndwi_dataset.bounds.right, 
                                                           ndwi_dataset.bounds.bottom, ndwi_dataset.bounds.top)
                                            cax_ndwi = ax.imshow(ndwi_masked, cmap='Blues', extent=ndwi_extent, 
                                                                 alpha=0.6)
                                            
                                            # Overlay the Bathymetry image
                                            bathy_extent = (ndwi_dataset.bounds.left, ndwi_dataset.bounds.right,
                                                            ndwi_dataset.bounds.bottom, ndwi_dataset.bounds.top)
                                            cax_bathy = ax.imshow(resampled_bathymetry, cmap='viridis', 
                                                                  extent=bathy_extent, alpha=0.4)
                                            fig.colorbar(cax_bathy, ax=ax, fraction=0.046, pad=0.04,
                                                         label='Bathymetry')
                                            
                                            # Plot the NDWI cloud-removed image
                                            fig, ax = plt.subplots(figsize=(10, 10))
                                            
                                            # Plot the NDWI image
                                            ndwi_extent = (ndwi_dataset.bounds.left, ndwi_dataset.bounds.right, ndwi_dataset.bounds.bottom, ndwi_dataset.bounds.top)
                                            cax_ndwi = ax.imshow(ndwi_masked, cmap='Blues', extent=ndwi_extent)
                                            fig.colorbar(cax_ndwi, ax=ax, fraction=0.046, pad=0.04, label='NDWI')
                                            
                                            # Get the cloud mask from the selected image
                                            cloud_mask = selected_image_with_mask.select('cloudmask')
                                            
                                            # Apply cloud mask to the NDWI mask
                                            ndwi_cloud_removed_mask = ndwi_mask.updateMask(cloud_mask.Not())
                                            
                                            # Calculate the pixel area for the masked NDWI image
                                            pixel_area = ndwi_cloud_removed_mask.multiply(ee.Image.pixelArea())
                                            
                                            # Reduce the region to calculate the total water area
                                            water_area = pixel_area.reduceRegion(
                                                reducer=ee.Reducer.sum(),
                                                geometry=roi,
                                                scale=10,  # Adjust the scale as needed
                                                maxPixels=1e10
                                            )
                                            
                                            # Assuming water_area is the result from reduceRegion
                                            water = water_area.getInfo().get('NDWI')
                                            print(water)       
                                            # Get the total water area in square meters
                                            total_water_area_m2 = total_area_m2
                                            
                                            # Convert the area to square kilometers
                                            total_water_area_km2 = total_water_area_m2 / 1e6# Convert the area to square kilometers
                                            total_water_area_adjusted = total_water_area_m2 
                                            
                                            area_cloud_aftected = w - total_water_area_adjusted
                                            cloud_affect_percentage = area_cloud_aftected/ cloud_pixels_in_roi
                                            
                                            print(f"The total NDWI water area is:{w}")
                                            print(f"The adjusted water area is: {total_water_area_adjusted}")
                                            print(f"The total amount of pixels covering the reservoir is:{area_cloud_aftected}")
                                            print(f"This is the area cloud pixels in the ROI:{cloud_pixels_in_roi*10}")
                                            print(f"The percentage of pixels which affect the reservoir's area  are :{cloud_affect_percentage}")
                                            
                                            if cloud_pixels_in_roi > 0:
                                                import rasterio
                                                import numpy as np
                                                import matplotlib.pyplot as plt
                                                from skimage import measure
                                                from shapely.geometry import Polygon
                                                from pyproj import Transformer
                                                import rasterio.transform
                                                from scipy.ndimage import binary_fill_holes  # To fill inside polygons
                                                from rasterio.warp import reproject, Resampling, calculate_default_transform
                                            
                                                # Path to bathymetry raster file
                                                path_bathymetry = "/Users/joaopimenta/Desktop/GEE_test/globathy_bathymetry.tif"
                                                # Path to NDWI raster file (the one with the projection you want)
                                                path_ndwi = ndwi_path
                                                path_cloud_mask = cloud_mask_path
                                            
                                                # Load Bathymetry image
                                                bathymetry_dataset = rasterio.open(path_bathymetry)
                                                cloud_mask_dataset = rasterio.open(path_cloud_mask)
                                                ndwi_dataset = rasterio.open(path_ndwi)
                                            
                                                # Reproject Bathymetry to the NDWI CRS if necessary
                                                dst_crs = ndwi_dataset.crs
                                            
                                                transform, width, height = calculate_default_transform(
                                                    bathymetry_dataset.crs, dst_crs, bathymetry_dataset.width, bathymetry_dataset.height, *bathymetry_dataset.bounds)
                                            
                                                kwargs = bathymetry_dataset.meta.copy()
                                                kwargs.update({
                                                    'crs': dst_crs,
                                                    'transform': transform,
                                                    'width': width,
                                                    'height': height
                                                })
                                            
                                                reprojected_bathymetry = np.empty((height, width), dtype=np.float32)
                                            
                                                reproject(
                                                    source=rasterio.band(bathymetry_dataset, 1),
                                                    destination=reprojected_bathymetry,
                                                    src_transform=bathymetry_dataset.transform,
                                                    src_crs=bathymetry_dataset.crs,
                                                    dst_transform=transform,
                                                    dst_crs=dst_crs,
                                                    resampling=Resampling.nearest)
                                            
                                                # Reproject cloud mask to the bathymetry CRS if necessary
                                                if bathymetry_dataset.crs != cloud_mask_dataset.crs:
                                                    print("CRS misalignment detected. Reprojecting cloud mask to bathymetry CRS.")
                                                    reprojected_cloud_mask = np.empty_like(reprojected_bathymetry)
                                                    reproject(
                                                        source=rasterio.band(cloud_mask_dataset, 1),
                                                        destination=reprojected_cloud_mask,
                                                        src_transform=cloud_mask_dataset.transform,
                                                        src_crs=cloud_mask_dataset.crs,
                                                        dst_transform=transform,
                                                        dst_crs=dst_crs,
                                                        resampling=Resampling.nearest
                                                    )
                                                else:
                                                    reprojected_cloud_mask = cloud_mask_dataset.read(1)
                                            
                                                # Resample Bathymetry and cloud mask to match NDWI resolution if necessary
                                                resampled_bathymetry = np.empty_like(ndwi_dataset.read(1))
                                                resampled_cloud_mask = np.empty_like(ndwi_dataset.read(1))
                                            
                                                reproject(
                                                    source=reprojected_bathymetry,
                                                    destination=resampled_bathymetry,
                                                    src_transform=transform,
                                                    src_crs=dst_crs,
                                                    dst_transform=ndwi_dataset.transform,
                                                    dst_crs=dst_crs,
                                                    resampling=Resampling.bilinear)
                                            
                                                reproject(
                                                    source=reprojected_cloud_mask,
                                                    destination=resampled_cloud_mask,
                                                    src_transform=transform,
                                                    src_crs=dst_crs,
                                                    dst_transform=ndwi_dataset.transform,
                                                    dst_crs=dst_crs,
                                                    resampling=Resampling.nearest)
                                            
                                                # Load bathymetry raster data
                                                lakeBottom = resampled_bathymetry
                                                resolution = bathymetry_dataset.res
                                                lake_crs = bathymetry_dataset.crs
                                                lake_transform = bathymetry_dataset.transform
                                            
                                                # Load NDWI raster data (to get CRS and extent)
                                                ndwi_extent = (ndwi_dataset.bounds.left, ndwi_dataset.bounds.right, ndwi_dataset.bounds.bottom, ndwi_dataset.bounds.top)
                                            
                                                # Replace no-data value with np.nan for the bathymetry raster
                                                noDataValue = lakeBottom[0, 0]
                                                lakeBottom = lakeBottom.astype(float)
                                                lakeBottom[lakeBottom == noDataValue] = np.nan
                                            
                                                # Calculate minimum and maximum elevation
                                                minElev = np.nanmin(lakeBottom)
                                                maxElev = np.nanmax(lakeBottom)
                                            
                                                # Define number of steps for calculation
                                                nSteps = 50
                                                elevSteps = np.round(np.linspace(minElev, maxElev, nSteps), 2)
                                            
                                                # Define function to create a mask for a specific elevation
                                                def createMaskForElevation(elevation, elevDem, cloud_mask):
                                                    # Create a mask based on the elevation
                                                    mask = np.where(elevDem <= elevation, 1, 0)
                                                    
                                                    # Fill holes inside the polygon
                                                    filled_mask = binary_fill_holes(mask) * mask  # Ensures it's a binary mask
                                                    
                                                    waterarea = np.sum(mask) * (resolution[0] * resolution[1])
                                                    area_Array.append(waterarea)
                                                    # Apply the cloud mask, setting cloud-covered pixels to 0
                                                    filled_mask[cloud_mask == 1] = 0
                                                    
                                                    return filled_mask
                                            
                                                # Set up transformation to match NDWI CRS
                                                transformer = Transformer.from_crs(lake_crs, ndwi_dataset.crs, always_xy=True)
                                            
                                                # Arrays to store the areas for each elevation step
                                                areaArray = []
                                                area_Array = []
                                            
                                                # Plot setup
                                                fig, ax = plt.subplots(figsize=(12, 10))
                                                colors = plt.cm.viridis(np.linspace(0, 1, len(elevSteps)))
                                            
                                                for i, elev in enumerate(elevSteps):
                                                    # Create a mask for the current elevation and apply cloud mask
                                                    mask = createMaskForElevation(elev, lakeBottom, resampled_cloud_mask)
                                            
                                                    # Calculate water area by summing valid pixels (non-cloud, non-zero)
                                                    water_area = np.sum(mask) * (resolution[0] * resolution[1])  # Pixel resolution area
                                                    
                                                    areaArray.append(water_area)
                                                    
                                                    # Find contours (polygons) from the mask
                                                    contours = measure.find_contours(mask, 0.5)
                                                    
                                                    # Reproject and plot each contour as a polygon
                                                    for contour in contours:
                                                        lon_lat_coords = rasterio.transform.xy(lake_transform, contour[:, 0], contour[:, 1])
                                                        x_coords, y_coords = np.array(lon_lat_coords[0]), np.array(lon_lat_coords[1])
                                                        
                                                        # Reproject coordinates to NDWI CRS
                                                        x_proj, y_proj = transformer.transform(x_coords, y_coords)
                                                        
                                                        # Plot the reprojected contour
                                                        ax.plot(x_proj, y_proj, color=colors[i], label=f'Elevation {elev} m' if i == 0 else "")
                                            
                                                # Set the same extent as the NDWI image
                                                ax.set_xlim(ndwi_extent[0], ndwi_extent[1])
                                                ax.set_ylim(ndwi_extent[2], ndwi_extent[3])
                                                                                        
                                                # Plot the elevation vs area
                                                areaArraySqM = [area * 1e8 for area in areaArray] # Convert to square meters
                                                area_ArraySqM = [area * 1e8 for area in area_Array] 
                                                # Paths to the raster file
                                                path = "/Users/joaopimenta/Desktop/GEE_test/globathy_bathymetry.tif"
                                            
                                                # Load the raster data
                                                lakeRst = rasterio.open(path)
                                                lakeBottom = lakeRst.read(1)
                                            
                                                # Raster resolution (in meters, assuming UTM projection)
                                                resolution = lakeRst.res
                                                print("Resolution:", resolution)
                                            
                                                # Replace no-data value with np.nan
                                                noDataValue = np.copy(lakeBottom[0, 0])
                                                lakeBottom = lakeBottom.astype(float)
                                                lakeBottom[lakeBottom == noDataValue] = np.nan
                                                # Get the pixel size from raster resolution (in meters)
                                                pixelArea = lakeRst.res[0] * lakeRst.res[1]  # in square meters
                                            
                                                # Calculate the area of the detected water bodies from binary mask
                                                def calculate_area(image, transform):
                                                    # Mask the image to include only water
                                                    water_mask = image == 0
                                                    
                                                    # Compute the area in square meters
                                                    pixel_area = abs(transform[0] * transform[4])  # pixel size (in square meters)
                                                    water_area_pixels = np.sum(water_mask)
                                                    total_area_m2 = water_area_pixels * pixel_area
                                                    return total_area_m2
                                                # Define function to create mask for a specific elevation
                                                def createMaskForElevation(elevation, elevDem):
                                                    mask = np.where(elevDem <= elevation, 1, 0)  # White pixels for inundated area
                                                    return mask
                                            
                                                # Arrays to store the areas for each elevation step
                                                area_normal_Array = []
                                            
                                                # Plot all polygons representing water area for each elevation step
                                                fig, ax = plt.subplots(figsize=(12, 10))
                                            
                                                # Colors for different elevation levels
                                                colors = plt.cm.viridis(np.linspace(0, 1, len(elevSteps)))
                                            
                                                # Loop over each elevation step, calculate area, and plot polygons
                                                for i, elev in enumerate(elevSteps):
                                                    # Create a mask for the current elevation step
                                                    mask = createMaskForElevation(elev, lakeBottom)
                                                    
                                                    # Calculate the water area at this elevation
                                                    waterArea = np.sum(mask) * pixelArea  # sum of all '1' pixels * pixel area
                                                    area_normal_Array.append(waterArea)  # Store the area for this elevation
                                                    
                                                    # Find contours (polygons) from the mask
                                                    contours = measure.find_contours(mask, 0.5)
                                                    
                                                    # Plot each contour as a polygon
                                                    for contour in contours:
                                                        # Transform contour coordinates to UTM coordinates using the raster transform
                                                        utm_coords = rasterio.transform.xy(lakeRst.transform, contour[:, 0], contour[:, 1])
                                                        x_coords, y_coords = np.array(utm_coords[0]), np.array(utm_coords[1])
                                                        
                                                        # Plot the polygon for the current elevation step
                                                        ax.plot(x_coords, y_coords, color=colors[i], label=f'Elevation {elev} m' if i == 0 else "")
                                                                                
                                                # Plot the elevation vs area
                                                # Multiply the area by 1,000,000 to convert from km² to m² if necessary
                                                area_normal_ArraySqM = [area * 1e8 for area in area_normal_Array]  # Convert to square meters
                                            
                                                # Function to create a binary mask for the chosen elevation
                                                def createMaskForElevation(elevation, elevDem, resolution):
                                                    # Step 1: Generate the initial binary mask (1 for water, 0 for no water)
                                                    mask = np.where(elevDem <= elevation, 1, 0)
                                                    
                                                    # Step 2: Fill the holes inside the lake region
                                                    filled_mask = binary_fill_holes(mask) * mask  # Fill holes only inside the mask
                                                    
                                                    # Step 3: Create a mask for the lake region (anything inside the boundary is considered lake)
                                                    lake_mask = np.where(np.isnan(elevDem), 1, 0)  # NaN represents outside the lake
                                                    
                                                    # Step 4: Assign a value of 1 to everything outside the lake region
                                                    result_mask = np.where(lake_mask == 1, 1, filled_mask)
                                                    
                                                    # Step 5: Calculate the inundated area for the white pixels inside the lake
                                                    area = np.sum(filled_mask) * resolution[0] * resolution[1]
                                                    
                                                    return result_mask, area
                                                # Ensure differences, areaArraySqM, and elev are arrays or lists
                                                differences = []
                                            
                                                for area in areaArraySqM:
                                                    dif = abs(water - area) # Absolute difference
                                                    differences.append(dif)
                                                    
                                                print(f"The water area without the cloud pixels is: {water}")
                                            
                                                # Find the index of the smallest difference
                                                best_match_index = differences.index(min(differences))
                                                best_match = area_ArraySqM[best_match_index]
                                            
                                                # Reverse the elevation steps and convert to a list to allow indexing
                                                step_elevation_reversed = list(reversed(elevSteps))
                                            
                                                # Allow user to input a specific elevation based on the best match index
                                                specificElevation = step_elevation_reversed[best_match_index]
                                            
                                                # Generate the binary mask and calculate the area for the selected elevation
                                                maskForSpecificElevation, specificArea = createMaskForElevation(specificElevation, lakeBottom, resolution)
                                                                                
                                                # Load NDWI image and bathymetry mask
                                                ndwi_dataset = rasterio.open(path_ndwi)  # Path to NDWI image
                                                ndwi_crs = ndwi_dataset.crs
                                                ndwi_transform = ndwi_dataset.transform
                                                ndwi_res = ndwi_dataset.res
                                            
                                                # Ensure the mask for the specific elevation is reprojected to the NDWI's CRS, extent, and resolution
                                                mask_for_elevation_reprojected = np.empty_like(ndwi_dataset.read(1))
                                            
                                                reproject(
                                                    source=maskForSpecificElevation,  # Mask to reproject
                                                    destination=mask_for_elevation_reprojected,
                                                    src_transform=lake_transform,  # Transform from the bathymetry mask
                                                    src_crs=lake_crs,  # CRS of the mask
                                                    dst_transform=ndwi_transform,  # NDWI transform
                                                    dst_crs=ndwi_crs,  # NDWI CRS
                                                    resampling=Resampling.nearest  # Nearest neighbor interpolation for binary masks
                                                )
                                            
                                                # Now overlay the NDWI image with the mask
                                                ndwi_image = ndwi_dataset.read(1)  # Read the NDWI image (band 1)
                                            
                                                # Assign value 1 to NDWI where mask is 1
                                                ndwi_image[mask_for_elevation_reprojected == 0] = 1
                                                                                    
                                                # Save the NDWI image locally as a GeoTIFF
                                                output_path = '/Users/joaopimenta/Desktop/GEE_test/reconstructed_plygon.tif'  # Define the output path for the saved image
                                            
                                                # Retrieve the metadata from the NDWI dataset to use it for saving the file
                                                meta = ndwi_dataset.meta.copy()
                                            
                                                # Update metadata for a single band output
                                                meta.update({
                                                    'dtype': 'float32',  # or 'uint8' depending on the NDWI data type
                                                    'count': 1,          # Number of bands
                                                    'driver': 'GTiff',   # Save as a GeoTIFF file
                                                    'crs': ndwi_crs,     # Coordinate reference system
                                                    'transform': ndwi_transform  # Affine transform for georeferencing
                                                })
                                            
                                                # Save the NDWI image with the mask applied as a GeoTIFF
                                                with rasterio.open(output_path, 'w', **meta) as dst:
                                                    dst.write(ndwi_image.astype('float32'), 1)  # Write the NDWI data to band 1
                                                    print(f'Saved NDWI image as {output_path}')
                                            
                                                # Create a figure with 2 subplots side by side
                                                fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns
                                            
                                                # Plot the first contour: Identified contour (K-means method) on binary_ndwi
                                                contour_image_binary = np.zeros_like(binary_ndwi)
                                                contours_binary, _ = cv2.findContours(binary_ndwi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                                if contours_binary:
                                                    cv2.drawContours(contour_image_binary, [max(contours_binary, key=cv2.contourArea)], -1, (255), 2)
                                            
                                                axes[0].imshow(contour_image_binary, cmap='gray')
                                                axes[0].set_title('Polygon of the NDWI affected by clouds')
                                            
                                                # Plot the second contour: Identified contour (K-means method) on ndwi_image
                                                contour_image_ndwi = np.zeros_like(ndwi_image)
                                                contours_ndwi, _ = cv2.findContours(ndwi_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                                if contours_ndwi:
                                                    cv2.drawContours(contour_image_ndwi, [max(contours_ndwi, key=cv2.contourArea)], -1, (255), 2)
                                            
                                                axes[1].imshow(contour_image_ndwi, cmap='gray')
                                                axes[1].set_title('Polygon of the reconstructed Image')
                                            
                                                # Show the plots
                                                plt.tight_layout()
                                                plt.show()
                                                                                    
                                                # Create contour image for binary NDWI
                                                contour_image_binary = np.zeros_like(binary_ndwi)
                                                contours_binary, _ = cv2.findContours(binary_ndwi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                                if contours_binary:
                                                    cv2.drawContours(contour_image_binary, [max(contours_binary, key=cv2.contourArea)], -1, (255), 2)
                                            
                                                # Create contour image for NDWI image
                                                contour_image_ndwi = np.zeros_like(ndwi_image)
                                                contours_ndwi, _ = cv2.findContours(ndwi_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                                if contours_ndwi:
                                                    # Draw only the largest contour for the NDWI image
                                                    largest_contour = max(contours_ndwi, key=cv2.contourArea)
                                                    cv2.drawContours(contour_image_ndwi, [max(contours_ndwi, key=cv2.contourArea)], -1, (255), 2)
                                            
                                                # Stack the binary contour and NDWI contour into a 3-channel image for overlay (Red, Green, Blue)
                                                overlay_image = np.zeros((contour_image_binary.shape[0], contour_image_binary.shape[1], 3), dtype=np.uint8)
                                                overlay_image[..., 0] = contour_image_binary  # Red channel for binary NDWI contour
                                                overlay_image[..., 1] = contour_image_ndwi    # Green channel for NDWI image contour
                                            
                                                # Create a mask to fill the inside of the largest NDWI contour
                                                mask = np.zeros_like(ndwi_image, dtype=np.uint8)
                                                if contours_ndwi:
                                                    cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
                                            
                                                # Create a new output image, initialized to zeros (0 for a black image)
                                                output_image = np.zeros_like(ndwi_image, dtype=np.uint8)
                                            
                                                # Set the inside of the largest contour to one (255)
                                                output_image[mask == 255] = 1  # Change to fill with pixel value 1
                                            
                                                # Optionally convert to uint8 range for visualization
                                                output_image *= 255  # If you need the output image to be in the 0-255 range
                                                
                                                # Save the NDWI image locally as a GeoTIFF
                                                output_path = '/Users/joaopimenta/Desktop/GEE_test/reconstructed_water_mask.tif'  # Define the output path for the saved image
                                            
                                                # Retrieve the metadata from the NDWI dataset to use it for saving the file
                                                meta = ndwi_dataset.meta.copy()
                                            
                                                # Update metadata for a single band output
                                                meta.update({
                                                    'dtype': 'float32',  # or 'uint8' depending on the NDWI data type
                                                    'count': 1,          # Number of bands
                                                    'driver': 'GTiff',   # Save as a GeoTIFF file
                                                    'crs': ndwi_crs,     # Coordinate reference system
                                                    'transform': ndwi_transform  # Affine transform for georeferencing
                                                })
                                            
                                                # Save the NDWI image with the mask applied as a GeoTIFF
                                                with rasterio.open(output_path, 'w', **meta) as dst:
                                                    dst.write(output_image.astype('float32'), 1)  # Write the NDWI data to band 1
                                                    print(f'Saved NDWI image as {output_path}')
                                                                                    
                                                # If resolution is a tuple (x_resolution, y_resolution)
                                                x_resolution, y_resolution = resolution
                                                pixel_area = x_resolution * y_resolution  # Area of one pixel in square meters
                                            
                                                # Count water pixels
                                                water_pixels = ndwi_image > 0
                                                water_pixel_count = np.sum(water_pixels)
                                            
                                                # Calculate total water area
                                                total_water_area = water_pixel_count * pixel_area*1e8
                                            
                                                # Print the result
                                                print(f'Total water area: {total_water_area} square meters')
                                                water_area_info.append(total_water_area)
                                                # Optionally, save the modified NDWI image as a new file
                                                out_meta = ndwi_dataset.meta.copy()
                                                with rasterio.open('ndwi_with_elevation_mask.tif', 'w', **out_meta) as dst:
                                                    dst.write(ndwi_image, 1)  # Write the new image to disk
                                            
                                                # Close datasets
                                                ndwi_dataset.close()
                                            else:
                                                print("There are no cloud pixels inside the reservoir's area.")
                                                water_area_info.append(waterarea)
                                                                                
                                    st.write(water_area_info)
                                else:                                    
                                        # Options for confirming the reservoir selection
                                        water_method = ['Fixed thershold', 'Dynamic']
       
                                        # Select box to confirm selection
                                        water = st.selectbox("Choose this method of identifying water pixels", water_method)
                                        
                                        def extract_bbox_from_aoi(aoi):
                                            # Get the bounding box of the AOI
                                            bounds = aoi.bounds().getInfo()
                                            
                                            # Extract the coordinates based on the observed structure
                                            try:
                                                lon_min = bounds['coordinates'][0][0][0]  # First point's longitude
                                                lat_min = bounds['coordinates'][0][0][1]  # First point's latitude
                                                lon_max = bounds['coordinates'][0][2][0]  # Third point's longitude
                                                lat_max = bounds['coordinates'][0][2][1]  # Third point's latitude
                                        
                                                return lat_min, lon_min, lat_max, lon_max
                                            except (IndexError, KeyError, TypeError):
                                                print("Unexpected bounds structure:", bounds)
                                                raise ValueError("Unable to extract bounding box; check structure of bounds data.")

                                        lat_min, lon_min, lat_max, lon_max = extract_bbox_from_aoi(roi)
                                                                                
                                        # Function to query bridges
                                        def check_bridge_in_area(lat_min, lon_min, lat_max, lon_max):
                                            overpass_url = "http://overpass-api.de/api/interpreter"
                                            overpass_query = f"""
                                            [out:json];
                                            (
                                              way["man_made"="bridge"]({lat_min},{lon_min},{lat_max},{lon_max});
                                              node(w);
                                            );
                                            out body qt;
                                            """
                                            
                                            print(f"Querying Overpass API with:\n{overpass_query}")
                                            
                                            response = requests.get(overpass_url, params={'data': overpass_query})
                                            
                                            if response.status_code == 200:
                                                print("Received response from Overpass API.")
                                                return response.json()
                                            else:
                                                print(f"Error: {response.status_code}")
                                                return None
                                        
                                        # Query the Overpass API for bridges in the bounding box
                                        bridge_data = check_bridge_in_area(lat_min, lon_min, lat_max, lon_max)
                                        
                                        # Initialize lists for GeoDataFrame
                                        bridge_names = []
                                        elem = None
                                        # Parse and display bridges with their shapes and names
                                        if bridge_data and 'elements' in bridge_data:
                                            node_coords = {  # Store node coordinates for reference
                                                int(node['id']): (node['lat'], node['lon'])
                                                for node in bridge_data['elements']
                                                if node['type'] == 'node'
                                            }
                                            
                                            if len(node_coords) > 0:
                                                print(f"Node coordinates found: {node_coords}")
                                            else:
                                                print("No node coordinates found.")
                                            
                                            for element in bridge_data['elements']:
                                                if element['type'] == 'way':
                                                    elem = element['type']
                                                    bridge_name = element.get('tags', {}).get('name')
                                                    if bridge_name:  # Check if bridge has a name
                                                        st.write(f"It was detected the bridge {bridge_name} inside the ROI")
                                                        coords = [node_coords.get(node_id) for node_id in element.get('nodes', [])]
                                                        coords = [coord for coord in coords if coord is not None]  # Remove invalid coordinates
                                                    else:                                    
                                                        st.write(f"Bridge ID: {element['id']} has no name and will be excluded.")
                                        else:
                                            st.write("No bridge data or 'elements' not in the response.")
                                        
                                        if water == 'Fixed thershold':
                                            # Define a function to calculate NDWI and mask for each image
                                            def calculate_ndwi_and_mask(image):
                                                ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
                                                ndwi_threshold = ndwi.gte(0.0)
                                                ndwi_mask = ndwi_threshold.updateMask(ndwi_threshold)
                                                return ndwi_mask
    
                                            # Map the function over the image collection to get NDWI masks for each image
                                            ndwi_masks = sentinelImageCollection.map(calculate_ndwi_and_mask)
    
                                            # Perform erosion (shrinking the mask slightly to remove small gaps and noise)
                                            eroded_ndwi = ndwi_masks.map(lambda img: img.focal_min(radius=1, kernelType='circle', iterations=1))
                                            
                                            # Perform dilation after erosion (expanding the mask back to restore shape)
                                            closed_ndwi = eroded_ndwi.map(lambda img: img.focal_max(radius=1, kernelType='circle', iterations=1))
                                            # Now, closed_ndwi contains the NDWI masks that have been eroded and then dilated for each image in the collection.
    
                                            # Define a function to calculate water area
                                            def calculate_water_area(image):
                                                water_area = image.multiply(ee.Image.pixelArea()).reduceRegion(
                                                    reducer=ee.Reducer.sum(),
                                                    geometry=roi,
                                                    bestEffort=True,
                                                    scale=5
                                                ).get('NDWI')
                                                return image.set('water_area', water_area)
                                            
                                            if elem is not None:
                                                # Map the function over the NDWI masks to calculate water area for each image
                                                ndwi_masks_with_area = closed_ndwi.map(calculate_water_area)
                                            else:    
                                                # Map the function over the NDWI masks to calculate water area for each image
                                                ndwi_masks_with_area = ndwi_masks.map(calculate_water_area)
    
                                            # Get the water area information
                                            water_area_info = ndwi_masks_with_area.aggregate_array('water_area').getInfo()
                                            
                                            # Display the list of water areas
                                            #st.write(water_area_info)
                                            
                                            # Get acquisition dates in human-readable format
                                            dates = ndwi_masks_with_area.aggregate_array('system:time_start') \
                                                .map(lambda d: ee.Date(d).format('YYYY-MM-dd')).getInfo()
                                            
                                            # Display the dates
                                            #st.write("Acquisition dates for each image:", dates)
                                            
                                            # Alternatively, convert acquisition times to readable format (if needed)
                                            acquisition_times = sentinelImageCollection.aggregate_array('system:time_start').getInfo()
                                            acquisition_dates = [datetime.datetime.utcfromtimestamp(time / 1000).strftime('%Y-%m-%d') for time in acquisition_times]
                                            #st.write("Alternative acquisition dates:", acquisition_dates)
     
                                        else:
                                             # Define a function to calculate NDWI
                                            def calculate_ndwi(image):
                                                ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
                                                return image.addBands(ndwi)
     
                                            # Define a function to sample NDWI values for clustering
                                            def sample_ndwi(image):
                                                ndwi = image.select('NDWI')
                                                sampled_ndwi = ndwi.sample(
                                                    region=roi_geometry,
                                                    scale=10,
                                                    numPixels=10000,
                                                    seed=0
                                                ).select('NDWI')
                                                return sampled_ndwi
     
                                            # Define a function to perform K-means clustering
                                            def cluster_ndwi(sampled_ndwi):
                                                clusterer = ee.Clusterer.wekaKMeans(2).train(sampled_ndwi)
                                                return clusterer
     
                                            # Define a function to determine the water cluster
                                            def get_water_cluster(clustered_image):
                                                mean_ndwi_per_cluster = clustered_image.reduceRegion(
                                                    reducer=ee.Reducer.mean(),
                                                    geometry=roi_geometry,
                                                    scale=10
                                                )
                                                mean_values = ee.List(mean_ndwi_per_cluster.values())
                                                water_cluster = mean_values.indexOf(mean_values.reduce(ee.Reducer.max()))
                                                return water_cluster
     
                                            # Define a function to create a binary water mask based on the cluster
                                            def create_water_mask(clustered_image, water_cluster):
                                                water_mask = clustered_image.eq(water_cluster).rename('water_mask')
                                                return water_mask
     
                                            # Define a function to compute the area of water bodies in square meters
                                            def compute_water_area(water_mask):
                                                water_area = water_mask.reduceRegion(
                                                    reducer=ee.Reducer.sum(),
                                                    geometry=roi_geometry,
                                                    scale=10
                                                ).get('water_mask')
                                                water_area = ee.Number(water_area).multiply(100).divide(1e4)  # Convert to square kilometers
                                                return water_area
                                            
                                            if elem is not None:
                                                # Combine all functions into one for mapping
                                                def process_image(image):
                                                    # Calculate NDWI
                                                    image = calculate_ndwi(image)
                                                    
                                                    # Sample and cluster NDWI for water detection
                                                    sampled_ndwi = sample_ndwi(image)
                                                    clusterer = cluster_ndwi(sampled_ndwi)
                                                    clustered_image = image.select('NDWI').cluster(clusterer).rename('cluster')
                                                    
                                                    # Determine which cluster represents water
                                                    water_cluster = get_water_cluster(clustered_image)
                                                    water_mask = create_water_mask(clustered_image, water_cluster)
                                                    
                                                    # Perform morphological operations (closing)
                                                    eroded_ndwi = water_mask.focal_min(radius=1, kernelType='circle', iterations=1)
                                                    closed_ndwi = eroded_ndwi.focal_max(radius=1, kernelType='circle', iterations=1)
                                                    
                                                    water_area = compute_water_area(closed_ndwi)
                                                    
                                                    return image.set('water_area_km2', water_area)
                                            else:
                                                # Combine all functions into one for mapping
                                                def process_image(image):
                                                    image = calculate_ndwi(image)
                                                    sampled_ndwi = sample_ndwi(image)
                                                    clusterer = cluster_ndwi(sampled_ndwi)
                                                    clustered_image = image.select('NDWI').cluster(clusterer).rename('cluster')
                                                    water_cluster = get_water_cluster(clustered_image)
                                                    water_mask = create_water_mask(clustered_image, water_cluster)
                                                    water_area = compute_water_area(water_mask)
                                                    
                                                    return image.set('water_area_km2', water_area)
         
                                            # Apply the processing function to each image in the collection
                                            processed_images = sentinelImageCollection.map(process_image)
     
                                            # Extract the water area and date information
                                            water_area_info = processed_images.aggregate_array('water_area_km2').getInfo()
                                            dates = processed_images.aggregate_array('system:time_start').map(lambda d: ee.Date(d).format('YYYY-MM-dd')).getInfo()
                                            
                                            # Get acquisition times of the images
                                            acquisition_times = sentinelImageCollection.aggregate_array('system:time_start').getInfo()
     
                                            # Convert acquisition times to human-readable dates
                                            acquisition_dates = [datetime.datetime.utcfromtimestamp(time / 1000).strftime('%Y-%m-%d') for time in acquisition_times]
                                                 
                            if method == ("Write the A-V function of your reservoir"):
                                                            
                                                        for area in water_area_info:
                                                            volume = None
                                                            # Calculate the volume using the area-storage equation
                                                            volume = (area / a) ** (1 / b)
                                                            
                                                            if volume is not None:
                                                                volumes.append(volume)
                                                            else:
                                                                st.write("Error with the coefficients")
                                                                                                                      
                                                        st.write(f"The list of the volumes in cubic meters for the chosen dates is: {volumes}")
                                                        
                            elif method == ("upload excel sheet"):
                                                            
                                                            if dictionary:
                                                               for area in water_area_info:
                                                                    volume = None
                                                                    keys = sorted(dictionary.keys())
                                                                    for i in range(len(keys)):
                                                                        key = keys[i]
                                                                        if key >= area:
                                                                            if i == 0:
                                                                                volume = dictionary[key]
                                                                                st.write(f"This is the volume {volume/10**6}km³")
                                                                                volumes.append(volume)
                                                                            else:
                                                                                prev_key = keys[i - 1]
                                                                                delta_volume = dictionary[key] - dictionary[prev_key]
                                                                                delta_key = key - prev_key
                                                                                delta_area = area - prev_key
                                                                                interpolated_volume = dictionary[prev_key] + (delta_volume * delta_area / delta_key)
                                                                                volume = (interpolated_volume/10**6)
                                                                                st.write(f"This is the volume {volume}km³")
                                                                                volumes.append(volume)
                                                                            break
                                                            else:
                                                                  # This else block belongs to the for loop, not the if condition
                                                                 st.write("Dam value not found in the dictionary ")
                            elif method == ("upload the DEM"):
                                                            
                                                            if dictionary:
                                                               for area in water_area_info:
                                                                    volume = None
                                                                    keys = sorted(dictionary.keys())
                                                                    for i in range(len(keys)):
                                                                        key = keys[i]
                                                                        if key >= area:
                                                                            if i == 0:
                                                                                volume = dictionary[key]
                                                                                st.write(f"This is the volume {volume/10**6}km³")
                                                                                volumes.append(volume)
                                                                            else:
                                                                                prev_key = keys[i - 1]
                                                                                delta_volume = dictionary[key] - dictionary[prev_key]
                                                                                delta_key = key - prev_key
                                                                                delta_area = area - prev_key
                                                                                interpolated_volume = dictionary[prev_key] + (delta_volume * delta_area / delta_key)
                                                                                volume = (interpolated_volume/10**6)
                                                                                st.write(f"This is the volume {volume}km³")
                                                                                volumes.append(volume)
                                                                            break
                                                            else:
                                                                  # This else block belongs to the for loop, not the if condition
                                                                 st.write("Dam value not found in the dictionary ")                                 
                            elif method == "Don't have that info":
                                                                                                    
                                                    import netCDF4 as nc
                                                    import numpy as np
                                                    
                                                    volumes =[]
                                                    # Open the NetCDF file
                                                    nc_file = nc.Dataset('/Users/joaopimenta/Downloads/Master thesis/GLOBathy_hAV_relationships.nc')
                                                    
                                                    # Specify the lake ID you want to search for
                                                    target_lake_id = hydrolakes_id  # Replace this with the actual lake ID you're interested in
                                                                                                                    
                                                    # Find the index of the lake based on the lake ID
                                                    lake_ids = nc_file.variables['lake_id'][:]
                                                    
                                                    # Check if the target lake ID exists in the lake_id variable
                                                    lake_index = np.where(lake_ids == target_lake_id)[0]
                                                    
                                                    if len(lake_index) == 0:
                                                        st.write("Lake not found in the dataset.")
                                                    else:
                                                        lake_index = lake_index[0]  # Use the first match if found
                                                    
                                                        # Extract coefficients of the area-storage equation for the identified lake
                                                        area_storage_coeffs = nc_file.variables['f_hA'][lake_index, :]
                                                        lon_lat = nc_file.variables['lon_lat'][lake_index, :]
                                                    
                                                        # Print the lake's ID, coordinates, and area-storage equation coefficients
                                                        st.write("Coordinates (Lon, Lat):", lon_lat)
                                                        # Print the coefficients
                                                        st.write("Area-Storage equation coefficients:")
                                                        st.write("a:", area_storage_coeffs[0])
                                                        st.write("b:", area_storage_coeffs[1])
                                                        st.write("R^2:", area_storage_coeffs[2])
                                                        import numpy as np
                                                        
                                                        for area in water_area_info:
                                                              
                                                            # Coefficients obtained from the NetCDF dataset
                                                            a = area_storage_coeffs[0]
                                                            b = area_storage_coeffs[1]
     
                                                            # Calculate the volume using the area-storage equation
                                                            volume = ((area/1e6) / a) ** (1 / b)
                                                            volumes.append(volume)
                                                                    
                                                                                                                                  
                            from io import BytesIO                                
                            # Function to generate the sample data DataFrame
                            def generate_sample_data():
                                date = acquisition_dates 
                                area = water_area_info  
                                vol = volumes 
                                return pd.DataFrame({'Date': date, 'Volume (10⁸m³)': vol, 'Area (km²)': area })
                       
                            # Generate the sample data DataFrame
                            df = generate_sample_data()
                            
                            # Save the DataFrame to an Excel file in memory
                            excel_buffer = BytesIO()
                            
                            import pandas as pd
                            import io
                            
                            # Assuming excel_buffer and output, area_storage_coeffs are defined elsewhere in your code
                            excel_buffer = io.BytesIO()
                            
                            # Use a single `ExcelWriter` for writing all sheets
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                # Check if 'Water Surface Elevation' is in output and write relevant data
                                if 'Water Surface Elevation' in output:
                                    # Convert date to timezone-unaware if necessary
                                    elevation_dates = pd.to_datetime(df_filtered['time_str']).dt.tz_localize(None)
                                    elevations = df_filtered['wse']
                                    df_2 = pd.DataFrame({'Date': elevation_dates, 'Water Surface Elevations': elevations})
                                    df_2.to_excel(writer, sheet_name='Elevations Data', index=False)
                                
                                # Check if 'Storage-Capacity curve' is in output and write relevant data
                                if 'Storage-Capacity curve' in output:
                                    # Assume `area_storage_coeffs` contains appropriate data in tuple or list format
                                    df_3 = pd.DataFrame({
                                        'a': [area_storage_coeffs[0]],
                                        'b': [area_storage_coeffs[1]],
                                        'R^2': [area_storage_coeffs[2]]
                                    })
                                    df_3.to_excel(writer, sheet_name='Storage_capacity_curve', index=False)
                                
                                # Assuming `df` is a base DataFrame you want to write to a default sheet
                                df.to_excel(writer, sheet_name='Reservoir Data', index=False)
                            
                            # Reset buffer position to the start for reading/download
                            excel_buffer.seek(0)
                            # Create a download button for the Excel file
                            st.download_button(
                                label="Download Excel file",
                                data=excel_buffer,
                                file_name="reservoir_data.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
                            st.write("Click the button above to download the data as an Excel file.")
                            
                            import tempfile
                            
                            # Load the bathymetry dataset from Earth Engine
                            globathy = ee.Image("projects/sat-io/open-datasets/GLOBathy/GLOBathy_bathymetry")
                            # Define the function to export the image and return the path
                            def export_image_for_download(image, roi, scale=10):
                                # Use a temporary directory for saving the file
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as temp_file:
                                    out_image_path = temp_file.name
                                    geemap.ee_export_image(image, filename=out_image_path, scale=scale, region=roi)
                                return out_image_path
                            
                            
                            if 'Bathymetry file' in output:
                                # Call the function and set up the download button
                                if st.button("Download Image"):
                                    # Assuming `globathy` is your Earth Engine image and `roi` is the region of interest
                                    image_path = export_image_for_download(globathy, roi)
                                    
                                    # Read the file as bytes for download
                                    with open(image_path, "rb") as file:
                                        file_bytes = file.read()
                                        st.download_button(
                                            label="Click here to download the image",
                                            data=file_bytes,
                                            file_name="exported_image.tif",
                                            mime="image/tiff"
                                        )

                             # Display the bar charts
                            col1, col2= st.columns([7,3])
                             # Combine acquisition dates and volumes into a list of tuples
                            with col1:
                                 
                                 import pandas as pd
                                 import altair as alt
                                 # Function to generate sample data
                                 def generate_sample_data():
                                     date = acquisition_dates
                                     vol= volumes
                                     return pd.DataFrame({'Date': date, 'Volume': vol})
                 
                                 # Sample data
                                 df = generate_sample_data()
                                 
                                 if 'Water Surface Elevation' in output:
                                    st.subheader("WSE over the chosen date range")
                                    
                                    # Convert 'time_str' to timezone-unaware and set up DataFrame for plotting
                                    elevation_dates = pd.to_datetime(df_filtered['time_str']).dt.tz_localize(None)
                                    elevations = df_filtered['wse']
                                    df_wse = pd.DataFrame({'Date': elevation_dates, 'Water Surface Elevations': elevations})
                                    
                                    # Create the line chart for water surface elevations
                                    wse_chart = alt.Chart(df_wse).mark_line(
                                        color='#00FFFF'
                                    ).encode(
                                        x=alt.X('Date:T', title='Date'),
                                        y=alt.Y('Water Surface Elevations:Q', title='Water Surface Elevation (m)')
                                    )
                                    
                                    # Display the WSE chart in Streamlit
                                    st.altair_chart(wse_chart, use_container_width=True)
                                
                                 st.subheader("Volume over the chosen date range")
                                
                                # Ensure that 'Date' and 'Volume' columns are available in df
                                 volume_chart = alt.Chart(df).mark_line(
                                    color='#00FFFF'
                                 ).encode(
                                    x=alt.X('Date:T', title='Date'),
                                    y=alt.Y('Volume:Q', title='Volume (10⁶ m³)',scale=alt.Scale(zero=False))
                                 )
                                
                                 # Display the volume chart in Streamlit
                                 st.altair_chart(volume_chart, use_container_width=True)
                            with col2:
                                 
                                 import pandas as pd
                                 # Donut chart function
                                 def make_donut(input_response, input_text, input_color):
                                     if input_color == 'green':
                                         chart_color = ['#27AE60', '#12783D']
                                     elif input_color == 'red':
                                         chart_color = ['#E74C3C', '#781F16']
                                     elif input_color == 'yellow':
                                         chart_color = ['#FFFF00', '#FFD700']  # Yellow colors
                                     elif input_color == 'orange':
                                         chart_color = ['#FFA500', '#FF4500']  # Orange colors
                                     elif input_color == 'light green':
                                         chart_color = ['#90EE90', '#006400']  # Light green colors
                                     else:
                                         raise ValueError("Invalid color. Please choose either 'green' or 'red'.")
                 
                                     source = pd.DataFrame({
                                         "Topic": ['', input_text],
                                         "% value": [100-input_response, input_response]
                                     })
                                     source_bg = pd.DataFrame({
                                         "Topic": ['', input_text],
                                         "% value": [100, 0]
                                     })
                 
                                     plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
                                         theta="% value",
                                         color=alt.Color("Topic:N",
                                                         scale=alt.Scale(
                                                             domain=[input_text, ''],
                                                             range=chart_color),
                                                         legend=None),
                                     ).properties(width=130, height=130)
                 
                                     text = plot.mark_text(align='center', color=chart_color[0], font="sans-serif", fontSize=20, fontWeight=500, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
                 
                                     plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
                                         theta="% value",
                                         color=alt.Color("Topic:N",
                                                         scale=alt.Scale(
                                                             domain=[input_text, ''],
                                                             range=chart_color),  # 31333F
                                                         legend=None),
                                     ).properties(width=130, height=130)
                 
                                     return plot_bg + plot + text
                                          
                                 
                                 def get_color(value):
                                    """Helper function to determine the color based on percentage."""
                                    if value < 25:
                                        return 'red'
                                    elif 25 <= value < 50:
                                        return 'orange'
                                    elif value == 50:
                                        return 'yellow'
                                    elif 50 < value < 75:
                                        return 'light green'
                                    else:
                                        return 'green'
                                
                                # Check if storage is not None, not an empty string, and can be converted to a float
                                 if Vol_res is not None:
                                    try:
                                        storage_float = Vol_res/10
                                        if storage_float > 0:                                                
                                            total_volume = storage_float
                                            worst = (min(volumes) / total_volume) * 100
                                            best = (max(volumes) / total_volume) * 100
                                
                                            # Colors for worst and best day
                                            wrst_color = get_color(worst)
                                            bst_color = get_color(best)
                                
                                            # Display donut charts
                                            st.subheader("Lower storage")
                                            st.altair_chart(make_donut(round(worst, 2), 'Worst day', wrst_color), use_container_width=True)
                                
                                            st.subheader("Higher storage")
                                            st.altair_chart(make_donut(round(best, 2), 'Best day', bst_color), use_container_width=True)
                                    except ValueError:
                                        st.write("Invalid storage value; cannot convert to float.")
                                
                                # Fallback if storage is invalid or not provided, and ref_area is available
                                 elif properties and ref_area is not None:
                                    ref_area_float = (float(ref_area)*1e6)
                                    worst = (min(water_area_info) / ref_area_float) * 100
                                    best = (max(water_area_info) / ref_area_float) * 100
                                
                                    # Colors for worst and best day
                                    wrst_color = get_color(worst)
                                    bst_color = get_color(best)
                                
                                    # Display fallback donut charts
                                    st.subheader("Lower storage")
                                    st.altair_chart(make_donut(round(worst, 2), 'Worst day', wrst_color), use_container_width=True)
                                
                                    st.subheader(" Higher storage")
                                    st.altair_chart(make_donut(round(best, 2), 'Best day', bst_color), use_container_width=True)
                         
                            def calculate_max_percentage_variation(volumes, acquisition_dates):
                                 max_variation = 0
                                 max_variation_index = None
                 
                                 for i in range(1, len(volumes)):
                                     # Calculate percentage variation
                                     percentage_variation = abs((volumes[i] - volumes[i - 1]) / volumes[i - 1]) * 100
                 
                                     # Update max variation and index if current variation is greater
                                     if percentage_variation > max_variation:
                                         max_variation = percentage_variation
                                         max_variation_index = i - 1  # Store index of the first date in the pair
                 
                                 # Get the dates corresponding to the max variation
                                 date1 = acquisition_dates[max_variation_index]
                                 date2 = acquisition_dates[max_variation_index + 1]
                 
                                 return max_variation, date1, date2
                 
                            max_variation, date1, date2 = calculate_max_percentage_variation(volumes, acquisition_dates)
                                         
                            import statistics
                 
                            std_dev = round(statistics.stdev(volumes),2)
                         
                            mean_vol = round(statistics.mean(volumes),2)
                         
                            mean_area = round(statistics.mean(water_area_info),2)
                 
                            max_variation_area, date1, date2 = calculate_max_percentage_variation(water_area_info, acquisition_dates)
                            #st.write(" The greates variation occured between:", date1, "and", date2)
                         
                            if max_variation >=0:
                                delta = 1
                            else:
                                delta = -1
                                                                                               
                            max_area = max(water_area_info)
                            max_volume = max(volumes)
                         
                            current_volume = round(volumes[-1],2)
                            current_area = round(water_area_info[-1],2)
                 
                             #create column span
                            col1, col2, col3 = st.columns(3)
                         
                             #Customize metric style to have white text color
                            metric_style = "color: black;"
                         
                            col1.metric(label="Max variation", value="%" + " " + f"{max_variation:,.2f}", delta=delta)
                            col2.metric(label="Mean area", value="km²" + " " + f"{mean_area/1e6:,.2f}", delta=round(max_variation_area,2))
                            col3.metric(label="standard deviation", value = "km³ " + " " + f"{std_dev:,.2f}")
                            
                            st.write(" The greates variation occured between:", date1, "and", date2)
                    # Create a select box for asking ChatGPT about this reservoir
                    opt = ["No","Yes"]
                    info = st.selectbox(
                       f"Ask ChatGPT more information about this lake {lake_name}",
                       opt,
                       key="info")
                    if info == "Yes":
                        import streamlit as st
                        from openai import OpenAI
                       
                       # Define the reservoir information retrieval function
                        def get_reservoir_info(lake_name, country, lng, lat):
                           client = OpenAI(api_key="sk-proj-uK1IbwMXiNImV7RFDxr3T3BlbkFJXjBzHIIJYRoQbiJE6Kc5")
                       
                           prompt = (
                               f"Provide detailed information about the dam/reservoir {lake_name}, "
                               f"located in {country}, with coordinates (longitude: {lng}, latitude: {lat}). "
                               f"Use short sentences and split the response into concise, clear lines."
                               f"Specify the type of use of that reservoir or lake and when it wast built. "
                           )
                       
                           stream = client.chat.completions.create(
                               model="gpt-3.5-turbo",
                               messages=[{"role": "user", "content": prompt}],
                               stream=True,
                           )
                       
                           response_content = ""
                       
                           for chunk in stream:
                               if chunk.choices[0].delta.content is not None:
                                   response_content += chunk.choices[0].delta.content
                       
                           return response_content
                       
                        st.subheader(f"Information about the reservoir {lake_name}")
                       
                        info_text = get_reservoir_info(lake_name, Country, lng, lat)
                       
                        # Displaying the information with line breaks
                        for line in info_text.split(". "):  # Split into sentences
                           st.text(line.strip() + ".")
                    else:
                        st.write("Please select the date range and cloud coverage thershold for the analysis.")                                                                                                                                                    
    else:
         st.write("Please search on the map the lake you want to analyse and click on it to select it")                               
        
elif page =="About":    

                        from PIL import Image
                        # For handling images
                        # Load images
                        satellite_image = Image.open("/Users/joaopimenta/Desktop/images thesis and figures/Captura de ecrã 2024-08-29, às 18.17.19.png")
                        workflow_diagram = Image.open("/Users/joaopimenta/Downloads/image-Photoroom.png")
                        reservoir_map = Image.open("/Users/joaopimenta/Desktop/images thesis and figures/Captura de ecrã 2024-08-30, às 00.43.24.png")
                        worflow_image = Image.open("/Users/joaopimenta/Desktop/SCR-20241218-bmyx.png")
                        #comparison_graph = Image.open("images/comparison_graph.jpg")
                        #future_advancements = Image.open("images/future_advancements.jpg")
     # Path to your video file
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        st.markdown(" ")
                        
                        st.markdown(
                            """
                            <style>
                            .about-text {
                                font-family: 'Times New Roman', Times, serif;
                                font-size: 40px;
                                line-height: 1.6;
                                max-width: 1000px;
                                margin: 0 auto;
                                text-align: justify;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                        # Content with the "about-text" class for styling
                        st.markdown(
                            """
                            <div class="about-text">
                                <h1>About the Research</h1>
                                <p>
                                Efficient management of water reservoirs is essential for water security, flood control, and hydroelectric power generation. 
                                Traditional methods of evaluating reservoir volumes depend on in-situ measurements and physical surveys, which are often 
                                time-consuming, resource-intensive, and impractical for many regions due to financial and logistical limitations.
                                </p>
                                <p>
                                To address these challenges, this research introduces a novel remote sensing tool designed to provide an accurate, scalable, 
                                and globally accessible method for reservoir volume evaluation. The tool integrates high-resolution Sentinel-2 satellite imagery 
                                with geospatial analysis techniques and machine learning algorithms to automatically calculate inundated areas and reservoir water storage.
                                </p>
                                <p>
                                This problem is both significant and complex. Reservoir volume measurements are critical for effective water resource management, 
                                yet current methodologies struggle to scale for large or remote areas due to high costs. Furthermore, environmental factors such as 
                                cloud cover and human-made structures, like bridges, can interfere with satellite imagery, presenting additional challenges for large-scale 
                                remote sensing. By employing the algorithms developed in this study, the proposed tool overcomes these barriers, delivering flexible 
                                and reliable estimates of reservoir volumes.
                                </p>
                                <p>
                                The solution was tested on reservoirs in Portugal and California, USA, achieving high accuracy. Results showed an average mean absolute 
                                percentage error of <strong>5.35%</strong> and an average correlation coefficient (<strong>R²</strong>) of <strong>0.90</strong> when compared to published data obtained 
                                through traditional methods.
                                </p>
                                <p>
                                This software includes a free demo version designed to allow users to test the tool, with continuous improvements planned. Currently, it utilizes a sample of polygons 
                                from the SWOT lakes database, covering 93% of all lakes across Europe. 
                                Over time, the database will be expanded, incorporating additional data, while also optimizing the website's RAM usage.
                                </p>
                                <p>
                                Beyond the current promising results, this research opens pathways for future enhancements. These include:
                                </p>
                                <ul>
                                    <li>Incorporating additional satellite data sources such as <strong>SWOT</strong> (Surface Water and Ocean Topography)</li>
                                    <li>Updating bathymetric datasets</li>
                                    <li>Integrating predictive <strong>LSTM</strong> (Long Short-Term Memory) models to forecast reservoir volumes under varying climate scenarios</li>
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                             st.image(worflow_image, caption="App description", width=700)
                        st.markdown(
                            """
                            <div class="about-text">
                                <h1>About This Application</h1>
                                <h1>Revolutionizing Water Resource Management</h1>
                                <p>
                                The Reservoir Volume Monitoring Application is a cutting-edge tool designed to address global challenges in water management, flood prevention, and hydroelectric power optimization. By leveraging high-resolution satellite imagery from Sentinel-2 and advanced geospatial analysis, the app automates the estimation of reservoir volumes, delivering accurate, efficient, and globally scalable solutions.This software includes a free demo version designed to allow users to test the tool, with continuous improvements planned. Currently, it utilizes a sample of polygons 
                                from the SWOT lakes database, covering 93% of all lakes across Europe. 
                                Over time, the database will be expanded, incorporating additional data, while also optimizing the website's RAM usage.
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        ) 
                        # Image in the middle column
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                             st.image(satellite_image, caption="Sentinel-2 satellite image of a large reservoir", width=700,)
                        st.markdown(
                            """
                            <div class="about-text">
                                <h1>How It Works</h1>
                                <p>
                                This application simplifies complex workflows into an intuitive and automated process. Users start by selecting a Region of Interest (ROI) using an interactive map or by uploading geojson files. Satellite imagery for the specified area and date range is automatically retrieved and preprocessed. Advanced algorithms remove interferences such as clouds, shadows, or structural obstacles like bridges.
The app applies indices such as NDWI (Normalized Difference Water Index) to classify water pixels and calculate inundated areas. For reservoirs affected by cloud cover, bathymetric data from global databases like GLOBathy is used to reconstruct accurate water surfaces. Finally, volumes are calculated using area-volume relationships derived from either existing databases or user-provided data. The results are visualized through dynamic charts, maps, and downloadable reports, providing users with actionable insights.
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                             st.image(workflow_diagram, caption="Workflow of the app: From data acquisition to volume estimation", width=700)
                        st.markdown(
                            """
                            <div class="about-text">
                                <h1>Why It Matters</h1>
                                <p>
                                Reservoirs are crucial for ensuring water security, supporting agriculture, producing hydroelectric power, and maintaining ecological balance. However, many regions lack efficient monitoring tools, leading to water mismanagement and heightened risks of droughts, floods, and ecological disruption.
This application bridges the gap by offering a globally accessible solution that requires no physical infrastructure. Its scalability enables it to monitor reservoirs of all sizes, from local irrigation ponds to massive hydroelectric reservoirs. With an accuracy of 94.65%, tested on reservoirs in Portugal and California, the app provides reliable data to support decision-making in water management, flood risk mitigation, and ecosystem preservation.
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        ) 
                        
                        st.markdown(
                            """
                            <div class="about-text">
                                <h1>Key Benefits</h1>
                                <p>
                                The application offers a robust yet user-friendly platform that integrates cutting-edge technology into a seamless user experience. Built with Python and the Streamlit framework, it provides:
	•	Automated Image Processing: Reduces manual effort by leveraging advanced algorithms for water surface detection and volume calculation.
	•	Accurate Data Insights: Achieves a mean absolute percentage error of just 5.35%.
	•	Global Scalability: Access anywhere, monitor reservoirs of all sizes, and ensure reliable data even in remote areas.
	•	Environmental Sustainability: Supports efficient water use and better management of natural resources.
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        ) 
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                             st.image(reservoir_map, caption="Tested reservoirs in Portugal and California", width=700)
                        st.markdown(
                            """
                            <div class="about-text">
                                <h1>The Future of Reservoir Monitoring<h1>
                                <p>
                                The application is poised for future enhancements, including integration with new satellite missions like SWOT (Surface Water and Ocean Topography), predictive modeling using LSTM algorithms, and expanded compatibility with emerging geospatial technologies. With its scalable and adaptable design, this tool is set to become an indispensable resource for water resource management professionals, researchers, and environmental advocates.
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        ) 
                        
                        # Contact Section
                        st.header("Contact Me")
                        
                        # Creating three columns
                        col1, col2, col3 = st.columns([1, 2, 1])
                        
                        # Place email in the first column
                        with col1:
                            st.markdown(
                                """
                                **Email:**
                                [joaopedromateusp@gmail.com](mailto:joaopedromateusp@gmail.com)
                                """,
                                unsafe_allow_html=True
                            )
                        
                        # Place GitHub link in the second (middle) column
                        with col2:
                            st.markdown(
                                """
                                **GitHub:**
                                [github.com/yourusername](https://github.com/yourusername)
                                """,
                                unsafe_allow_html=True
                            )
                        
                        # Place LinkedIn link in the third column
                        with col3:
                            st.markdown(
                                """
                                **LinkedIn:**
                                [www.linkedin.com/in/joão-pimenta-mp](www.linkedin.com/in/joão-pimenta-mp)
                                """,
                                unsafe_allow_html=True
                            )
elif page =="Tutorial":    
 
                        st.markdown("""
                        # Tutorial: Analyzing Satellite Imagery and Calculating Reservoir Volumes
                        
                        Welcome to the tutorial for your app, which automates the process of analyzing satellite imagery and calculating the area and volume of reservoirs. This guide will walk you through the steps to use the app effectively.
                        
                        ---
                        
                        ## Step 1: Define the Region of Interest (ROI)
                        
                        1. **Set the Region of Interest (ROI)**  
                           Start by defining the Region of Interest (ROI), which is the geographic area you want to analyze. You can specify this by selecting coordinates or using a map interface to draw a boundary around the reservoir.  
                           **Tip:** You can zoom in and adjust the shape of the ROI for more precise selection.
                        
                        ---
                        
                        ## Step 2: Define the Date Range
                        
                        1. **Select the Date Range**  
                           The next step is to choose a date range for the analysis. You can use the calendar interface within the app to select the start and end dates for the period you wish to analyze.  
                           The app will automatically filter available satellite imagery based on the selected date range and cloud coverage.
                        
                           ### Cloud Coverage Percentage Filter:  
                           The app will display images for the chosen date range and allow you to choose the maximum acceptable percentage of cloud coverage for the images.  
                           **Tip:** To ensure clear images, select a lower cloud coverage threshold (e.g., less than 10%).
                        
                        ---
                        
                        ## Step 3: Confirm the Reservoir Selection
                        
                        1. **Select the Reservoir**  
                           After defining the ROI and setting the date range, the app will retrieve satellite imagery for the region. You will be shown a list of possible reservoirs within the selected area.  
                           Review the options and confirm the specific reservoir you want to analyze.  
                           **Tip:** If the app detects multiple water bodies, it will present thumbnails or maps to help you identify the correct reservoir.
                        
                        ---
                        
                        ## Step 4: Choose the Cloud Coverage Percentage
                        
                        1. **Choose Cloud Coverage Threshold**  
                           You will now select the cloud coverage threshold. The app will show you images with varying levels of cloud coverage.  
                           You can choose a cloud coverage percentage that meets your needs (e.g., less than 10%, 20%, etc.).  
                           **Tip:** For more accurate results, choose a threshold that minimizes the impact of cloud cover on your analysis.
                        
                        ---
                        
                        ## Step 5: Choose the Output Variables
                        
                        1. **Select Output Variables**  
                           Now, you can choose the specific variables you want the app to calculate for the reservoir. These may include:
                           - Water Area
                           - Volume
                           - Time Series Data for Volume
                           - Bathymetric Information  
                           **Tip:** Select the variables you are most interested in, such as volume or changes over time.
                        
                        ---
                        
                        ## Step 6: Press the "Start" Button
                        
                        1. **Start the Analysis**  
                           Once all parameters have been defined (date range, reservoir selection, cloud coverage, and output variables), you can initiate the analysis by pressing the **"Start"** button.  
                           The app will begin processing the satellite imagery, applying necessary corrections, and performing calculations to estimate the reservoir's water area and volume.  
                           **Tip:** Depending on the data size, the process may take a few minutes. You’ll see a progress indicator during this time.
                        
                        ---
                        
                        ## Step 7: View and Export Results
                        
                        1. **View Results**  
                           Once the analysis is complete, you can view the results directly within the app. The app will display visualizations of the water area and provide calculated volume data for the reservoir.
                        
                        2. **Export Data**  
                           You can export the analysis results in CSV, Excel, or other formats for further analysis or reporting. Simply click the "Export" button to download the data.
                        
                        ---
                        
                        ## Notes
                        
                        1. **Fill the parameters**
                           In order for the software to compute the water analysis all the paremeters must have been adressed
                           
                        2. **Statistics**  
                           Note that 'higher percentage' and 'lower percentage' values are calulated based on the maxiumum and minum water volume value from the calculated time series comparing with the maximum water volume present on the SWOT lakes database for that specific reservoir
                        
                        ---
                        
                        ## Conclusion
                        
                        By following these steps, you can efficiently analyze satellite imagery and calculate reservoir volumes using the app. The methodology ensures accurate results with cloud coverage filtering, error checking, and reliable bathymetric analysis.
                        
                        If you encounter any issues or need further assistance, refer to the help section within the app or contact support.
                        """)
                        video_file = open('/Users/joaopimenta/Desktop/Gravação do ecrã 2024-11-08, às 00.40.22.mov', "rb")
                        video_bytes = video_file.read()
                        
                        st.video(video_bytes)
                                                
                        # For handling images
