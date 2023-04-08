# Question:
# In this coding challenge, your objective is to utilize the arcpy.da module to undertake some basic partitioning of
# your dataset. In this coding challenge, I want you to work with the Forest Health Works dataset from RI GIS
# (I have provided this as a downloadable ZIP file in this repository).
#
# Using the arcpy.da module (yes, there are other ways and better tools to do this), I want you to extract all sites
# that have a photo of the invasive species (Field: PHOTO) into a new Shapefile, and do some basic counts of the dataset
# In summary, please addressing the following:
# 1. Count how many individual records have photos, and how many do not (2 numbers), print the results.
# 2. Count how many unique species there are in the dataset, print the result.
# 3. Generate two shapefiles, one with photos and the other without.


# Answer:
import os  # import module to interact with the native OS Python is currently running on
import arcpy  # import package to perform geographic data analysis, data conversion, data management, and map automation

arcpy.env.workspace = os.getcwd()  # To get current working directory
arcpy.env.overwriteOutput = True  # allowed to overwrite output files

# 1. Count how many individual records have photos, and how many do not (2 numbers), print the results.
input_shp = 'RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp'
fields = ['photo']

# Count how many individual records have photos
expression = arcpy.AddFieldDelimiters(input_shp, "photo") + " = 'y'"  # to allow for use in SQL expressions in cursor
with arcpy.da.SearchCursor(input_shp, fields, expression) as cursor:
    count = 0
    for row in cursor:
        count += 1
print(count, 'individual records have photos')

# Count how many individual records do not have photos
expression2 = arcpy.AddFieldDelimiters(input_shp, "photo") + " = ''"  # to allow for use in SQL expressions in cursor
with arcpy.da.SearchCursor(input_shp, fields, expression2) as cursor:
    count = 0
    for row in cursor:
        count += 1
print(count, 'individual records do not have photos')


# 2. Count how many unique species there are in the dataset, print the result.
input_shp = 'RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp'
fields = ['Species']

expression = arcpy.AddFieldDelimiters(input_shp, "Species") + "<> ''"  # to allow for use in SQL expressions in cursor
with arcpy.da.SearchCursor(input_shp, fields, expression) as cursor:
    count = 0
    for row in cursor:
        count += 1
print(count, 'unique species there are in the dataset')


# 3. Generate two shapefiles, one with photos and the other without.
input_shp = 'RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp'

# Generate shapefile with photos
output_shp = "RI_Forest_Health_with_photo.shp"
arcpy.CopyFeatures_management(input_shp, output_shp)  # Copies features from the input to a new feature class

with arcpy.da.UpdateCursor(output_shp, "photo") as cursor:
    for row in cursor:
        if row[0] == 'y':
            cursor.deleteRow()

# Generate shapefile without photos
output_shp2 = "RI_Forest_Health_without_photo.shp"
arcpy.CopyFeatures_management(input_shp, output_shp2)  # Copies features from the input to a new feature class

with arcpy.da.UpdateCursor(output_shp2, "photo") as cursor:
    for row in cursor:
        if row[0] == ' ':
            cursor.deleteRow()
