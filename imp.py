#Import modules
import arcpy
import gdb_tools

#Set environments 
#Databases
gdb = r'J:\CITYWIDE\Utilities\Stormwater Utility\GIS\Impervious\Impervious.gdb'
sde = r'Database Connections\Connection to GISPRDDB direct connect.sde'

arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

#Data pointers
sde_parcel_area = sde + r'\cvgis.CITY.Cadastre\cvGIS.CITY.parcel_area'
sde_parcel_point = sde + r'\cvgis.CITY.Cadastre\cvgis.CITY.parcel_point'

#List of all impervious surfaces
imp_list = [
  sde+r'\cvgis.CITY.Buildings\cvgis.CITY.structure_existing_area',
  sde+r'\cvgis.CITY.Buildings\cvgis.CITY.slab_area',  
  sde+r'\cvgis.CITY.Buildings\cvgis.CITY.miscellaneous_building_area',
  sde+r'\cvgis.CITY.Transportation_Other\cvgis.CITY.vehicle_parking_area',
  sde+r'\cvgis.CITY.Transportation_Other\cvgis.CITY.vehicle_driveway_area',
  sde+r'\cvgis.CITY.Transportation_Other\cvgis.CITY.pedestrian_sidewalk_area',
  sde+r'\cvgis.CITY.Transportation_Other\cvgis.CITY.pedestrian_walkway_area',
  sde+r'\cvgis.CITY.Transportation_Road\cvgis.CITY.road_area_master',
  sde+r'\cvgis.CITY.Transportation_Railroad\cvgis.CITY.railroad_area',
  ]

#Output names
intersect = gdb + r'\intersect'
dissolve = gdb + r'\dissolve'
imperv = gdb + r'\imperv'
union = gdb + r'\union_del'
parcel_point = gdb + r'\parcel_point'
imp_points = gdb + r'\imp_points'
final_table = gdb + r'\IMPERVIOUS_AREA'

imp_fields = ["STRUCTURE_AREA", "SLAB_AREA", "MISC_STRUCT_AREA", 
  "PARKING_AREA", "DRIVEWAY_AREA", "SIDEWALK_AREA", "WALKWAY_AREA","ROAD_AREA",
  "RAILROAD_AREA"]

def data_prep():
  #Copy Parcel points to gdb
  arcpy.CopyFeatures_management(sde_parcel_point, parcel_point)
  #Merge imp_list to create imperv
  arcpy.Merge_management(imp_list, imperv)
  #Union imperv to create union
  arcpy.Union_analysis(imperv, union, "ALL", "", "GAPS")
  #Intersect parcel polygons with union, create intersect feature
  arcpy.Intersect_analysis([sde_parcel_area, union], intersect, "ALL", 
    "", "INPUT")
  #Disolve intersect around GPIN, create dissolve feature
  arcpy.Dissolve_management(intersect, dissolve, "GPIN", "", "MULTI_PART", 
    "DISSOLVE_LINES")
  #Join parcel points with dissolve
  arcpy.JoinField_management(parcel_point, "PARCELSPOL", dissolve, "GPIN", 
    "")
  #Add PIN to join listed above
  arcpy.AddField_management(parcel_point, "PIN", "TEXT", "", "", "15", "", 
    "NULLABLE", "NON_REQUIRED", "")
  #Populate PIN with PROP_ID field
  arcpy.CalculateField_management(parcel_point, "PIN", "[PROP_ID]", "VB", 
    "")
  #Add TOTAL_IMP_AREA field
  arcpy.AddField_management(parcel_point, "TOTAL_IMP_AREA", "DOUBLE", "", 
    "", "", "", "NULLABLE", "NON_REQUIRED", "")
  #Populate TOTAL_IMP_AREA as shape area of all impervious 
  arcpy.CalculateField_management(parcel_point, "TOTAL_IMP_AREA", 
    "[Shape_Area]", "VB", "")
  #Export joins to imp_points
  arcpy.Copy_management(parcel_point, imp_points)

def gen_imp_tbl():
  #For each feature in imp_list
  for feat in imp_list:
    #Feature name
    feat_name = feat.split('.')[-1]
    #Intersect output path
    inte = gdb + '\\' + feat_name + '_int'
    #Disolve output path
    dis = gdb + '\\' + feat_name + '_dis'
    #Field to join on 
    current_field = imp_fields[imp_list.index(feat)]

    #Intersect feature and sde parcel area
    arcpy.Intersect_analysis([feat, sde_parcel_area], inte)
    #Disolve around GPIN
    arcpy.Dissolve_management(inte, dis, ["GPIN"], "","MULTI_PART", 
    "DISSOLVE_LINES")
    #Add current_field to intersect
    arcpy.AddField_management(dis, current_field, "DOUBLE", "", "", "15", "", 
    "NULLABLE", "NON_REQUIRED", "")
    #Populate current_field with representative impervious area 
    arcpy.CalculateField_management(dis, current_field,"[Shape_Area]", "VB")
    #Join imp_points with feature
    arcpy.JoinField_management(imp_points, 'PARCELSPOL', dis, 
    'GPIN', current_field)
  #Create IMPERVIOUS_AREA table
  arcpy.CopyRows_management(imp_points, final_table)

def clean():
  all_fields = [f.name for f in arcpy.ListFields(final_table)]
  keep_fields = ['OBJECTID', 'PIN', 'GPIN', 'TOTAL_IMP_AREA'] + imp_fields
  for field in all_fields:
    if field not in  keep_fields:
      print field
      arcpy.DeleteField_management(final_table, field)

#Cleans GDB
gdb_tools.wipe(gdb)
data_prep()
gen_imp_tbl()
clean()