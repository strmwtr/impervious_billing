# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# IMP_1_TOTAL_AREA.py
# Created on: 2013-10-11 09:45:31.00000
#   (created by Mark Simpson)
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

arcpy.env.workspace = "r\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb"
arcpy.env.overwriteOutput = True

sde =  "Database Connections\\CVGISWEB_Connection to GISPRDDB.sde"

# Local variables:
cvgis_CITY_parcel_area = sde + "\\cvgis.CITY.Cadastre\\cvgis.CITY.parcel_area"
cvgis_CITY_slab_area = sde + "\\cvgis.CITY.Buildings\\cvgis.CITY.slab_area"
cvgis_CITY_structure_existing_area = sde + "\\cvgis.CITY.Buildings\\cvgis.CITY.structure_existing_area"
cvgis_CITY_miscellaneous_building_area = sde + "\\cvgis.CITY.Buildings\\cvgis.CITY.miscellaneous_building_area"
cvgis_CITY_pedestrian_walkway_area = sde + "\\cvgis.CITY.Transportation_Other\\cvgis.CITY.pedestrian_walkway_area"
cvgis_CITY_road_area = sde + "\\cvgis.CITY.Transportation_Road\\cvgis.CITY.road_area_master"
cvgis_CITY_vehicle_driveway_area= sde + "\\cvgis.CITY.Transportation_Other\\cvgis.CITY.vehicle_driveway_area"
cvgis_CITY_vehicle_parking_area = sde + "\\cvgis.CITY.Transportation_Other\\cvgis.CITY.vehicle_parking_area"
cvgis_CITY_parcel_point = sde + "\\cvgis.CITY.Cadastre\\cvgis.CITY.parcel_point"
cvgis_CITY_pedestrian_sidewalk_area = sde + "\\cvgis.CITY.Transportation_Other\\cvgis.CITY.pedestrian_sidewalk_area"
cvgis_CITY_railroad_area = sde + "\\cvgis.CITY.Transportation_Railroad\\cvgis.CITY.railroad_area"

intersect1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\intersect1"
dissolve1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\dissolve1"
merge1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\merge1"
union1 = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\union1"
parcel_point_copy = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson.gdb\\parcel_point_copy"
FINAL_IMP_POINTS = "\\\Metanoia\geodata\IT\SIMPSON\projects\Impervious\Simpson_2.gdb\\FINAL_IMP_POINTS"

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
# Process: Copy (2)
arcpy.Copy_management(cvgis_CITY_parcel_point, parcel_point_copy, "FeatureClass")
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------


# Process: Merge
#
arcpy.Merge_management("'" + cvgis_CITY_slab_area + "';'" + cvgis_CITY_structure_existing_area + "';'" + cvgis_CITY_miscellaneous_building_area + "';'"
 + cvgis_CITY_pedestrian_walkway_area + "';'" + cvgis_CITY_railroad_area + "';'" + cvgis_CITY_pedestrian_sidewalk_area + "';'" + cvgis_CITY_road_area + "';'" + cvgis_CITY_vehicle_driveway_area + "';'" + cvgis_CITY_vehicle_parking_area + "';'"
 + "'", merge1)

# Process: Union
arcpy.Union_analysis(merge1, union1, "ALL", "", "GAPS")

# Process: Intersect
arcpy.Intersect_analysis([cvgis_CITY_parcel_area, union1], intersect1, "ALL", "", "INPUT")

# Process: Dissolve
arcpy.Dissolve_management(intersect1, dissolve1, "GPIN", "", "MULTI_PART", "DISSOLVE_LINES")

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
# Process: Join Field
arcpy.JoinField_management(parcel_point_copy, "PARCELSPOL", dissolve1, "GPIN", "")

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

# Process: Add Field (PIN)
arcpy.AddField_management(parcel_point_copy, "PIN", "TEXT", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field (PIN)
arcpy.CalculateField_management(parcel_point_copy, "PIN", "[PROP_ID]", "VB", "")

# Process: Add Field (Total Area)
arcpy.AddField_management(parcel_point_copy, "TOTAL_IMP_AREA", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field (calculate Total IMP area)
arcpy.CalculateField_management(parcel_point_copy, "TOTAL_IMP_AREA", "[Shape_Area]", "VB", "")

# Process: Add Field (Structure_Area)
arcpy.AddField_management(parcel_point_copy, "STRUCTURE_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (Slab)
arcpy.AddField_management(parcel_point_copy, "SLAB_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (misc struct)
arcpy.AddField_management(parcel_point_copy, "MISC_STRUCT_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (vehicle parking)
arcpy.AddField_management(parcel_point_copy, "PARKING_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (vehicle driveway)
arcpy.AddField_management(parcel_point_copy, "DRIVEWAY_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (sidewalk)
arcpy.AddField_management(parcel_point_copy, "SIDEWALK_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (walkway)
arcpy.AddField_management(parcel_point_copy, "WALKWAY_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (road_area)
arcpy.AddField_management(parcel_point_copy, "ROAD_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (railroad_area)
arcpy.AddField_management(parcel_point_copy, "RAILROAD_AREA", "DOUBLE", "", "", "15", "", "NULLABLE", "NON_REQUIRED", "")


#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

# Process: Remove Join
#arcpy.RemoveJoin_management(parcel_point_copy) # might speed things up

# Process: Copy out to final point featureclass
arcpy.Copy_management(parcel_point_copy, FINAL_IMP_POINTS, "")


