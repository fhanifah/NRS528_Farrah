# Question:
# In your final assignment for this course, you should create a Python Toolbox that contains a minimum of three
# simple tools for undertaking geoprocessing and file management operations. These tools can be discrete or part of
# a larger workflow. However, the caveats are that you should create a "single file" toolbox (no includes, or
# external file tools) and you should aim to not exceed 2000 lines of code in its entirety (but if you do, no worries).
# You should document the toolbox using Github README.md and provide example data for running each of your tools.
# Grading and feedback will focus on:
# 1) Does the toolbox install, and the tools run successfully?
# 2) cleanliness of code,
# 3) functionality and depth of processing operation, and
# 4) appropriate use of documentation. Plus,
# 5) provide example data that allows me to test your tools.
# The criteria are:
# 1. Does the toolbox install and run? (25 points)
# 2. Cleanliness of code (25 points)
# 3. Functionality and depth of processing (25 points)
# 4. Appropriate use of documentation (15 points)
# 5. In addition, you must provide example data (10 points).


# Answer:
# This script is a toolbox for processing and visualizing Temperature, zonal and meridional current, and bathymetry from
# data point. In this example, the data are obtained from RAMA (Indian) https://www.pmel.noaa.gov/tao/drupal/disdel/
# in Indian Ocean save it in csv file.
#
# In this toolbox, there are 3 tools to processing and visualizing Temperature, zonal and meridional current, and
# bathymetry respectively.
# Tool 1: Temperature
# There are 4 processes in this tool:
# 1. Generate shapefile of of Temperature from csv data that contain Lat, Lon, Temperature, u, and v
# 2. Generate raster file of points interpolation
# 3. Masking the interpolation with land, so only Temperature in the ocean that show in the map
# 4. Deleting unnecessary files
# Tool 2: Current
# There are 4 processes in this tool:
# 1. Generate shapefiles of u (zonal current) and v (meridional current) from csv data that contain Lat, Lon,
#    Temperature, u, and v
# 2. Generate raster file of u (zonal current) and v (meridional current) from shapefiles
# 3. Generate vector field file of u (zonal current) and v (meridional current) from raster
# 4. Deleting unnecessary files
# Tool 3: Bathymetry
# There are 4 processes in this tool:
# 1. Define bathymetry from ETOPO10 (Topography and Bathymetry) file
# 2. Masking bathymetry
# 3. Clip bathymetry by known extent (Temperature raster file) - Left Bottom Right Top
# 4. Deleting unnecessary files
#
# In this example, there are 3 inputs needed
# 1. RAMA.csv: Lat, Lon, Temperature, u, and v are obtained from from https://www.pmel.noaa.gov/tao/drupal/disdel/
#    RAMA (Indian). This is one time monthly data (December 2019) in the depth 10 m.
# 2. ne_10m_ocean.shp (for masking land and ocean) obtained from
#    https://www.arcgis.com/home/item.html?id=4462f63e2d1a4844bcf4dab98d376f4e
# 3. etopo10 are obtained from
#    https://github.com/marecotec/Course_ArcGIS_Python/blob/master/Classes/10_Rasters/Step_2_Data.zip
#
# Steps:
# 1. Extract ne_10m_ocean.zip and etopo10.zip
# 2. Install and run the toolbox in ArcGIS Pro using this guide for input files:
#    a. Tool 1: Temperature
#       Input csv: input csv file, in this example RAMA.csv
#       Input mask file: input shapefile for masking, in this example ne_10m_ocean.shp
#       Output shapefile: output shapefile (would be deleted at the end of this process, process no.4)
#       Output raster: output raster (would be deleted at the end of this process, process no.4)
#       Output Temperature: final result of this tool (raster)
#    b. Tool 2: Current
#       Input csv: input csv file, in this example RAMA.csv
#       Output u shapefile: output shapefile (would be deleted at the end of this process, process no.4)
#       Output v shapefile: output shapefile (would be deleted at the end of this process, process no.4)
#       Output u raster: output raster (would be deleted at the end of this process, process no.4)
#       Output v raster: output raster (would be deleted at the end of this process, process no.4)
#       Output vector field: final result of this tool (raster vector field)
#    c. Tool 3: Bathymetry
#       Input Topography Bathymetry: input topography bathymetry file, in this example etopo10
#       Input mask file: input shapefile for masking, in this example ne_10m_ocean.shp
#       Input raster Temperature: file from final result of this Tool 1: Temperature (raster)
#       Output Bathymetry: output bathymetry (would be deleted at the end of this process, process no.4)
#       Output mask Bathymetry: output masking bathymetry (would be deleted at the end of this process, process no.4)
#       Output Bathymetry same region as Temperature: final result of this tool (raster)


import arcpy
from arcpy.sa import *

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Temperature, Current, Bathymetry]


class Temperature(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Temperature"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_csv = arcpy.Parameter(name="input_csv",
                                     displayName="Input csv",
                                     datatype="DETable",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(input_csv)

        input_mask = arcpy.Parameter(name="input_mask",
                                     displayName="Input mask file",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(input_mask)


        output_shp = arcpy.Parameter(name="output_shp",
                                 displayName="Output shapefile",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_shp)

        output_ras = arcpy.Parameter(name="output_ras",
                                 displayName="Output raster",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_ras)

        output_temp = arcpy.Parameter(name="output_temp",
                                 displayName="Output Temperature",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_temp)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.env.overwriteOutput = True
        # 1. Generate shapefile of of Temperature from csv
        arcpy.AddMessage('Shapefile created for Temperature')  # print statements
        # Using input .csv file to convert .csv to a shapefile
        in_Table = parameters[0].valueAsText  # input cvs
        x_coords = 'Lon'  # name of x-coords from csv file
        y_coords = 'Lat'  # name of y-coords from csv file
        z_coords = 'Temp'  # name of z-coords from csv file
        out_Layer = z_coords
        saved_Layer = parameters[2].valueAsText  # output shapefile
        # Set the spatial reference
        spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
        lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
        # Save to a layer file
        arcpy.CopyFeatures_management(lyr, saved_Layer)

        # 2. Generate raster file of points interpolation
        arcpy.AddMessage('Raster file created for Temperature')  # print statements
        # Set local variables
        input_points = TopoPointElevation([[parameters[2].valueAsText, 'Temp']])  # input shp and variable
        cell_size = ''
        extent = ''
        margin = ''
        minimum_z_value = ''
        maximum_z_value = ''
        enforce = 'NO_ENFORCE'  # No sinks will be filled
        data_type = 'CONTOUR'  # The dominant type of input data will be elevation contours. This is the default.
        # Execute point to spatial using TopoToRaster
        outTTR = TopoToRaster(input_points, cell_size, extent, margin, minimum_z_value, maximum_z_value, enforce,
                              data_type)
        # Save the output
        outTTR.save(parameters[3].valueAsText)  # output raster

        # 3. Masking the interpolation with land, so only Temperature in the ocean that show in the map
        arcpy.AddMessage('Temperature with mask file created')  # print statements
        # Set local variables
        inRaster = parameters[3].valueAsText  # input raster
        inMaskData = parameters[1].valueAsText  # input shapefile for masking
        extraction_area = 'INSIDE'  # Cells within the input mask will be selected and written to the output raster
        # Execute masking land and ocean using ExtractByMask
        outExtractByMask = ExtractByMask(inRaster, inMaskData, extraction_area)
        # Save the output
        outExtractByMask.save(parameters[4].valueAsText)  # output raster

        # 4. Deleting unnecessary files
        arcpy.AddMessage('Deleting unnecessary files')  # print statements
        # Delete the intermediate files (shapefile and spatial interpolation before masking)
        arcpy.Delete_management(parameters[2].valueAsText)
        arcpy.Delete_management(parameters[3].valueAsText)
        return

class Current(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Current"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_csv = arcpy.Parameter(name="input_csv",
                                     displayName="Input csv",
                                     datatype="DETable",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(input_csv)


        output_u_shp = arcpy.Parameter(name="output_u_shp",
                                 displayName="Output u shapefile",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_u_shp)

        output_v_shp = arcpy.Parameter(name="output_v_shp",
                                 displayName="Output v shapefile",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_v_shp)

        output_u_ras = arcpy.Parameter(name="output_u_ras",
                                 displayName="Output u raster",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_u_ras)

        output_v_ras = arcpy.Parameter(name="output_v_ras",
                                 displayName="Output v raster",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_v_ras)

        output_vector_field = arcpy.Parameter(name="output_vector_field",
                                 displayName="Output vector field",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_vector_field)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.env.overwriteOutput = True
        # 1. Generate shapefiles of u (zonal current) and v (meridional current) from csv
        # Generate shapefile of u (zonal current) from csv
        arcpy.AddMessage('shapefile created for u')  # print statements
        # Using input .csv file to convert .csv to a shapefile
        in_Table = parameters[0].valueAsText  # input cvs
        x_coords = 'Lon'  # name of x-coords from csv file
        y_coords = 'Lat'  # name of y-coords from csv file
        z_coords = 'u'  # name of z-coords from csv file
        out_Layer = z_coords
        saved_Layer = parameters[1].valueAsText  # output shapefile
        # Set the spatial reference
        spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
        lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
        # Save to a layer file
        arcpy.CopyFeatures_management(lyr, saved_Layer)

        # Generate shapefile of v (meridional current) from csv
        arcpy.AddMessage('shapefile created for v')  # print statements
        # Using input .csv file to convert .csv to a shapefile
        in_Table = parameters[0].valueAsText  # input cvs
        x_coords = 'Lon'  # name of x-coords from csv file
        y_coords = 'Lat'  # name of y-coords from csv file
        z_coords = 'v'  # name of z-coords from csv file
        out_Layer = z_coords
        saved_Layer = parameters[2].valueAsText  # output shapefile
        # Set the spatial reference
        spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
        lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
        # Save to a layer file
        arcpy.CopyFeatures_management(lyr, saved_Layer)

        # 2. Generate raster file of u (zonal current) and v (meridional current) from shapefiles
        # Generate raster file of u (zonal current) from shapefile
        arcpy.AddMessage('raster file created for u')  # print statements
        # Set local variables
        inFeatures = parameters[1].valueAsText
        valField = 'u'
        outRaster = parameters[3].valueAsText
        assignmentType = 'MOST_FREQUENT'
        priorityField = 'NONE'
        cellSize = '1'
        # Run PolygonToRaster
        arcpy.conversion.PointToRaster(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)

        # Generate raster file of v (meridional current) from shapefile
        arcpy.AddMessage('raster file created for v')  # print statements
        # Set local variables
        inFeatures = parameters[2].valueAsText
        valField = 'v'
        outRaster = parameters[4].valueAsText
        assignmentType = 'MOST_FREQUENT'
        priorityField = 'NONE'
        cellSize = '1'
        # Run PolygonToRaster
        arcpy.conversion.PointToRaster(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)

        # 3. Generate vector field file of u (zonal current) and v (meridional current) from raster
        arcpy.AddMessage('vector field created from u and v')  # print statements
        # input variables (u and v) from raster
        in_raster_u = parameters[3].valueAsText  # input raster u
        in_raster_v = parameters[4].valueAsText  # input raster v
        # Execute VectorField function
        out_vectorField_raster = VectorField(in_raster_u, in_raster_v, 'Vector-UV', 'Geographic', 'Vector-MagDir')
        # Save the output
        out_vectorField_raster.save(parameters[5].valueAsText)  # output vector field

        # 4. Deleting unnecessary files
        arcpy.AddMessage('Deleting unnecessary files')  # print statements
        # Delete the intermediate files (shapefile and raster files of u and v)
        arcpy.Delete_management(parameters[1].valueAsText)
        arcpy.Delete_management(parameters[2].valueAsText)
        arcpy.Delete_management(parameters[3].valueAsText)
        arcpy.Delete_management(parameters[4].valueAsText)
        return

class Bathymetry(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Bathymetry"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_topo = arcpy.Parameter(name="input_topo",
                                     displayName="Input Topography Bathymetry",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(input_topo)

        input_mask = arcpy.Parameter(name="input_mask",
                                    displayName="Input mask file",
                                    datatype="DEFeatureClass",
                                    parameterType="Required",  # Required|Optional|Derived
                                    direction="Input",  # Input|Output
                                    )
        params.append(input_mask)

        input_ras = arcpy.Parameter(name="input_ras",
                                     displayName="Input raster Temperature",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(input_ras)


        output_sea = arcpy.Parameter(name="output_sea",
                                 displayName="Output Bathymetry",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_sea)

        output_mask = arcpy.Parameter(name="output_mask",
                                 displayName="Output mask Bathymetry",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output_mask)

        output_clip = arcpy.Parameter(name="output_clip",
                                      displayName="Output Bathymetry same region as Temperature",
                                      datatype="DERasterDataset",
                                      parameterType="Required",  # Required|Optional|Derived
                                      direction="Output",  # Input|Output
                                      )
        params.append(output_clip)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.env.overwriteOutput = True
        # 1. Define bathymetry from ETOPO10 (Topography and Bathymetry) file
        arcpy.AddMessage('Bathymetry define from etopo10')  # print statements
        inRas = arcpy.Raster(parameters[0].valueAsText)  # input bathymetry and topography
        lowerLeft = arcpy.Point(inRas.extent.XMin, inRas.extent.YMin)
        cellSize = inRas.meanCellWidth
        arr = arcpy.RasterToNumPyArray(inRas, nodata_to_value=0)
        # extract only sea values
        arr[arr > 0] = -9999
        newRaster = arcpy.NumPyArrayToRaster(arr, lowerLeft, cellSize, value_to_nodata=-9999)
        newRaster.save(parameters[3].valueAsText)  # output bathymetry

        # 2. Masking bathymetry
        arcpy.AddMessage('Masking bathymetry')  # print statements
        inRaster = parameters[3].valueAsText  # name of input raster
        inMaskData = parameters[1].valueAsText  # name of input shapefile for masking
        extraction_area = 'INSIDE'  # Cells within the input mask will be selected and written to the output raster
        # Execute masking land and ocean using ExtractByMask
        outExtractByMask = ExtractByMask(inRaster, inMaskData, extraction_area)
        # Save the output
        outExtractByMask.save(parameters[4].valueAsText)  # output masking bathymetry

        # 3. Clip bathymetry by known extent (Temperature raster file) - Left Bottom Right Top
        arcpy.AddMessage('Clipping bathymetry')  # print statements
        # Define extent area from Temperature raster file
        desc = arcpy.Describe(parameters[2].valueAsText)
        XMin = desc.extent.XMin
        XMax = desc.extent.XMax
        YMin = desc.extent.YMin
        YMax = desc.extent.YMax
        in_raster = parameters[4].valueAsText  # input masking bathymetry
        out_raster = parameters[5].valueAsText  # output masking and clipping bathymetry
        rectangle = str(float(XMin)) + " " + str(float(YMin)) + " " + str(float(XMax)) + " " + str(float(YMax))
        # Clip bathymetry
        arcpy.Clip_management(in_raster, rectangle, out_raster, '#', '#', 'NONE')

        # 4. Deleting unnecessary files
        arcpy.AddMessage('Deleting unnecessary files')  # print statements
        # Delete the intermediate files (global and masking bathymetry)
        arcpy.Delete_management(parameters[3].valueAsText)
        arcpy.Delete_management(parameters[4].valueAsText)
        return