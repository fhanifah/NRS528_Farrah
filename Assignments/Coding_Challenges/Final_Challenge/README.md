# Final Challenge

To use and run this toolbox, please read and follow the steps in this Readme.md to avoid getting errors.

This script is a toolbox for processing and visualizing Temperature, zonal and meridional current, and bathymetry from data points. In this example, the data are obtained from RAMA (Indian) https://www.pmel.noaa.gov/tao/drupal/disdel/ in the Indian Ocean and saved in csv file.


This toolbox has 3 tools for processing and visualizing Temperature, zonal and meridional current, and bathymetry, respectively. 
- Tool 1: Temperature There are 4 processes in this tool:
1. Generate a shapefile of Temperature from csv data that contain Lat, Lon, Temperature, u, and v
2. Generate a raster file of points interpolation.
3. Masking the interpolation with land, so only the Temperature in the ocean that show in the map
4. Deleting unnecessary files 
- Tool 2: Current There are 4 processes in this tool:
1. Generate shapefiles of u (zonal current) and v (meridional current) from csv data that contain Lat, Lon, Temperature, u, and v
2. Generate a raster file of u (zonal current) and v (meridional current) from shapefiles.
3. Generate vector field file of u (zonal current) and v (meridional current) from raster.
4. Deleting unnecessary files 
- Tool 3: Bathymetry There are 4 processes in this tool:
1. Define bathymetry from ETOPO10 (Topography and Bathymetry) file.
2. Masking bathymetry
3. Clip bathymetry by known extent (Temperature raster file) - Left Bottom Right Top
4. Deleting unnecessary files


In this example, there are 3 inputs needed.
1. RAMA.csv: Lat, Lon, Temperature, u, and v are obtained from https://www.pmel.noaa.gov/tao/drupal/disdel/ RAMA (Indian). This data is one-time monthly data (December 2019) in a depth of 10 m.
2. ne_10m_ocean.shp (for masking land and ocean) obtained from https://www.arcgis.com/home/item.html?id=4462f63e2d1a4844bcf4dab98d376f4e
4. etopo10 is obtained from https://github.com/marecotec/Course_ArcGIS_Python/blob/master/Classes/10_Rasters/Step_2_Data.zip


Steps:
1. Extract ne_10m_ocean.zip and etopo10.zip in the same directory as all inputs and this toolbox, for example D:/
2. Install and run the toolbox in ArcGIS Pro using this guide for input files: 
   - Tool 1: Temperature 
      - Input csv: input csv file, in this example RAMA.csv or filled with for example D:/RAMA.csv
      - Input mask file: input shapefile for masking, in this example ne_10m_ocean.shp or filled with for example D:/ne_10m_ocean.shp
      - Output shapefile: rename and change the path of the output shapefile with the same path of this toobox and all input files, for example D:/Temp.shp (would be deleted at the end of this process, process no.4) 
      - Output raster: rename and change the path of the output raster with the same path of this toobox and all input files, for example D:/Temp_ras.tif (would be deleted at the end of this process, process no.4) 
      - Output Temperature: rename and change the path of the final result of this tool with the same path of this toobox and all input files, for example D:/Temp_mask.tif (raster) 
   - Tool 2: Current 
      - Input csv: input csv file, in this example RAMA.csv or filled with for example D:/RAMA.csv
      - Output u shapefile: rename and change the path of the output shapefile with the same path of this toobox and all input files, for example D:/u.shp (would be deleted at the end of this process, process no.4) 
      - Output v shapefile: rename and change the path of the output shapefile with the same path of this toobox and all input files, for example D:/v.shp (would be deleted at the end of this process, process no.4) 
      - Output u raster: rename and change the path of the output raster with the same path of this toobox and all input files, for example D:/u_ras.tif (would be deleted at the end of this process, process no.4) 
      - Output v raster: rename and change the path of the output raster with the same path of this toobox and all input files, for example D:/v_ras.tif (would be deleted at the end of this process, process no.4) 
      - Output vector field: rename and change the path of the final result of this tool with the same path of this toobox and all input files, for example D:/uv_vectorfield.tif (raster vector field) 
   - Tool 3: Bathymetry 
      - Input Topography Bathymetry: input topography bathymetry file, in this example etopo10 or filled with for example D:/etopo10
      - Input mask file: input shapefile for masking, in this example ne_10m_ocean.shp or filled with for example D:/ne_10m_ocean.shp
      - Input raster Temperature: file from the final result of this Tool 1: Temperature (raster) or for example D:/Temp_mask.tif (raster)
      - Output Bathymetry: rename and change the path of the output raster bathymetry with the same path of this toobox and all input files, for example D:/Bat.tif (would be deleted at the end of this process, process no.4) 
      - Output mask Bathymetry: rename and change the path of the output raster masking bathymetry with the same path of this toobox and all input files, for example D:/Bat_mask.tifoutput (would be deleted at the end of this process, process no.4) 
      - Output Bathymetry same region as Temperature: rename and change the path of the final result of this tool with the same path of this toobox and all input files, for example D:/Bathymetry.tif (raster)
