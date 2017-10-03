#Import modules
import arcpy
import wipe_gdb

#Set environments 
gdb = r'C:\Users\brownr\Desktop\imperv\data\imp.gdb'
sde = r'Database Connections\Connection to GISPRDDB direct connect.sde'

arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

#Clears gdb, can be taken out after development is done
wipe_gdb.wipe(gdb)

#Data pointers
sde_parcel_area = sde + r'\cvgis.CITY.Cadastre\cvGIS.CITY.parcel_area'
sde_parcel_point = sde + r'\cvgis.CITY.Cadastre\cvgis.CITY.parcel_point'

#Output names
intersect1 = gdb + r'\intersect1'
dissolve1 = gdb + r'\dissolve1'
all_imp = gdb + r'\all_imp'
union1 = gdb + r'\union1'
gdb_parcel_point = gdb + r'\parcel_point'
FINAL_IMP_POINTS = gdb + r'\FINAL_IMP_POINTS'
FINAL_IMP_BREAKOUT = gdb + r'\FINAL_IMP_BREAKOUT'


#Copy Parcel points to gdb
arcpy.CopyFeatures_management(sde_parcel_point, gdb_parcel_point)

# Merge all impervious layers into all_imp
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

arcpy.Merge_management(imp_list, all_imp)

arcpy.Union_analysis(all_imp, union1, "ALL", "", "GAPS")

arcpy.Intersect_analysis([sde_parcel_area, union1], intersect1, "ALL", 
  "", "INPUT")

arcpy.Dissolve_management(intersect1, dissolve1, "GPIN", "", "MULTI_PART", 
  "DISSOLVE_LINES")

arcpy.JoinField_management(gdb_parcel_point, "PARCELSPOL", dissolve1, "GPIN", 
  "")

arcpy.AddField_management(gdb_parcel_point, "PIN", "TEXT", "", "", "15", "", 
  "NULLABLE", "NON_REQUIRED", "")

arcpy.CalculateField_management(gdb_parcel_point, "PIN", "[PROP_ID]", "VB", 
  "")

add_fields = ["STRUCTURE_AREA", "SLAB_AREA", "MISC_STRUCT_AREA", 
  "PARKING_AREA", "DRIVEWAY_AREA", "SIDEWALK_AREA", "WALKWAY_AREA","ROAD_AREA",
  "RAILROAD_AREA"]

for field in add_fields:
  arcpy.AddField_management(gdb_parcel_point, field, "DOUBLE", "", 
  "", "15", "", "NULLABLE", "NON_REQUIRED", "")

arcpy.AddField_management(gdb_parcel_point, "TOTAL_IMP_AREA", "DOUBLE", "", 
  "", "", "", "NULLABLE", "NON_REQUIRED", "")

arcpy.CalculateField_management(gdb_parcel_point, "TOTAL_IMP_AREA", 
  "[Shape_Area]", "VB", "")

# Process: Remove Join
#arcpy.RemoveJoin_management(gdb_parcel_point) # might speed things up

# Process: Copy out to final point featureclass
arcpy.Copy_management(gdb_parcel_point, FINAL_IMP_POINTS, "")

# Script 2

#This line is from script 3
arcpy.MakeTableView_management(FINAL_IMP_POINTS, "FINAL_IMP_POINTS_tview")

for feat in imp_list:
  feat_name = feat.split('.')[-1]
  inte = gdb + '\\' + feat_name + '_int'
  dis = gdb + '\\' + feat_name + '_dis'
  tview = feat + '_tview'
  #calc_field = "{0}_dis.Shape_Area".format(feat_name)

  arcpy.Intersect_analysis([feat, sde_parcel_area], inte)
  arcpy.Dissolve_management(inte, dis, ["GPIN"], "","MULTI_PART", 
  "DISSOLVE_LINES")

  arcpy.AddField_management(dis, add_fields[imp_list.index(feat)], "DOUBLE", "", 
  "", "15", "", "NULLABLE", "NON_REQUIRED", "")  
  arcpy.CalculateField_management(dis, add_fields[imp_list.index(feat)], 
  "[Shape_Area]", "VB")
  '''
  #Scipt 3
  arcpy.MakeTableView_management(dis, tview)
  arcpy.AddJoin_management("FINAL_IMP_POINTS_tview", "PARCELSPOL", 
  tview, "GPIN")

  tblv_names = [f.name for f in arcpy.ListFields("FINAL_IMP_POINTS_tview")]
  print tblv_names

  updated_field = "FINAL_IMP_POINTS."+add_fields[imp_list.index(feat)]
  source_field = "{0}_dis.".format(feat_name)+add_fields[imp_list.index(feat)]
  print updated_field, '\n', source_field, '\n'

  arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", updated_field, 
  source_field, "VB")

  arcpy.CopyRows_management("FINAL_IMP_POINTS_tview", dis+'_tbl')
  arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview")
  
  if calc_field in tblv_names:
    print "Yes", calc_field
    #arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", add_fields[imp_list.index(feat)], '[LOTSQFT]', "VB")
    #arcpy.CalculateField_management("FINAL_IMP_POINTS_tview", add_fields[imp_list.index(feat)], calc_field, "VB")
    
    arcpy.CopyRows_management("FINAL_IMP_POINTS_tview", dis+'_tbl')
    arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview")
  else:
    print "No", calc_field, '\n', tblv_names
    arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview")
  '''
  '''
  arcpy.CalculateField_management("FINAL_IMP_POINTS_tview",
  add_fields[imp_list.index(feat)], calc_field, "VB")
  arcpy.RemoveJoin_management("FINAL_IMP_POINTS_tview")
  '''
#arcpy.CopyRows_management("FINAL_IMP_POINTS_tview", FINAL_IMP_BREAKOUT)
