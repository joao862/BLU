# BLU
Blu is a reservoirs monitoring platform built with Streamlit framework to allow calculate the volume of reservoirs worldwide using remote sensing



Tutorial: Analyzing Satellite Imagery and Calculating Reservoir Volumes
                        
Welcome to the tutorial for your app, which automates the process of analyzing satellite imagery and calculating the area and volume of reservoirs. This guide will walk you through the steps to use the app effectively.    
                        ---
 Step 1: Define the Region of Interest (ROI)
 1. **Set the Region of Interest (ROI)**  
 Start by defining the Region of Interest (ROI), which is the geographic area you want to analyze. You can specify this by selecting coordinates or using a map interface to draw a boundary around the reservoir.  
 **Tip:** You can zoom in and adjust the shape of the ROI for more precise selection.
                        ---
 Step 2: Define the Date Range
 1. **Select the Date Range**  
The next step is to choose a date range for the analysis. You can use the calendar interface within the app to select the start and end dates for the period you wish to analyze.  
The app will automatically filter available satellite imagery based on the selected date range and cloud coverage.

 Cloud Coverage Percentage Filter:  
The app will display images for the chosen date range and allow you to choose the maximum acceptable percentage of cloud coverage for the images.  
**Tip:** To ensure clear images, select a lower cloud coverage threshold (e.g., less than 10%).
                        ---
Step 3: Confirm the Reservoir Selection
1. **Select the Reservoir**  
After defining the ROI and setting the date range, the app will retrieve satellite imagery for the region. You will be shown a list of possible reservoirs within the selected area.  
 Review the options and confirm the specific reservoir you want to analyze.  
  **Tip:** If the app detects multiple water bodies, it will present thumbnails or maps to help you identify the correct reservoir.  
                        ---
Step 4: Choose the Cloud Coverage Percentage
1. **Choose Cloud Coverage Threshold**  
You will now select the cloud coverage threshold. The app will show you images with varying levels of cloud coverage.  
ou can choose a cloud coverage percentage that meets your needs (e.g., less than 10%, 20%, etc.).  
**Tip:** For more accurate results, choose a threshold that minimizes the impact of cloud cover on your analysis.
                        ---
Step 5: Choose the Output Variables
     1. **Select Output Variables**  
        Now, you can choose the specific variables you want the app to calculate for the reservoir. These may include:
         - Water Area
           - Volume
           - Time Series Data for Volume
           - Bathymetric Information  
      **Tip:** Select the variables you are most interested in, such as volume or changes over time.                  
                        ---

Step 6: Press the "Start" Button   
      1. **Start the Analysis** 
      Once all parameters have been defined (date range, reservoir selection, cloud coverage, and output variables), you can initiate the analysis       by pressing the **"Start"** button.  
      The app will begin processing the satellite imagery, applying necessary corrections, and performing calculations to estimate the reservoir's water area and volume.  
       **Tip:** Depending on the data size, the process may take a few minutes. You’ll see a progress indicator during this time.
                        ---
Step 7: View and Export Results
      1. **View Results**  
      Once the analysis is complete, you can view the results directly within the app. The app will display visualizations of the water area and         provide calculated volume data for the reservoir.
      2. **Export Data**  
      You can export the analysis results in CSV, Excel, or other formats for further analysis or reporting. Simply click the "Export" button to download the data.
                        ---
Notes
1. **Fill the parameters**
In order for the software to compute the water analysis all the paremeters must have been adressed
2. **Statistics**  
Note that 'higher percentage' and 'lower percentage' values are calulated based on the maxiumum and minum water volume value from the calculated time series comparing with the maximum water volume present on the SWOT lakes database for that specific reservoir
                        ---
Conclusion
By following these steps, you can efficiently analyze satellite imagery and calculate reservoir volumes using the app. The methodology ensures accurate results with cloud coverage filtering, error checking, and reliable bathymetric analysis.
If you encounter any issues or need further assistance, refer to the help section within the app or contact support.
