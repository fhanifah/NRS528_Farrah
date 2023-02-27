# Question:
# For this coding challenge, I want you to practice the heatmap generation that we went through in class, but this time
# obtain your own input data, and I want you to generate heatmaps for TWO species.
#
# You can obtain species data from a vast array of different sources, for example:
# - obis - Note: You should delete many columns (keep species name, lat/lon) as OBIS adds some really long strings
#   that don't fit the Shapefile specification.
# - GBIF
# - Maybe something on RI GIS
# - Or just Google species distribution data
#
# My requirements are:
# 1. The two input species data must be in a SINGLE CSV file, you must process the input data to separate out the
#    species (Hint: You can a slightly edited version of our CSV code from a previous session to do this),
#    I recommend downloading the species data from the same source so the columns match.
# 2. Only a single line of code needs to be altered (workspace environment) to ensure code runs on my computer,
#    and you provide the species data along with your Python code.
# 3. The heatmaps are set to the right size and extent for your species input data, i.e. appropriate fishnet cellSize.
# 4. You leave no trace of execution, except the resulting heatmap files.
# 5. You provide print statements that explain what the code is doing, e.g. Fishnet file generated.


# Answer:
# This code is an example of heatmap generation using data obtained from obis with 2 species
# Chelonia mydas (Green sea turtle) for global scale and Homarus americanus (american lobster) for regional scale
# Step: please change workspace to your working directory (line 31) before run this script

import csv  # import module to working with csv format files
import arcpy  # import package to perform geographic data analysis, data conversion, data management, and map automation
arcpy.env.overwriteOutput = True  # allowed to overwrite output files
# set working directory
arcpy.env.workspace = r"D:\NRS528 - Farrah\Assignments\Coding_Challenges\Challenge_05"

# Make list of species from csv file
with open('data_species.csv') as data:  # open csv file
    next(data)  # skip header of csv file
    species_list = []  # make a new list that will contain list of species
    for row in csv.reader(data):
        if row[0].split(' ')[0] not in species_list:
            species_list.append(row[0].split(' ')[0])

for species in species_list:
    # Make a new csv files for every species on species_list
    with open(species + '.csv', 'w', newline='') as file:  # create new csv files for every species on species_list
        writer = csv.writer(file)
        writer.writerow(['Species', 'Lat', 'Lon'])
        with open('data_species.csv') as data:  # input csv file
            next(data)
            for row in csv.reader(data):
                if row[0].split(' ')[0] == species:
                    writer.writerow([row[0], row[1], row[2]])  # write species name, Lat, and Lon to a new csv files
    print('csv file generated for species', species)  # print statements

    # Using species.csv to convert .csv to a shapefile.
    in_Table = str(species) + '.csv'  # name of input cvs
    x_coords = 'Lon'  # name of x-coords from csv file
    y_coords = 'Lat'  # name of y-coords from csv file
    z_coords = ''
    out_Layer = str(species)
    saved_Layer = str(species) + '.shp'  # name of output shapefile
    # Set the spatial reference
    spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
    # Save to a layer file
    arcpy.CopyFeatures_management(lyr, saved_Layer)
    print('shapefile generated for species', species)  # print statements

    # Define the Extent of the generated species shapefile.
    desc = arcpy.Describe(str(species) + '.shp')  # name of input shapefile
    XMin = desc.extent.XMin
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax

    # Generate a fishnet based on the originCoordinate
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
    outFeatureClass = str(species) + '_fishnet.shp'  # Name of output fishnet
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
    target_features = str(species) + '_fishnet.shp'  # Name of input fishnet
    join_features = str(species) + '.shp'  # Name of species shapefile
    out_feature_class = str(species) + '_heatmap.shp'  # Name of output heatmap
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

    # Delete the intermediate files (csv, species shapefile, and fishnet)
    arcpy.Delete_management(str(species) + '.csv')
    arcpy.Delete_management(str(species) + '.shp')
    arcpy.Delete_management(str(species) + '_fishnet.shp')