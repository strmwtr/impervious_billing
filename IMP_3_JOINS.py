# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# IMP_3_JOINS.py
# Created on: 2013-10-11 14:10:58.00000
#   (generated by ArcGIS/ModelBuilder)
# Description:
# ---------------------------------------------------------------------------
import arcpy

gdb = r'C:\Users\brownr\Desktop\imperv\data\imp.gdb'
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

sde = r'Database Connections\Connection to GISPRDDB direct connect.sde'

cvgis_CITY_parcel_area = sde + "\\cvgis.CITY.Cadastre\\cvgis.CITY.parcel_area"

imp_list = [
  sde+r'\cvgis.CITY.Buildings\cvgis.CITY.slab_area',
  sde+r'\cvgis.CITY.Buildings\cvgis.CITY.structure_existing_area',
  sde+r'\cvgis.CITY.Buildings\cvgis.CITY.miscellaneous_building_area',
  sde+r'\cvgis.CITY.Transportation_Other\cvgis.CITY.pedestrian_walkway_area',
  sde+r'\cvgis.CITY.Transportation_Railroad\cvgis.CITY.railroad_area',
  sde+r'\cvgis.CITY.Transportation_Other\cvgis.CITY.pedestrian_sidewalk_area',
  sde+r'\cvgis.CITY.Transportation_Road\cvgis.CITY.road_area_master',
  sde+r'\cvgis.CITY.Transportation_Other\cvgis.CITY.vehicle_driveway_area',
  sde+r'\cvgis.CITY.Transportation_Other\cvgis.CITY.vehicle_parking_area'
  ]

# Local variables:
FINAL_IMP_POINTS = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb\\FINAL_IMP_POINTS"
FINAL_IMP_BREAKOUT = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb\\FINAL_IMP_BREAKOUT"

'''
dissolve_slab_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_slab_1"
dissolve_misc_struct_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_misc_struct_1"
dissolve_walkway_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_walkway_1"
dissolve_road_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_road_1"
dissolve_driveway_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_driveway_1"
dissolve_parking_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_parking_1"
dissolve_structure_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_structure_1"
dissolve_sidewalk_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_sidewalk_1"
dissolve_railroad_1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve_railroad_1"
FINAL_IMP_POINTS = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb\\FINAL_IMP_POINTS"
FINAL_IMP_BREAKOUT = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb\\FINAL_IMP_BREAKOUT"
'''

for feat in imp_list:
  feat_name = feat.split('.')[-1]
  inte = gdb + '\\' + feat_name + '_int'
  dis = gdb + '\\' + feat_name + '_dis'
  arcpy.MakeTableView_management(dis, "{0}_tview".format(feat_name, "", "", "")

#Create Table View for FINAL_IMP_POINTS

arcpy.MakeTableView_management(FINAL_IMP_POINTS, "FINAL_IMP_POINTS_tview", "", 
  "", "" )


#AddJoin, Calc and remove-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
# Driveways
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_driveway_1_tview", "GPIN")

#Get the fields from the input
#fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "DRIVEWAY_AREA", "[dissolve_driveway_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up


#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
# Misc_Structures
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_misc_struct_1_tview", "GPIN")

# Get the fields from the input
fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "MISC_STRUCT_AREA", "[dissolve_misc_struct_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up

#----------------------------------------------------------------------------------------------------

# Parking
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_parking_1_tview", "GPIN")

# Get the fields from the input
fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "PARKING_AREA", "[dissolve_parking_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up

#----------------------------------------------------------------------------------------------------
# Road area
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_road_1_tview", "GPIN")

# Get the fields from the input
fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "ROAD_AREA", "[dissolve_road_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up

#----------------------------------------------------------------------------------------------------
# slab
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_slab_1_tview", "GPIN")

# Get the fields from the input
fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "SLAB_AREA", "[dissolve_slab_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up
#----------------------------------------------------------------------------------------------------
# structure
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_structure_1_tview", "GPIN")

# Get the fields from the input
fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "STRUCTURE_AREA", "[dissolve_structure_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up

#----------------------------------------------------------------------------------------------------
# walkway
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_walkway_1_tview", "GPIN")

# Get the fields from the input
fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "WALKWAY_AREA", "[dissolve_walkway_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up

# Copy the layer to a new permanent feature class
# arcpy.CopyFeatures_management(layerName, outFeature)
#----------------------------------------------------------------------------------------------------
# sidewalk
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_sidewalk_1_tview", "GPIN")

# Get the fields from the input
fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "SIDEWALK_AREA", "[dissolve_sidewalk_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up

#----------------------------------------------------------------------------------------------------
# railroad_area
# Purpose: "AddJoin" Joins a table to a featureclass and select the desired attributes

# Set environment settings
arcpy.workspace = "\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb"

# Join the feature layer to a table
arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", "dissolve_railroad_1_tview", "GPIN")

# Get the fields from the input
fields = arcpy.ListFields("FINAL_IMP_POINTS_tview")
field_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
print field_names

# Process: Calculate Field
arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", "RAILROAD_AREA", "[dissolve_railroad_1.SHAPE_Area]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview") # might speed things up


#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
# use CopyRows to copy the tables in a folder to a file geodatabase.
arcpy.CopyRows_management("FINAL_IMP_POINTS_tview", FINAL_IMP_BREAKOUT)

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

# consider preserving points to do dissolve (would need to use layer views instead of table views)
# arcpy.Copy_management("FINAL_IMP_POINTS_lview", FINAL_IMP_BREAKOUT_points)
# alternately, consider using arcpy.Statistics_analysis on table instead of points and dissolve
