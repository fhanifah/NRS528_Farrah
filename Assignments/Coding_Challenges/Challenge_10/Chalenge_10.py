# Question:
# Our coding challenge this week that improves our practice with rasters from Week 10.
#
# Task 1 - Use what you have learned to process the Landsat files provided, this time, you know you are interested in
# the NVDI index which will use Bands 4 (red, aka vis) and 5 (near-infrared, aka nir) from the Landsat 8 imagery,
# see here for more info about the bands: https://www.usgs.gov/faqs/what-are-band-designations-landsat-satellites.
# Data provided are monthly (a couple are missing due to cloud coverage) during the year 2015 for the State of RI, and
# stored in the file Landsat_data_lfs.zip.
#
# Before you start, here is a suggested workflow:
# 1. Extract the Landsat_data_lfs.zip file into a known location.
# 2. For each month provided, you want to calculate the NVDI, using the equation: nvdi = (nir - vis) / (nir + vis)
#    https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index. Consider using the Raster Calculator Tool in
#    ArcMap and using "Copy as Python Snippet" for the first calculation.
#
# The only rule is, you should run your script once, and generate the NVDI for ALL MONTHS provided. As part of your
# code submission, you should also provide a visualization document (e.g. an ArcMap layout in PDF format), showing the
# patterns for an area of RI that you find interesting.


# Answer:
# This script is to calculate the NVDI, using the equation: nvdi = (nir - vis) / (nir + vis)
# This script uses the data from
# https://github.com/marecotec/Course_ArcGIS_Python/blob/master/Assignments/Coding_Challenges/Challenge_10/Landsat_data_lfs.zip
# Before running the script, please download and extract the data in the same directory as this script

import os  # import module to interact with the native OS Python is currently running on
import arcpy  # import package to perform geographic data analysis, data conversion, data management, and map automation
import glob  # import module to return all file paths that match a specific pattern

arcpy.env.workspace = os.getcwd()  # To get current working directory
arcpy.env.overwriteOutput = True  # allowed to overwrite output files

# Make a list of directory (each month)
items = os.listdir('.')
dir_list = []
for item in items:
    if os.path.isdir(item):
        dir_list.append(item)

# Calculate NVDI, using the equation: nvdi = (nir - vis) / (nir + vis) for each month
for dir in dir_list:
    print("calculate month:", dir)  # print statements
    in_raster1 = glob.glob(os.path.join(arcpy.env.workspace, str(dir), "*_B5.tif"))  # Band 5 (near-infrared, aka nir)
    in_raster2 = glob.glob(os.path.join(arcpy.env.workspace, str(dir), "*_B4.tif"))  # Bands 4 (red, aka vis)
    output_raster = arcpy.ia.RasterCalculator([in_raster1, in_raster2], ["x", "y"], "(x-y)/(x+y)")
    output_raster.save(os.path.join(arcpy.env.workspace, str(dir), str(dir) + "NVDI.tif"))
