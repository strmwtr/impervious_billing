#Import modules
import arcpy
import gdb_tools
import datetime

#Set environments 
#Databases
gdb = r'\\metanoia\geodata\PW\sw_tech\Impervious\Impervious.gdb'
sde = r'Database Connections\Connection to GISPRDDB direct connect.sde'
arc_gdb = r'\\metanoia\geodata\PW\sw_tech\Impervious\Impervious_Archive.gdb'

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

#Get data as string and replace - with _
str_today = str(datetime.date.today()).replace('-','_')

#Output names
intersect = gdb + r'\intersect'
dissolve = gdb + r'\dissolve'
imperv = gdb + r'\imperv'
union_out = gdb + r'\union_out'
parcel_point = gdb + r'\parcel_point'
imp_points = gdb + r'\imp_points'
final_table = arc_gdb + r'\IMPERVIOUS_AREA_{0}'.format(str_today)

imp_fields = ['STRUCTURE_AREA', 'SLAB_AREA', 'MISC_STRUCT_AREA', 
  'PARKING_AREA', 'DRIVEWAY_AREA', 'SIDEWALK_AREA', 'WALKWAY_AREA','ROAD_AREA',
  'RAILROAD_AREA']

def data_prep():
  #If final_table already exists, delete it
  gdb_tools.check_del(arc_gdb, final_table)
  #Copy Parcel points to gdb
  arcpy.CopyFeatures_management(sde_parcel_point, parcel_point)
  #Merge imp_list to create imperv
  arcpy.Merge_management(imp_list, imperv)
  #Union imperv to create union_out
  arcpy.Union_analysis(imperv, union_out)
  #Intersect parcel polygons with union_out, create intersect feature
  arcpy.Intersect_analysis([sde_parcel_area, union_out], intersect)
  #Disolve intersect around GPIN, create dissolve feature
  arcpy.Dissolve_management(intersect, dissolve, 'GPIN')
  #Join parcel points with dissolve
  arcpy.JoinField_management(parcel_point, 'PARCELSPOL', dissolve, 'GPIN')
  #Add PIN to join listed above
  arcpy.AddField_management(parcel_point, 'PIN', 'TEXT', '', '', '15')
  #Populate PIN with PROP_ID field
  arcpy.CalculateField_management(parcel_point, 'PIN', '[PROP_ID]', 'VB')
  #Add TOTAL_IMP_AREA field
  arcpy.AddField_management(parcel_point, 'TOTAL_IMP_AREA', 'DOUBLE')
  #Populate TOTAL_IMP_AREA as shape area of all impervious 
  arcpy.CalculateField_management(parcel_point, 'TOTAL_IMP_AREA', 
  '[Shape_Area]', 'VB')
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
    arcpy.Dissolve_management(inte, dis, ['GPIN'])
    #Add current_field to intersect
    arcpy.AddField_management(dis, current_field, 'DOUBLE', '', '', '15')
    #Populate current_field with representative impervious area 
    arcpy.CalculateField_management(dis, current_field,'[Shape_Area]', 'VB')
    #Join imp_points with feature
    arcpy.JoinField_management(imp_points, 'PARCELSPOL', dis, 
    'GPIN', current_field)
  #Create IMPERVIOUS_AREA table
  arcpy.CopyRows_management(imp_points, final_table)

def clean():
  #Deletes all fields other than imp_fields and the pin/gpin/total/objectid
  #Generates field names
  all_fields = [f.name for f in arcpy.ListFields(final_table)]
  #All the fields that should not be deleted
  keep_fields = ['OBJECTID', 'PIN', 'GPIN', 'TOTAL_IMP_AREA'] + imp_fields
  #If a field in all_fields is not in keep_fields, delete it
  for field in all_fields:
    if field not in  keep_fields:
      arcpy.DeleteField_management(final_table, field)

def null_to_zero():
  #Changes null values to zeros
  #imp_fields plus Total_IMP_AREA field
  update_fields = imp_fields + ['TOTAL_IMP_AREA']
  #Create cursor for values of update_fields
  with arcpy.da.UpdateCursor(final_table, update_fields) as cursor:
    #For each row in the cursor, if value is None, change value to 0
    for row in cursor:
      indices = [i for i, x in enumerate(row) if x == None]
      for val in indices:
        row[val] = 0
      cursor.updateRow(row)

def delta_calcs():
  #Add these fields to table
  more_fields = ['SUM_IMP', 'DELTA']
  #Generate sum equation
  sum_fields = ''
  for x in imp_fields:
    sum_fields = sum_fields + '[{0}]+'.format(x)
  sum_fields = sum_fields[:-1]
  #Add fields from more_fields
  for field in more_fields:
    arcpy.AddField_management(final_table, field, 'DOUBLE')
  #Calculate SUM_IMP with sum_fields equation
  arcpy.CalculateField_management(final_table, 'SUM_IMP', sum_fields, 'VB')
  #Calculate DELTA as TOTAL_IMP_AREA-SUM_IMP
  arcpy.CalculateField_management(final_table, 'DELTA', 
  '[TOTAL_IMP_AREA] - [SUM_IMP]', 'VB')
  
gdb_tools.wipe(gdb)
data_prep()
gen_imp_tbl()
clean()
null_to_zero()
delta_calcs()