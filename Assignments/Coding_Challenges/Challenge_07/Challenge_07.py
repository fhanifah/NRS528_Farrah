# Question:
# Our coding challenge this week should make use of temporary folders, output folders and file management.
# Convert your Coding Challenge 5 exercise to work with temporary folders, os.path.join and glob.glob.
# Do not take too much time on this and if you do not have a working Challenge 5, talk to the instructor.

# Answer:
# This code is a modification of Coding Challenge 5, which is an example of heatmap generation using data obtained from
# obis with 2 species, Chelonia mydas (Green sea turtle) on a global scale and Homarus americanus (American lobster)
# on a regional scale.
# In this modification, instead of manually defining a working directory path, I use temporary folders, output folders,
# and file management using module glob and os. Therefore the code could run well in any directory.

import glob  # import module to return all file paths that match a specific pattern
import os  # import module to interact with the native OS Python is currently running on
import csv  # import module to working with csv format files
import arcpy  # import package to perform geographic data analysis, data conversion, data management, and map automation

arcpy.env.overwriteOutput = True  # allowed to overwrite output files
# set working directory
input_directory = os.getcwd()  # To get current working directory
input_csv = glob.glob("*.csv")  # Get specific file in current directory

keep_temp_files = True

# Create new directories for temporary files and output (heatmap) if the directories are not exist
if not os.path.exists(os.path.join(input_directory, "temporary_files")):
    os.mkdir(os.path.join(input_directory, "temporary_files"))
if not os.path.exists(os.path.join(input_directory, "heatmap")):
    os.mkdir(os.path.join(input_directory, "heatmap"))

# Make list of species from csv file
with open(input_csv[0]) as data:  # open csv file
    next(data)  # skip header of csv file
    species_list = []  # make a new list that will contain list of species
    for row in csv.reader(data):
        if row[0].split(' ')[0] not in species_list:
            species_list.append(row[0].split(' ')[0])

for species in species_list:
    # Make a new csv files for every species on species_list
    with open(os.path.join(input_directory, 'temporary_files', species + '.csv'), 'w', newline='') as file:  # create new csv files for every species on species_list
        writer = csv.writer(file)
        writer.writerow(['Species', 'Lat', 'Lon'])
        with open(input_csv[0]) as data:  # input csv file
            next(data)
            for row in csv.reader(data):
                if row[0].split(' ')[0] == species:
                    writer.writerow([row[0], row[1], row[2]])  # write species name, Lat, and Lon to a new csv files
    print('csv file generated for species', species)  # print statements

    # Using species.csv to convert .csv to a shapefile.
    in_Table = os.path.join(input_directory, 'temporary_files', str(species) + '.csv')  # name of input cvs
    x_coords = 'Lon'  # name of x-coords from csv file
    y_coords = 'Lat'  # name of y-coords from csv file
    z_coords = ''
    out_Layer = str(species)
    saved_Layer = os.path.join(input_directory, 'temporary_files', str(species) + '.shp')  # name of output shapefile
    # Set the spatial reference
    spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
    # Save to a layer file
    arcpy.CopyFeatures_management(lyr, saved_Layer)
    print('shapefile generated for species', species)  # print statements

    # Define the Extent of the generated species shapefile.
    desc = arcpy.Describe(os.path.join(input_directory, 'temporary_files', str(species) + '.shp'))  # name of input shapefile
    XMin = desc.extent.XMin
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax

    # Generate a fishnet based on the originCoordinate
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
    outFeatureClass = os.path.join(input_directory, 'temporary_files', str(species) + '_fishnet.shp')  # Name of output fishnet
    # Set the origin of the fishnet
    originCoordinate = str(float(XMin)) + ' ' + str(float(YMin))  # left bottom of point data
    yAxisCoordinate = str(float(XMin)) + ' ' + str(float(YMin+1))   # sets the orientation on the y-axis (head north)
    # Sets width and height of fishnet cells; in this case, cell size depends on how big the Extent
    # and number of fishnets horizontal grid would be fixed at 360
    # and fishnet polygon will be uniform cellSizeWidth = cellSizeHeight
    cellSizeWidth = str(float((XMax-XMin)/360))
    cellSizeHeight = str(float((XMax-XMin)/360))
    numRows = ''  # leave blank, as we have set cellSize
    numColumns = ''  # leave blank, as we have set cellSize
    oppositeCorner = str(float(XMax)) + ' ' + str(float(YMax))   # i.e. max x and max y coordinate
    labels = 'NO_LABELS'
    templateExtent = '#'  # no need to use, as we have set yAxisCoordinate and oppositeCorner
    geometryType = 'POLYGON'  # create a polygon, could be POLYLINE
    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                   cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                   oppositeCorner, labels, templateExtent, geometryType)
    print('fishnet file generated for species', species)  # print statements

    # Undertake a Spatial Join to join the fishnet to the observed points.
    target_features = os.path.join(input_directory, 'temporary_files', str(species) + '_fishnet.shp')  # Name of input fishnet
    join_features = os.path.join(input_directory, 'temporary_files', str(species) + '.shp')  # Name of species shapefile
    out_feature_class = os.path.join(input_directory, 'heatmap', str(species) + '_heatmap.shp')  # Name of output heatmap
    join_operation = 'JOIN_ONE_TO_ONE'
    join_type = 'KEEP_ALL'
    field_mapping = ''
    match_option = 'INTERSECT'
    search_radius = ''
    distance_field_name = ''
    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                               join_operation, join_type, field_mapping, match_option,
                               search_radius, distance_field_name)
    print('heatmap file generated for species', species)  # print statements

# Deletion temporary_files directories
arcpy.Delete_management(os.path.join(input_directory, "temporary_files"))