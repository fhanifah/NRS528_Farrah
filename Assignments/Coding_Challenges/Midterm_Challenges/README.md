# Midterm Challenge

This script is to generate an interpolated spatial map from points of variables in the ocean for several years

There are 4 processes in this script:
1. Generate yearly csv data from 1 csv data that contain Year, Lat, Lon, and SST
2. Generate shapefile of SST for every year
3. Generate a raster file of points interpolation
4. Masking the interpolation with land, so only SST in the ocean that show

In this example, there are 2 inputs needed
1. Homarus.csv: Year, Lat, Lon, and SST are obtained from https://obis.org/ for Homarus americanus (American lobster)
2. ne_10m_ocean.shp (for masking land and ocean) obtained from https://www.arcgis.com/home/item.html?id=4462f63e2d1a4844bcf4dab98d376f4e

Step:
1. Extract ne_10m_ocean.zip in the same directory as the working directory
2. Change 'arcpy.env.workspace' in line 40 to your working directory
3. Run the script
