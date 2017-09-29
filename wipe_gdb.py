import arcpy

def wipe_gdb(gdb):
  '''Deletes everything in a geodatabase'''
  arcpy.env.workspace = gdb

  for x in arcpy.ListDatasets():
    arcpy.Delete_management(x)


wipe_gdb(r'C:\Users\brownr\Desktop\imperv\data\imp.gdb')