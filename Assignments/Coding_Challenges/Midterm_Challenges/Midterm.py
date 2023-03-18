# Question:
# In this assignment, you are instructed to produce a small script tool that takes advantage of arcpy and Python.
# You will need to provide example data, and the code should run on all PC's.
# The tool needs to manipulate a dataset across three different processes, for example, extracting, modifying
# and exporting data. The exact workflow is entirely up to yourself. You are expected to take 3-4 hours on this coding
# assignment, and you should deposit your code and example files within a Github repository for feedback and grading.
#
# The criteria are:
#  1. Cleanliness of code (10 points)
#  2. Functionality (10 points)
#  3. Appropriate use of documentation (10 points)
#  4. Depth of processing operation (10 points)
#  5. In addition, you must provide example data and minimize the amount of editing a user must make in order for
#     the program to run (10 points).


# Answer:
# This script is to generate an interpolated spatial map from points of variables in the ocean for several years
# There are 4 processes in this script:
# 1. Generate yearly csv data from 1 csv data that contain Year, Lat, Lon, and SST
# 2. Generate shapefile of SST for every year
# 3. Generate a raster file of points interpolation
# 4. Masking the interpolation with land, so only SST in the ocean that show
#
# In this example, there are 2 inputs needed
# 1. Homarus.csv: Year, Lat, Lon, and SST are obtained from https://obis.org/ for Homarus americanus (American lobster)
# 2. ne_10m_ocean.shp (for masking land and ocean) obtained from
#    https://www.arcgis.com/home/item.html?id=4462f63e2d1a4844bcf4dab98d376f4e
#
# Step:
# 1. Extract ne_10m_ocean.zip in the same directory as the working directory
# 2. Change 'arcpy.env.workspace' in line 40 to your working directory
# 3. Run the script

import csv  # import module to working with csv format files
import arcpy  # import package to perform geographic data analysis, data conversion, data management, and map automation
from arcpy.sa import *  # Importing the Spatial Analyst module
arcpy.env.overwriteOutput = True  # allowed to overwrite output files
# set working directory
arcpy.env.workspace = r"D:\NRS528 - Farrah\Assignments\Midterm_Challenges"

# Make list year
with open('Homarus.csv') as data:  # open csv file
    next(data)  # skip header of csv file
    year_list = []  # make a new list that will contain list of year
    for row in csv.reader(data):
        if row[0] not in year_list:
            year_list.append(row[0])
year_list = sorted(year_list)  # sorting list of year

for year in year_list:
    # 1. Make a new csv files for every year on year_list
    print('csv file created for year: ', year)  # print statements
    with open(year + '.csv', 'w', newline='') as file:  # create new csv files for every species on year_list
        writer = csv.writer(file)
        writer.writerow(['Year', 'Lat', 'Lon', 'SST'])
        with open('Homarus.csv') as data:  # input csv file
            next(data)
            for row in csv.reader(data):
                if row[0] == year:
                    writer.writerow([row[0], row[1], row[2], row[3]])  # write year, Lat, Lon, SST to a new csv files

    # 2. Generate shapefile of SST for every year
    print('shapefile created for year: ', year)  # print statements
    # Using year.csv to convert .csv to a shapefile.
    in_Table = str(year) + '.csv'  # name of input cvs
    x_coords = 'Lon'  # name of x-coords from csv file
    y_coords = 'Lat'  # name of y-coords from csv file
    z_coords = 'SST'  # name of z-coords from csv file
    out_Layer = z_coords
    saved_Layer = str(year) + '.shp'  # name of output shapefile
    # Set the spatial reference
    spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
    # Save to a layer file
    arcpy.CopyFeatures_management(lyr, saved_Layer)

    # 3. Generate raster file of points interpolation
    print('raster file created for year: ', year)  # print statements
    # Set local variables
    input_points = TopoPointElevation([[str(year), 'SST']])  # name of input shapefile and variable for interpolation
    cell_size = ''
    extent = ''
    margin = ''
    minimum_z_value = ''
    maximum_z_value = ''
    enforce = 'NO_ENFORCE'  # No sinks will be filled
    data_type = 'CONTOUR'  # The dominant type of input data will be elevation contours. This is the default.
    # Execute point to spatial using TopoToRaster
    outTTR = TopoToRaster(input_points, cell_size, extent, margin, minimum_z_value, maximum_z_value, enforce, data_type)
    # Save the output
    outTTR.save(str(year) + 'raster.tif')  # name of output raster

    # 4. Masking the interpolation with land, so only SST in the ocean that show
    print('SST with mask file created for year: ', year)  # print statements
    # Set local variables
    inRaster = str(year) + 'raster.tif'  # name of input raster
    inMaskData = "ne_10m_ocean.shp"  # name of input shapefile for masking
    extraction_area = "INSIDE"  # Cells within the input mask will be selected and written to the output raster
    # Execute masking land and ocean using ExtractByMask
    outExtractByMask = ExtractByMask(inRaster, inMaskData, extraction_area)
    # Save the output
    outExtractByMask.save(str(year) + 'mask.tif')

    # 5. Deleting unnecessary files
    print('deleting unnecessary files')  # print statements
    # Delete the intermediate files (csv, shapefile, and spatial interpolation before masking)
    arcpy.Delete_management(str(year) + '.csv')
    arcpy.Delete_management(str(year) + '.shp')
    arcpy.Delete_management(str(year) + 'raster.tif')

print('Finished calculating without error')  # print statements



