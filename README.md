# BLU
Blu is a reservoirs monitoring platform built with Streamlit framework to allow calculate the volume of reservoirs worldwide using remote sensing
![Workflow of the app: From data acquisition to volume estimation](https://github.com/joao862/BLU/blob/main/app.png)

## About the Research
Efficient management of water reservoirs is critical for water security, flood control, and hydroelectric power generation. Traditional methods for evaluating reservoir volumes rely on in-situ measurements and physical surveys, which are often time-consuming, resource-intensive, and impractical for many regions due to financial and logistical limitations.

To address these challenges, this research introduces a novel remote sensing tool that provides an accurate, scalable, and globally accessible method for reservoir volume evaluation. By integrating high-resolution Sentinel-2 satellite imagery with geospatial analysis techniques and machine learning algorithms, the tool automatically calculates inundated areas and reservoir water storage. 

Key results from testing on reservoirs in Portugal and California, USA, demonstrated an average mean absolute percentage error of **5.35%** and an average correlation coefficient (**R²**) of **0.90**, showcasing the tool's reliability compared to traditional methods.

## About This Application
The **Reservoir Volume Monitoring Application** is a cutting-edge solution designed to tackle global challenges in water management, flood prevention, and hydroelectric power optimization. By leveraging Sentinel-2 satellite imagery and advanced geospatial analysis, the app automates the estimation of reservoir volumes, offering accurate, efficient, and globally scalable solutions.

This software includes a free demo version for users to test the tool. It currently uses a sample of polygons from the SWOT lakes database, covering 93% of lakes across Europe. Future updates will expand the database, improve performance, and optimize memory usage.

## How It Works
This application simplifies complex workflows into an intuitive and automated process:
1. **Select a Region of Interest (ROI):** Choose using an interactive map or upload geojson files.
2. **Retrieve Satellite Imagery:** Automatically fetch Sentinel-2 data for the specified area and date range.
3. **Preprocess Data:** Remove interferences like clouds, shadows, or structural obstacles such as bridges.
4. **Classify Water Pixels:** Use indices like NDWI (Normalized Difference Water Index) to classify water pixels and calculate inundated areas.
5. **Reconstruct Water Surfaces:** For cloud-covered reservoirs, use bathymetric data from global databases like GLOBathy.
6. **Calculate Volumes:** Derive area-volume relationships from databases or user-provided data.

The results are visualized through dynamic charts, maps, and downloadable reports, providing actionable insights.

## Why It Matters
Reservoirs are essential for water security, agriculture, hydroelectric power, and ecological balance. Many regions, however, lack efficient monitoring tools, leading to mismanagement and increased risks of droughts, floods, and ecological disruption. This application bridges the gap by offering a globally accessible solution that requires no physical infrastructure. 

With an accuracy of **94.65%**, tested on reservoirs in Portugal and California, the app provides reliable data to support decision-making in water management, flood risk mitigation, and ecosystem preservation.

## Key Benefits
- **Automated Image Processing:** Reduces manual effort using advanced algorithms for water surface detection and volume calculation.
- **Accurate Data Insights:** Achieves a mean absolute percentage error of just **5.35%**.
- **Global Scalability:** Monitors reservoirs of all sizes, even in remote areas.
- **Environmental Sustainability:** Supports efficient water use and resource management.

## The Future of Reservoir Monitoring
Future enhancements include:
- Integration with new satellite missions like **SWOT** (Surface Water and Ocean Topography).
- Predictive modeling using **LSTM** algorithms to forecast reservoir volumes under varying climate scenarios.
- Expanded compatibility with emerging geospatial technologies.

With its scalable and adaptable design, this tool aims to become an indispensable resource for water resource management professionals, researchers, and environmental advocates.

## Workflow Overview
![Workflow of the app: From data acquisition to volume estimation](https://github.com/joao862/BLU/blob/main/workflow.png)

## Contact Me
If you have any questions or want to collaborate, feel free to reach out:

- **Email:** [joaopedromateusp@gmail.com](mailto:joaopedromateusp@gmail.com)
- **GitHub:** [github.com/yourusername](https://github.com/yourusername)
- **LinkedIn:** [www.linkedin.com/in/joão-pimenta-mp](https://www.linkedin.com/in/jo%C3%A3o-pimenta-mp)

                        ---
Conclusion
By following these steps, you can efficiently analyze satellite imagery and calculate reservoir volumes using the app. The methodology ensures accurate results with cloud coverage filtering, error checking, and reliable bathymetric analysis.
If you encounter any issues or need further assistance, refer to the help section within the app or contact support.
