# Question:
# For this coding challenge, I want you to find a particular tool that you like in arcpy. It could be a tool that
# you have used in GIS before or something new. Try browsing the full tool list to get some insight here
# (click Tool Reference on the menu list to the left).
#
# Set up the tool to run in Python, add some useful comments, and importantly, provide some example data in
# your repository (try to make it open source, such as Open Streetmap, or RI GIS. You can add it as a zip file to
# your repository.
#
# My only requirements are:
#
# 1. Comment your code well.
# 2. Ensure that the code will run on my machine with only a single change to a single variable
# (i.e. a base folder location).


# Answer:
# This code is an example of changes in the spatial resolution of a raster dataset and sets rules for aggregating or
# interpolating values across the new pixel sizes using the arcpy tool named "Resample".
# The data example used in this code is a resample 5 cell size from the original data source taken from
# https://data.rigis.org/img/2016USDA/tif/0310001400.zip
# note: the original data is too big to be uploaded to GitHub, therefore needs to be resampled beforehand

# Step:
# 1. Extract data.zip
# 2. Move inside of data directory (0310001400.prj, 0310001400.tfw, 0310001400.tif, 0310001400.tif.ovr,
#    0310001400.tif.aux.xml) to the same directory as Challenge_04.py (if it is not in the same directory)
# 3. After all 6 files are in the same directory, run Challenge_04.py

import os  # import module to operate on underlying Operating System tasks
import arcpy  # import package to perform geographic data analysis, data conversion, data management, and map automation

dir_path = os.path.dirname(os.path.realpath(__file__))  # set working directory in the same dir as .py file

in_ras = os.path.join(dir_path, '0310001400_res_5.tif')  # The raster dataset with the spatial resolution to be changed
out_ras = os.path.join(dir_path, '0310001400_res_5_10.tif')  # The dataset being created
cell_size = '10'  # The cell size of the new raster using an existing raster dataset
resampling_type = 'NEAREST'  # Specifies the resampling technique to be used (NEAREST, BILINEAR, CUBIC, MAJORITY)
# Resample TIFF image to a lower resolution
arcpy.Resample_management(in_ras, out_ras, cell_size, resampling_type)

