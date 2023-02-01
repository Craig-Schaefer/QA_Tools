# Import needed python packages
from datetime import timedelta, date
import os, re, arcpy
import pandas as pd
# Set Arc to allow data overwriting
arcpy.env.overwriteOutput = True
# Set Arc to allow data overwriting
arcpy.SetLogHistory(False)
# Assign today's date to a variable
today_date = date.today()
# Define the ArcGIS Pro workspace/project and assign to variable
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Assign local path components to variables
rootpath = r"C:"
topfolder = r"\QAQC"
secondfolder = r"\Storm"
otherfolder = r"\Sewer"
nextfolder = r"\Water"

# Assign netowrk path(s) to Excel file(s) to variable(s)  "COPY FROM"
stormexceptionfileTemplate = r"\\cityoftulsa\eng\EngAtlas\Gw5320\usr5\wpdata\graphics\QAQC\Storm\Storm_QAQC_Exceptions.xlsx"
stormconfigurationfileTemplate = r"\\cityoftulsa\eng\EngAtlas\Gw5320\usr5\wpdata\graphics\QAQC\Storm\Storm_QAQC_Configuration.xlsx"

sewerexceptionfileTemplate = r"\\cityoftulsa\eng\EngAtlas\Gw5320\usr5\wpdata\graphics\QAQC\Sewer\Sewer_QAQC_Exceptions.xlsx"
sewerconfigurationfileTemplate = r"\\cityoftulsa\eng\EngAtlas\Gw5320\usr5\wpdata\graphics\QAQC\Sewer\Sewer_QAQC_Configuration.xlsx"

waterexceptionfileTemplate = r"\\cityoftulsa\eng\EngAtlas\Gw5320\usr5\wpdata\graphics\QAQC\Water\Water_QAQC_Exceptions.xlsx"
waterconfigurationfileTemplate = r"\\cityoftulsa\eng\EngAtlas\Gw5320\usr5\wpdata\graphics\QAQC\Water\Water_QAQC_Configuration.xlsx"

# Define the local Excel path and assign to variable   "COPY TO"
stormconfigurationfile = rootpath + topfolder + secondfolder + r"\Storm_QAQC_Configuration.xlsx"
stormexceptionfile = rootpath + topfolder + secondfolder + r"\Storm_QAQC_Exceptions.xlsx"

sewerconfigurationfile = rootpath + topfolder + otherfolder + r"\Sewer_QAQC_Configuration.xlsx"
sewerexceptionfile = rootpath + topfolder + otherfolder + r"\Sewer_QAQC_Exceptions.xlsx"

waterconfigurationfile = rootpath + topfolder + nextfolder + r"\Water_QAQC_Configuration.xlsx"
waterexceptionfile = rootpath + topfolder + nextfolder + r"\Water_QAQC_Exceptions.xlsx"

# Check for local path and create if doesn't exist
if arcpy.Exists(rootpath + topfolder):
    print("The local path " + rootpath + topfolder + " already exists")
else:
    arcpy.CreateFolder_management(rootpath, topfolder)
    print("Created local path " + rootpath + topfolder)
if arcpy.Exists(rootpath + topfolder + secondfolder):
    print("The local path " + rootpath + topfolder + secondfolder + " already exists")
else:
    arcpy.CreateFolder_management(rootpath + topfolder, secondfolder)
    print("Created local path " + rootpath + topfolder + secondfolder)
if arcpy.Exists(rootpath + topfolder + otherfolder):
    print("The local path " + rootpath + topfolder + otherfolder + " already exists")
else:
    arcpy.CreateFolder_management(rootpath + topfolder, otherfolder)
    print("Created local path " + rootpath + topfolder + otherfolder)
if arcpy.Exists(rootpath + topfolder + nextfolder):
    print("The local path " + rootpath + topfolder + nextfolder + " already exists")
else:
    arcpy.CreateFolder_management(rootpath + topfolder, nextfolder)
    print("Created local path " + rootpath + topfolder + nextfolder)

# Checks for existing Excel files on local drive, and pulls over copies from the network if missing
if arcpy.Exists(stormconfigurationfile):
    print("The file (and path) " + stormconfigurationfile + " already exists")
else:
    arcpy.management.Copy(stormconfigurationfileTemplate, stormconfigurationfile)
    print("Created file (at path) "+ stormconfigurationfile)	
if arcpy.Exists(stormexceptionfile):
    print("The file (and path) " + stormexceptionfile + " already exists")
else:
    arcpy.management.Copy(stormexceptionfileTemplate, stormexceptionfile)
    print("Created file (at path) "+ stormexceptionfile)
if arcpy.Exists(sewerconfigurationfile):
    print("The file (and path) " + sewerconfigurationfile + " already exists")
else:
    arcpy.management.Copy(sewerconfigurationfileTemplate, sewerconfigurationfile)
    print("Created file (at path) "+ sewerconfigurationfile)	
if arcpy.Exists(sewerexceptionfile):
    print("The file (and path) " + sewerexceptionfile + " already exists")
else:
    arcpy.management.Copy(sewerexceptionfileTemplate, sewerexceptionfile)
    print("Created file (at path) "+ sewerexceptionfile)
if arcpy.Exists(waterconfigurationfile):
    print("The file (and path) " + waterconfigurationfile + " already exists")
else:
    arcpy.management.Copy(waterconfigurationfileTemplate, waterconfigurationfile)
    print("Created file (at path) "+ waterconfigurationfile)	
if arcpy.Exists(waterexceptionfile):
    print("The file (and path) " + waterexceptionfile + " already exists")
else:
    arcpy.management.Copy(waterexceptionfileTemplate, waterexceptionfile)
    print("Created file (at path) "+ waterexceptionfile)

# Iterate through all Maps extant within the defined ArcGIS Pro workspace/project, and append all unique Layer names to a list
layerlist = []
for m in aprx.listMaps():
	print("Map: " + m.name)
	for lyr in m.listLayers():
		print("trying "+str(lyr))
		try:
			if str(lyr.name) not in layerlist:
				layerlist.append(str(lyr.name))
				print("added "+(str(lyr)))
			else:
				print((str(lyr.name))+" already in layerlist")
		except:
			print("Couldn't add "+str(lyr))
print(layerlist)

#create empty liat to be populated with ALL possible QAQC layers from the user's workspace
inclusionlayerlist = []

#create empty liats to be populated with all possible STORM QAQC layers from the user's workspace
stormOverallQueryLayerList=[]
stormManholeQueryLayerList=[]
stormManhole_ABQueryLayerList=[]
stormDischargePointsQueryLayerList=[]
stormDischargePoint_ABQueryLayerList=[]
stormGravityMainQueryLayerList=[]
stormGravityMains_ABQueryLayerList=[]
stormInletQueryLayerList=[]
stormInlet_ABQueryLayerList=[]
stormCleanOutQueryLayerList=[]
stormCleanOut_ABQueryLayerList=[]
stormControlValveQueryLayerList=[]
stormControlValve_ABQueryLayerList=[]
stormFitting_ABQueryLayerList=[]
stormFittingQueryLayerList=[]
stormDetention_ABQueryLayerList=[]
stormDetentionQueryLayerList=[]
stormNetworkStructure_ABQueryLayerList=[]
stormNetworkStructureQueryLayerList=[]
stormSystemValve_ABQueryLayerList=[]
stormSystemValveQueryLayerList=[]
stormWeirStructure_ABQueryLayerList=[]
stormWeirStructureQueryLayerList=[]


#create empty liats to be populated with all possible SEWER QAQC layers from the user's workspace
sewerOverallQueryLayerList=[]
sewerManholeQueryLayerList=[]
sewerGravityMainQueryLayerList=[]

#create empty liats to be populated with all possible WATER QAQC layers from the user's workspace
waterOverallQueryLayerList=[]
waterSysvalveQueryLayerList=[]
waterHydrantQueryLayerList=[]
waterMainQueryLayerList=[]
waterFittingQueryLayerList=[]
largemeterQueryLayerList=[]

layers = aprx.listMaps()[0].listLayers()[0:200]

for layer in layers:
	print("trying "+str(layer))
	try:	
		layer_metadata = layer.metadata
		print("Metadata Title for "+str(layer)+" is "+str(layer_metadata.title))
		try:
			if str(layer_metadata.title) == "swMains":
				print (str(layer)+" is swGravityMain")
				stormGravityMainQueryLayers=str(layer)+"-swGravityMain"
				if stormGravityMainQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormGravityMainQueryLayers)
				if str(layer) not in stormGravityMainQueryLayerList:
					stormGravityMainQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swMains_AB"):
				print (str(layer)+" is swMains_AB")
				stormGravityMains_ABQueryLayers=str(layer)+"-swMains_AB"
				if stormGravityMains_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormGravityMains_ABQueryLayers)
				if str(layer) not in stormGravityMains_ABQueryLayerList:
					stormGravityMains_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swManhole"):
				print (str(layer)+" is swManhole")
				stormManholeQueryLayers=str(layer)+"-swManhole"
				if stormManholeQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormManholeQueryLayers)
				if str(layer) not in stormManholeQueryLayerList:
					stormManholeQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swDischargePoint"):
				print (str(layer)+" is swDischargePoint")
				stormDischargePointsQueryLayers=str(layer)+"-swDischargePoint"
				if stormDischargePointsQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormDischargePointsQueryLayers)
				if str(layer) not in stormDischargePointsQueryLayerList:
					stormDischargePointsQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swInlet"):
				print (str(layer)+" is swInlet")
				stormInletQueryLayers=str(layer)+"-swInlet"
				if stormInletQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormInletQueryLayers)
				if str(layer) not in stormInletQueryLayerList:
					stormInletQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swCleanOut"):
				print (str(layer)+" is swCleanOut")
				stormCleanOutQueryLayers=str(layer)+"-swCleanOut"
				if stormCleanOutQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormCleanOutQueryLayers)
				if str(layer) not in stormCleanOutQueryLayerList:
					stormCleanOutQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swCleanOut_AB"):
				print (str(layer)+" is swCleanOut_AB")
				stormCleanOut_ABQueryLayers=str(layer)+"-swCleanOut_AB"
				if stormCleanOut_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormCleanOut_ABQueryLayers)
				if str(layer) not in stormCleanOut_ABQueryLayerList:
					stormCleanOut_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swControlValve"):
				print (str(layer)+" is swControlValve")
				stormControlValveQueryLayers=str(layer)+"-swControlValve"
				if stormControlValveQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormControlValveQueryLayers)
				if str(layer) not in stormControlValveQueryLayerList:
					stormControlValveQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swControlValve_AB"):
				print (str(layer)+" is swControlValve_AB")
				stormControlValve_ABQueryLayers=str(layer)+"-swControlValve_AB"
				if stormControlValve_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormControlValve_ABQueryLayers)
				if str(layer) not in stormControlValve_ABQueryLayerList:
					stormControlValve_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swFitting"):
				print (str(layer)+" is swFitting")
				stormFittingQueryLayers=str(layer)+"-swFitting"
				if stormFittingQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormFittingQueryLayers)
				if str(layer) not in stormFittingQueryLayerList:
					stormFittingQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swFitting_AB"):
				print (str(layer)+" is swFitting_AB")
				stormFitting_ABQueryLayers=str(layer)+"-swFitting_AB"
				if stormFitting_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormFitting_ABQueryLayers)
				if str(layer) not in stormFitting_ABQueryLayerList:
					stormFitting_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swManhole_AB"):
				print (str(layer)+" is swManhole_AB")
				stormManhole_ABQueryLayers=str(layer)+"-swManhole_AB"
				if stormManhole_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormManhole_ABQueryLayers)
				if str(layer) not in stormManhole_ABQueryLayerList:
					stormManhole_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swInlet_AB"):
				print (str(layer)+" is swInlet_AB")
				stormInlet_ABQueryLayers=str(layer)+"-swInlet_AB"
				if stormInlet_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormInlet_ABQueryLayers)
				if str(layer) not in stormInlet_ABQueryLayerList:
					stormInlet_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swDetention"):
				print (str(layer)+" is swDetention")
				stormDetentionQueryLayers=str(layer)+"-swDetention"
				if stormDetentionQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormDetentionQueryLayers)
				if str(layer) not in stormDetentionQueryLayerList:
					stormDetentionQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swDetention_AB"):
				print (str(layer)+" is swDetention_AB")
				stormDetention_ABQueryLayers=str(layer)+"-swDetention_AB"
				if stormDetention_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormDetention_ABQueryLayers)
				if str(layer) not in stormDetention_ABQueryLayerList:
					stormDetention_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swDischargePoint_AB"):
				print (str(layer)+" is swDischargePoint_AB")
				stormDischargePoint_ABQueryLayers=str(layer)+"-swDischargePoint_AB"
				if stormDischargePoint_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormDischargePoint_ABQueryLayers)
				if str(layer) not in stormDischargePoint_ABQueryLayerList:
					stormDischargePoint_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swNetworkStructure"):
				print (str(layer)+" is swNetworkStructure")
				stormNetworkStructureQueryLayers=str(layer)+"-swNetworkStructure"
				if stormNetworkStructureQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormNetworkStructureQueryLayers)
				if str(layer) not in stormNetworkStructureQueryLayerList:
					stormNetworkStructureQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swNetworkStructure_AB"):
				print (str(layer)+" is swNetworkStructure_AB")
				stormNetworkStructure_ABQueryLayers=str(layer)+"-swNetworkStructure_AB"
				if stormNetworkStructure_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormNetworkStructure_ABQueryLayers)
				if str(layer) not in stormNetworkStructure_ABQueryLayerList:
					stormNetworkStructure_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swSystemValve"):
				print (str(layer)+" is swSystemValve")
				stormSystemValveQueryLayers=str(layer)+"-swSystemValve"
				if stormSystemValveQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormSystemValveQueryLayers)
				if str(layer) not in stormSystemValveQueryLayerList:
					stormSystemValveQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swSystemValve_AB"):
				print (str(layer)+" is swSystemValve_AB")
				stormSystemValve_ABQueryLayers=str(layer)+"-swSystemValve_AB"
				if stormSystemValve_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormSystemValve_ABQueryLayers)
				if str(layer) not in stormSystemValve_ABQueryLayerList:
					stormSystemValve_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swWeirStructure"):
				print (str(layer)+" is swWeirStructure")
				stormWeirStructureQueryLayers=str(layer)+"-swWeirStructure"
				if stormWeirStructureQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormWeirStructureQueryLayers)
				if str(layer) not in stormWeirStructureQueryLayerList:
					stormWeirStructureQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "swWeirStructure_AB"):
				print (str(layer)+" is swWeirStructure_AB")
				stormWeirStructure_ABQueryLayers=str(layer)+"-swWeirStructure_AB"
				if stormWeirStructure_ABQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(stormWeirStructure_ABQueryLayers)
				if str(layer) not in stormWeirStructure_ABQueryLayerList:
					stormWeirStructure_ABQueryLayerList.append(str(layer))
				if str(layer) not in stormOverallQueryLayerList:
					stormOverallQueryLayerList.append(str(layer))


					
			elif str(layer_metadata.title) == "ssMains":
				print (str(layer)+" is ssGravityMain")
				sewerGravityMainQueryLayers=str(layer)+"-ssGravityMain"
				if sewerGravityMainQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(sewerGravityMainQueryLayers)
				if str(layer) not in sewerGravityMainQueryLayerList:
					sewerGravityMainQueryLayerList.append(str(layer))
				if str(layer) not in sewerOverallQueryLayerList:
					sewerOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "ssManhole"):
				print (str(layer)+" is ssManhole")
				sewerManholeQueryLayers=str(layer)+"-ssManhole"
				if sewerManholeQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(sewerGravityMainQueryLayers)
				if str(layer) not in sewerManholeQueryLayerList:
					sewerManholeQueryLayerList.append(str(layer))
				if str(layer) not in sewerOverallQueryLayerList:
					sewerOverallQueryLayerList.append(str(layer)) 
					
			elif str(layer_metadata.title) == "wMains":
				print (str(layer)+" is wMains")
				waterMainQueryLayers=str(layer)+"-wMains"
				if waterMainQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(waterMainQueryLayers)
				if str(layer) not in waterMainQueryLayerList:
					waterMainQueryLayerList.append(str(layer))
				if str(layer) not in waterOverallQueryLayerList:
					waterOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "wSystemValve"):
				print (str(layer)+" is wSystemValve")
				waterSysvalveQueryLayers=str(layer)+"-wSystemValve"
				if waterSysvalveQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(waterSysvalveQueryLayers)
				if str(layer) not in waterSysvalveQueryLayerList:
					waterSysvalveQueryLayerList.append(str(layer))
				if str(layer) not in waterOverallQueryLayerList:
					waterOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "wLargeMeter"):
				print (str(layer)+" is wLargeMeter")
				waterLargeMetersQueryLayers=str(layer)+"-wLargeMeter"
				if waterLargeMetersQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(waterLargeMetersQueryLayers)
				if str(layer) not in largemeterQueryLayerList:
					largemeterQueryLayerList.append(str(layer))
				if str(layer) not in waterOverallQueryLayerList:
					waterOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "wHydrant"):
				print (str(layer)+" is wHydrant")
				waterHydrantQueryLayers=str(layer)+"-wHydrant"
				if waterHydrantQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(waterHydrantQueryLayers)
				if str(layer) not in waterHydrantQueryLayerList:
					waterHydrantQueryLayerList.append(str(layer))
				if str(layer) not in waterOverallQueryLayerList:
					waterOverallQueryLayerList.append(str(layer))
			elif (str(layer_metadata.title) == "wFitting"):
				print (str(layer)+" is wFitting")
				waterFittingQueryLayers=str(layer)+"-wFitting"
				if waterFittingQueryLayers not in inclusionlayerlist:
					inclusionlayerlist.append(waterFittingQueryLayers)
				if str(layer) not in waterFittingQueryLayerList:
					waterFittingQueryLayerList.append(str(layer))
				if str(layer) not in waterOverallQueryLayerList:
					waterOverallQueryLayerList.append(str(layer))
			
			else:
				print (str(layer)+" will not be queried")
		except:
			print("Could not parse "+str(layer))
	except:
		print("Could not parse "+str(layer))
print(" ")
print("All selected layers are: ")
print(inclusionlayerlist)

print(" ")
print("All selected Storm layers are: ")
print(stormOverallQueryLayerList)
print("Selected Storm Manhole layers are: ")
print(stormManholeQueryLayerList)
print("Selected Storm Manhole_AB layers are: ")
print(stormManhole_ABQueryLayerList)
print("Selected Storm Discharge Point layers are: ")
print(stormDischargePointsQueryLayerList)
print("Selected Storm Discharge Point_AB layers are: ")
print(stormDischargePoint_ABQueryLayerList)
print("Selected Storm Gravity Main layers are: ")
print(stormGravityMainQueryLayerList)
print("Selected Storm Gravity Main_AB layers are: ")
print(stormGravityMains_ABQueryLayerList)
print("Selected Storm Inlet layers are: ")
print(stormInletQueryLayerList)
print("Selected Storm Inlet_AB layers are: ")
print(stormInlet_ABQueryLayerList)
print("Selected Storm CleanOut layers are: ")
print(stormCleanOutQueryLayerList)
print("Selected Storm CleanOut_AB layers are: ")
print(stormCleanOut_ABQueryLayerList)
print("Selected Storm Fitting layers are: ")
print(stormFittingQueryLayerList)
print("Selected Storm Fitting_AB layers are: ")
print(stormFitting_ABQueryLayerList)
print("Selected Storm ControlValve layers are: ")
print(stormControlValveQueryLayerList)
print("Selected Storm ControlValve_AB layers are: ")
print(stormControlValve_ABQueryLayerList)
print("Selected Storm Detention layers are: ")
print(stormDetentionQueryLayerList)
print("Selected Storm Detention_AB layers are: ")
print(stormDetention_ABQueryLayerList)
print("Selected Storm NetworkStructure layers are: ")
print(stormNetworkStructureQueryLayerList)
print("Selected Storm NetworkStructure_AB layers are: ")
print(stormNetworkStructure_ABQueryLayerList)
print("Selected Storm SystemValve layers are: ")
print(stormSystemValveQueryLayerList)
print("Selected Storm SystemValve_AB layers are: ")
print(stormSystemValve_ABQueryLayerList)
print("Selected Storm WeirStructure layers are: ")
print(stormWeirStructureQueryLayerList)
print("Selected Storm WeirStructure_AB layers are: ")
print(stormWeirStructure_ABQueryLayerList)


print(" ")
print("All selected Sewer layers are: ")
print(sewerOverallQueryLayerList)
print("Selected Sewer Manhole layers are: ")
print(sewerManholeQueryLayerList)
print("Selected Sewer Gravity Main layers are: ")
print(sewerGravityMainQueryLayerList)

print(" ")
print("All selected Water layers are: ")
print(waterOverallQueryLayerList)
print("Selected Water System Valve layers are: ")
print(waterSysvalveQueryLayerList)
print("Selected Water Hydrant layers are: ")
print(waterHydrantQueryLayerList)
print("Selected Water Main layers are: ")
print(waterMainQueryLayerList)
print("Selected Water Large Meter layers are: ")
print(largemeterQueryLayerList)
print("Selected Water Fitting layers are: ")
print(waterFittingQueryLayerList)

dummyWhere_clause="OBJECTID IS NULL"

for stormListedLayer in stormOverallQueryLayerList:
	print("Reviewing "+stormListedLayer)
	# Creates a list of Storm editors from Excel contents
	stormUsername_df = pd.read_excel(stormconfigurationfile, sheet_name='Configuration', usecols=str('A'))
	stormUsernamelist = stormUsername_df['Usernames'].tolist()
	# Creates a single date variable, calculated back from 'today' based upon the value in the Excel file
	stormLookbackdays_df = pd.read_excel(stormconfigurationfile, sheet_name='Configuration', usecols=str('B'))
	stormLookbackdayarray = stormLookbackdays_df['Lookback Number Of Days'].tolist()
	stormLookbackdayItem = stormLookbackdayarray[0]
	stormLookbackdays = int(stormLookbackdayItem)
	stormDateedit = today_date - timedelta(stormLookbackdays)
	stormEditdate = (str(stormDateedit))

	dummySelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=stormListedLayer, selection_type="NEW_SELECTION", where_clause=dummyWhere_clause, invert_where_clause="")
		
	for stormUsername in stormUsernamelist:		
		#print(stormUsername)
		if stormListedLayer in stormManholeQueryLayerList:
			# Creates a single stormManhole UC query variable (including stormLookbackdays-configured parameters) based upon the value in the Excel file
			stormManholeUCQuery_df = pd.read_excel(stormconfigurationfile, sheet_name='Queries', usecols=str('A'))
			stormManholeUCQueryarray = stormManholeUCQuery_df['Manholes UC'].tolist()
			stormManholeUCQueryVar = stormManholeUCQueryarray[0]
			stormManholeUCQueryItem = stormManholeUCQueryVar.format(stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate)
			#print(stormManholeUCQueryItem)
			# Creates a single stormManhole Active query variable (including stormLookbackdays-configured parameters) based upon the value in the Excel file
			stormManholeActQuery_df = pd.read_excel(stormconfigurationfile, sheet_name='Queries', usecols=str('B'))
			stormManholeActQueryarray = stormManholeActQuery_df['Manholes Active'].tolist()
			stormManholeActQueryVar = stormManholeActQueryarray[0]
			stormManholeActQueryItem = stormManholeActQueryVar.format(stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate)
			#print(stormManholeActQueryItem)
			# Creates a list of stormManhole FacilityIDs to ignore based upon the values in the Excel file
			stormManhole_df = pd.read_excel(stormexceptionfile, sheet_name='Manholes', usecols=str('A'))
			stormManholeExceptionFacIDs = stormManhole_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+stormUsername+"' And LASTUPDATE >= '"+stormEditdate+"') Or (LASTMODBY = '"+stormUsername+"' And LASTMODDATE >= '"+stormEditdate+"'))"
			stormManholeUCWhere_clause=stormManholeUCQueryItem
			stormManhole_new_ActWhere_clause=stormManholeActQueryItem			
			print("Selecting "+stormListedLayer+" where "+userDateWhere_clause+" And "+stormManholeUCWhere_clause)
			stormManholeUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+stormManholeUCWhere_clause, invert_where_clause="")
			print("Selecting "+stormListedLayer+" where "+userDateWhere_clause+" And "+stormManhole_new_ActWhere_clause)
			stormManholeActUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+stormManhole_new_ActWhere_clause, invert_where_clause="")
			for exFacID in stormManholeExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+stormListedLayer)
				stormManholeExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")
		if stormListedLayer in stormGravityMainQueryLayerList:
			# Creates a single Gravity Mains UC query variable (including stormLookbackdays-configured parameters) based upon the value in the Excel file
			stormGravityMainUCQuery_df = pd.read_excel(stormconfigurationfile, sheet_name='Queries', usecols=str('C'))
			stormGravityMainUCQueryarray = stormGravityMainUCQuery_df['GravityMains UC'].tolist()
			stormGravityMainUCQueryVar = stormGravityMainUCQueryarray[0]
			stormGravityMainUCQueryItem = stormGravityMainUCQueryVar.format(stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate)
			#print(stormGravityMainUCQueryItem)
			# Creates a single Gravity Mains Active query variable (including stormLookbackdays-configured parameters) based upon the value in the Excel file
			stormGravityMainActQuery_df = pd.read_excel(stormconfigurationfile, sheet_name='Queries', usecols=str('D'))
			stormGravityMainActQueryarray = stormGravityMainActQuery_df['GravityMains Active'].tolist()
			stormGravityMainActQueryVar = stormGravityMainActQueryarray[0]
			stormGravityMainActQueryItem = stormGravityMainActQueryVar.format(stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate)
			#print(stormGravityMainActQueryItem)
			# Creates a list of Gravity Main FacilityIDs to ignore based upon the values in the Excel file
			stormGravityMains_df = pd.read_excel(stormexceptionfile, sheet_name='GravityMains', usecols=str('A'))
			stormGravityMainExceptionFacIDs = stormGravityMains_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+stormUsername+"' And LASTUPDATE >= '"+stormEditdate+"') Or (LASTMODBY = '"+stormUsername+"' And LASTMODDATE >= '"+stormEditdate+"'))"			
			stormGravityMainUCWhere_clause=stormGravityMainUCQueryItem
			stormGravityMainActWhere_clause=stormGravityMainActQueryItem
			print("Selecting "+stormListedLayer+" where "+userDateWhere_clause+" And "+stormGravityMainUCWhere_clause)
			stormGravityMainUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+stormGravityMainUCWhere_clause, invert_where_clause="")
			print("Selecting "+stormListedLayer+" where "+userDateWhere_clause+" And "+stormGravityMainActWhere_clause)
			stormGravityMainUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+stormGravityMainActWhere_clause, invert_where_clause="")
			for exFacID in stormGravityMainExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+stormListedLayer)
				stormGravityMainExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")
		if stormListedLayer in stormInletQueryLayerList:
			# Creates a single Inlet UC query variable (including stormLookbackdays-configured parameters) based upon the value in the Excel file
			stormInletUCQuery_df = pd.read_excel(stormconfigurationfile, sheet_name='Queries', usecols=str('E'))
			stormInletUCQueryarray = stormInletUCQuery_df['Inlets UC'].tolist()
			stormInletUCQueryVar = stormInletUCQueryarray[0]
			stormInletUCQueryItem = stormInletUCQueryVar.format(stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate)
			#print(stormInletUCQueryItem)
			# Creates a single Inlet Active query variable (including stormLookbackdays-configured parameters) based upon the value in the Excel file
			stormInletActQuery_df = pd.read_excel(stormconfigurationfile, sheet_name='Queries', usecols=str('F'))
			stormInletActQueryarray = stormInletActQuery_df['Inlets Active'].tolist()
			stormInletActQueryVar = stormInletActQueryarray[0]
			stormInletActQueryItem = stormInletActQueryVar.format(stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate)
			#print(stormInletActQueryItem)
			# Creates a list of Inlet FacilityIDs to ignore based upon the values in the Excel file
			stormInlet_df = pd.read_excel(stormexceptionfile, sheet_name='Inlets', usecols=str('A'))
			stormInletExceptionFacIDs = stormInlet_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+stormUsername+"' And LASTUPDATE >= '"+stormEditdate+"') Or (LASTMODBY = '"+stormUsername+"' And LASTMODDATE >= '"+stormEditdate+"'))"
			stormInletUCWhere_clause=stormInletUCQueryItem
			stormInletActWhere_clause=stormInletActQueryItem
			print("Selecting "+stormListedLayer+" where "+userDateWhere_clause+" And "+stormInletUCWhere_clause)
			stormInletUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+stormInletUCWhere_clause, invert_where_clause="")
			print("Selecting "+stormListedLayer+" where "+userDateWhere_clause+" And "+stormInletActWhere_clause)
			stormInletUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+stormInletActWhere_clause, invert_where_clause="")
			for exFacID in stormInletExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+stormListedLayer)
				stormInletExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")
		if stormListedLayer in stormDischargePointsQueryLayerList:
			# Creates a single DischargePoints UC query variable (including stormLookbackdays-configured parameters) based upon the value in the Excel file
			stormDischargePointsUCQuery_df = pd.read_excel(stormconfigurationfile, sheet_name='Queries', usecols=str('G'))
			stormDischargePointsUCQueryarray = stormDischargePointsUCQuery_df['DischargePoints UC'].tolist()
			stormDischargePointsUCQueryVar = stormDischargePointsUCQueryarray[0]
			stormDischargePointsUCQueryItem = stormDischargePointsUCQueryVar.format(stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate)
			#print(stormDischargePointsUCQueryItem)
			# Creates a single DischargePoints Active query variable (including stormLookbackdays-configured parameters) based upon the value in the Excel file
			stormDischargePointsActQuery_df = pd.read_excel(stormconfigurationfile, sheet_name='Queries', usecols=str('H'))
			stormDischargePointsActQueryarray = stormDischargePointsActQuery_df['DischargePoints Active'].tolist()
			stormDischargePointsActQueryVar = stormDischargePointsActQueryarray[0]
			stormDischargePointsActQueryItem = stormDischargePointsActQueryVar.format(stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate, stormEditdate)
			#print(stormDischargePointsActQueryItem)
			# Creates a list of Discharge Point FacilityIDs to ignore based upon the values in the Excel file
			stormDischargePoints_df = pd.read_excel(stormexceptionfile, sheet_name='DischargePoints', usecols=str('A'))
			stormDischargePointsExceptionFacIDs = stormDischargePoints_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+stormUsername+"' And LASTUPDATE >= '"+stormEditdate+"') Or (LASTMODBY = '"+stormUsername+"' And LASTMODDATE >= '"+stormEditdate+"'))"
			stormDischargePointsUCWhere_clause=stormDischargePointsUCQueryItem
			stormDischargePointsActWhere_clause=stormDischargePointsActQueryItem
			print("Selecting "+stormListedLayer+" where "+userDateWhere_clause+" And "+stormDischargePointsUCWhere_clause)
			stormDischargePointsUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+stormDischargePointsUCWhere_clause, invert_where_clause="")
			print("Selecting "+stormListedLayer+" where "+userDateWhere_clause+" And "+stormDischargePointsActWhere_clause)
			stormDischargePointsActUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+stormDischargePointsActWhere_clause, invert_where_clause="")
			for exFacID in stormDischargePointsExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+stormListedLayer)
				stormDischargePointsExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")

for waterListedLayer in waterOverallQueryLayerList:
	print("Reviewing "+waterListedLayer)
	# Creates a list of editors from Excel contents
	waterUsername_df = pd.read_excel(waterconfigurationfile, sheet_name='Configuration', usecols=str('A'))
	waterUsernamelist = waterUsername_df['Usernames'].tolist()
	# Creates a single date variable, calculated back from 'today' based upon the value in the Excel file
	waterLookbackdays_df = pd.read_excel(waterconfigurationfile, sheet_name='Configuration', usecols=str('B'))
	waterLookbackdayarray = waterLookbackdays_df['Lookback Number Of Days'].tolist()
	waterLookbackdayItem = waterLookbackdayarray[0]
	waterLookbackdays = int(waterLookbackdayItem)
	waterDateedit = today_date - timedelta(waterLookbackdays)
	waterEditdate = (str(waterDateedit))

	dummySelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=waterListedLayer, selection_type="NEW_SELECTION", where_clause=dummyWhere_clause, invert_where_clause="")
		
	for waterUsername in waterUsernamelist:		
		#print(waterUsername)
		if waterListedLayer in waterSysvalveQueryLayerList:
			# Creates a single System Valve UC query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterSysvalveUCQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('A'))
			waterSysvalveUCQueryarray = waterSysvalveUCQuery_df['System Valve UC'].tolist()
			waterSysvalveUCQueryVar = waterSysvalveUCQueryarray[0]
			waterSysvalveUCQueryItem = waterSysvalveUCQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterSysvalveUCQueryItem)
			# Creates a single System Valve Active query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterSysvalveActQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('B'))
			waterSysvalveActQueryarray = waterSysvalveActQuery_df['System Valve Active'].tolist()
			waterSysvalveActQueryVar = waterSysvalveActQueryarray[0]
			waterSysvalveActQueryItem = waterSysvalveActQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterSysvalveActQueryItem)
			# Creates a list of System Valve FacilityIDs to ignore based upon the values in the Excel file
			waterSysvalve_df = pd.read_excel(waterexceptionfile, sheet_name='SystemValve', usecols=str('A'))
			waterSysvalveExceptionFacIDs = waterSysvalve_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+waterUsername+"' And LASTUPDATE >= '"+waterEditdate+"') Or (LASTMODBY = '"+waterUsername+"' And LASTMODDATE >= '"+waterEditdate+"'))"
			waterSysvalveUCWhere_clause=waterSysvalveUCQueryItem
			waterSysvalve_new_ActWhere_clause=waterSysvalveActQueryItem			
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterSysvalveUCWhere_clause)
			waterSysvalveUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterSysvalveUCWhere_clause, invert_where_clause="")
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterSysvalve_new_ActWhere_clause)
			waterSysvalveActUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterSysvalve_new_ActWhere_clause, invert_where_clause="")
			for exFacID in waterSysvalveExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+waterListedLayer)
				waterSysvalveExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")
		if waterListedLayer in waterMainQueryLayerList:
			# Creates a single Water Mains UC query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterMainUCQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('C'))
			waterMainUCQueryarray = waterMainUCQuery_df['Mains UC'].tolist()
			waterMainUCQueryVar = waterMainUCQueryarray[0]
			waterMainUCQueryItem = waterMainUCQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterMainUCQueryItem)
			# Creates a single Water Mains Active query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterMainActQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('D'))
			waterMainActQueryarray = waterMainActQuery_df['Mains Active'].tolist()
			waterMainActQueryVar = waterMainActQueryarray[0]
			waterMainActQueryItem = waterMainActQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterMainActQueryItem)
			# Creates a list of Water Main FacilityIDs to ignore based upon the values in the Excel file
			waterMains_df = pd.read_excel(waterexceptionfile, sheet_name='Main', usecols=str('A'))
			waterMainExceptionFacIDs = waterMains_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+waterUsername+"' And LASTUPDATE >= '"+waterEditdate+"') Or (LASTMODBY = '"+waterUsername+"' And LASTMODDATE >= '"+waterEditdate+"'))"			
			waterMainUCWhere_clause=waterMainUCQueryItem
			waterMainActWhere_clause=waterMainActQueryItem
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterMainUCWhere_clause)
			waterMainUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterMainUCWhere_clause, invert_where_clause="")
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterMainActWhere_clause)
			waterMainUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterMainActWhere_clause, invert_where_clause="")
			for exFacID in waterMainExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+waterListedLayer)
				waterMainExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")
		if waterListedLayer in waterFittingQueryLayerList:
			# Creates a single Fitting UC query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterFittingUCQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('E'))
			waterFittingUCQueryarray = waterFittingUCQuery_df['Fitting UC'].tolist()
			waterFittingUCQueryVar = waterFittingUCQueryarray[0]
			waterFittingUCQueryItem = waterFittingUCQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterFittingUCQueryItem)
			# Creates a single Fitting Active query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterFittingActQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('F'))
			waterFittingActQueryarray = waterFittingActQuery_df['Fitting Active'].tolist()
			waterFittingActQueryVar = waterFittingActQueryarray[0]
			waterFittingActQueryItem = waterFittingActQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterFittingActQueryItem)
			# Creates a list of Fitting FacilityIDs to ignore based upon the values in the Excel file
			waterFitting_df = pd.read_excel(waterexceptionfile, sheet_name='Fitting', usecols=str('A'))
			waterFittingExceptionFacIDs = waterFitting_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+waterUsername+"' And LASTUPDATE >= '"+waterEditdate+"') Or (LASTMODBY = '"+waterUsername+"' And LASTMODDATE >= '"+waterEditdate+"'))"
			waterFittingUCWhere_clause=waterFittingUCQueryItem
			waterFittingActWhere_clause=waterFittingActQueryItem
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterFittingUCWhere_clause)
			waterFittingUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterFittingUCWhere_clause, invert_where_clause="")
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterFittingActWhere_clause)
			waterFittingUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterFittingActWhere_clause, invert_where_clause="")
			for exFacID in waterFittingExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+waterListedLayer)
				waterFittingExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")
		if waterListedLayer in waterHydrantQueryLayerList:
			# Creates a single Hydrant UC query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterHydrantUCQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('G'))
			waterHydrantUCQueryarray = waterHydrantUCQuery_df['Hydrant UC'].tolist()
			waterHydrantUCQueryVar = waterHydrantUCQueryarray[0]
			waterHydrantUCQueryItem = waterHydrantUCQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterHydrantUCQueryItem)
			# Creates a single Hydrant Active query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterHydrantActQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('H'))
			waterHydrantActQueryarray = waterHydrantActQuery_df['Hydrant Active'].tolist()
			waterHydrantActQueryVar = waterHydrantActQueryarray[0]
			waterHydrantActQueryItem = waterHydrantActQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterHydrantActQueryItem)
			# Creates a list of Hydrant FacilityIDs to ignore based upon the values in the Excel file
			waterHydrant_df = pd.read_excel(waterexceptionfile, sheet_name='Hydrant', usecols=str('A'))
			waterHydrantExceptionFacIDs = waterHydrant_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+waterUsername+"' And LASTUPDATE >= '"+waterEditdate+"') Or (LASTMODBY = '"+waterUsername+"' And LASTMODDATE >= '"+waterEditdate+"'))"
			waterHydrantUCWhere_clause=waterHydrantUCQueryItem
			waterHydrantActWhere_clause=waterHydrantActQueryItem
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterHydrantUCWhere_clause)
			waterHydrantUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterHydrantUCWhere_clause, invert_where_clause="")
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterHydrantActWhere_clause)
			waterHydrantActUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterHydrantActWhere_clause, invert_where_clause="")
			for exFacID in waterHydrantExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+waterListedLayer)
				waterHydrantExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")
		if waterListedLayer in largemeterQueryLayerList:
			# Creates a single Large Meter UC query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterLargeMeterUCQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('I'))
			waterLargeMeterUCQueryarray = waterLargeMeterUCQuery_df['Large Meter UC'].tolist()
			waterLargeMeterUCQueryVar = waterLargeMeterUCQueryarray[0]
			waterLargeMeterUCQueryItem = waterLargeMeterUCQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterLargeMeterUCQueryItem)
			# Creates a single Large Meter Active query variable (including waterLookbackdays-configured parameters) based upon the value in the Excel file
			waterLargeMeterActQuery_df = pd.read_excel(waterconfigurationfile, sheet_name='Queries', usecols=str('J'))
			waterLargeMeterActQueryarray = waterLargeMeterActQuery_df['Large Meter Active'].tolist()
			waterLargeMeterActQueryVar = waterLargeMeterActQueryarray[0]
			waterLargeMeterActQueryItem = waterLargeMeterActQueryVar.format(waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate, waterEditdate)
			#print(waterLargeMeterActQueryItem)
			# Creates a list of Large Meter FacilityIDs to ignore based upon the values in the Excel file
			waterLargeMeter_df = pd.read_excel(waterexceptionfile, sheet_name='LargeMeter', usecols=str('A'))
			largemeterExceptionFacIDs = waterLargeMeter_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+waterUsername+"' And LASTUPDATE >= '"+waterEditdate+"') Or (LASTMODBY = '"+waterUsername+"' And LASTMODDATE >= '"+waterEditdate+"'))"
			waterLargeMeterUCWhere_clause=waterLargeMeterUCQueryItem
			waterLargeMeterActWhere_clause=waterLargeMeterActQueryItem
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterLargeMeterUCWhere_clause)
			largemeterUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterLargeMeterUCWhere_clause, invert_where_clause="")
			print("Selecting "+waterListedLayer+" where "+userDateWhere_clause+" And "+waterLargeMeterActWhere_clause)
			largemeterActUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+waterLargeMeterActWhere_clause, invert_where_clause="")
			for exFacID in largemeterExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+waterListedLayer)
				largemeterExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")

for sewerListedLayer in sewerOverallQueryLayerList:
	print("Reviewing "+sewerListedLayer)
	# Creates a list of editors from Excel contents
	sewerUsername_df = pd.read_excel(sewerconfigurationfile, sheet_name='Configuration', usecols=str('A'))
	sewerUsernamelist = sewerUsername_df['Usernames'].tolist()
	# Creates a single date variable, calculated back from 'today' based upon the value in the Excel file
	sewerLookbackdays_df = pd.read_excel(sewerconfigurationfile, sheet_name='Configuration', usecols=str('B'))
	sewerLookbackdayarray = sewerLookbackdays_df['Lookback Number Of Days'].tolist()
	sewerLookbackdayItem = sewerLookbackdayarray[0]
	sewerLookbackdays = int(sewerLookbackdayItem)
	sewerDateedit = today_date - timedelta(sewerLookbackdays)
	sewerEditdate = (str(sewerDateedit))

	dummySelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=sewerListedLayer, selection_type="NEW_SELECTION", where_clause=dummyWhere_clause, invert_where_clause="")
	
	for sewerUsername in sewerUsernamelist:		
		#print(sewerUsername)
		if sewerListedLayer in sewerManholeQueryLayerList:
			# Creates a single Manhole UC query variable (including sewerLookbackdays-configured parameters) based upon the value in the Excel file
			sewerManholeUCQuery_df = pd.read_excel(sewerconfigurationfile, sheet_name='Queries', usecols=str('A'))
			sewerManholeUCQueryarray = sewerManholeUCQuery_df['Manholes UC'].tolist()
			sewerManholeUCQueryVar = sewerManholeUCQueryarray[0]
			sewerManholeUCQueryItem = sewerManholeUCQueryVar.format(sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate)
			#print(sewerManholeUCQueryItem)
			# Creates a single Manhole Active query variable (including sewerLookbackdays-configured parameters) based upon the value in the Excel file
			sewerManholeActQuery_df = pd.read_excel(sewerconfigurationfile, sheet_name='Queries', usecols=str('B'))
			sewerManholeActQueryarray = sewerManholeActQuery_df['Manholes Active'].tolist()
			sewerManholeActQueryVar = sewerManholeActQueryarray[0]
			sewerManholeActQueryItem = sewerManholeActQueryVar.format(sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate)
			#print(sewerManholeActQueryItem)
			# Creates a list of Manhole FacilityIDs to ignore based upon the values in the Excel file
			sewerManhole_df = pd.read_excel(sewerexceptionfile, sheet_name='Manholes', usecols=str('A'))
			sewerManholeExceptionFacIDs = sewerManhole_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+sewerUsername+"' And LASTUPDATE >= '"+sewerEditdate+"') Or (LASTMODBY = '"+sewerUsername+"' And LASTMODDATE >= '"+sewerEditdate+"'))"
			sewerManholeUCWhere_clause=sewerManholeUCQueryItem
			sewerManhole_new_ActWhere_clause=sewerManholeActQueryItem			
			print("Selecting "+sewerListedLayer+" where "+userDateWhere_clause+" And "+sewerManholeUCWhere_clause)
			sewerManholeUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+sewerManholeUCWhere_clause, invert_where_clause="")
			print("Selecting "+sewerListedLayer+" where "+userDateWhere_clause+" And "+sewerManhole_new_ActWhere_clause)
			sewerManholeActUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+sewerManhole_new_ActWhere_clause, invert_where_clause="")
			for exFacID in sewerManholeExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+sewerListedLayer)
				sewerManholeExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")
		if sewerListedLayer in sewerGravityMainQueryLayerList:
			# Creates a single Gravity Mains UC query variable (including sewerLookbackdays-configured parameters) based upon the value in the Excel file
			sewerGravityMainUCQuery_df = pd.read_excel(sewerconfigurationfile, sheet_name='Queries', usecols=str('C'))
			sewerGravityMainUCQueryarray = sewerGravityMainUCQuery_df['GravityMains UC'].tolist()
			sewerGravityMainUCQueryVar = sewerGravityMainUCQueryarray[0]
			sewerGravityMainUCQueryItem = sewerGravityMainUCQueryVar.format(sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate)
			#print(sewerGravityMainUCQueryItem)
			# Creates a single Gravity Mains Active query variable (including sewerLookbackdays-configured parameters) based upon the value in the Excel file
			sewerGravityMainActQuery_df = pd.read_excel(sewerconfigurationfile, sheet_name='Queries', usecols=str('D'))
			sewerGravityMainActQueryarray = sewerGravityMainActQuery_df['GravityMains Active'].tolist()
			sewerGravityMainActQueryVar = sewerGravityMainActQueryarray[0]
			sewerGravityMainActQueryItem = sewerGravityMainActQueryVar.format(sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate, sewerEditdate)
			#print(sewerGravityMainActQueryItem)
			# Creates a list of Gravity Main FacilityIDs to ignore based upon the values in the Excel file
			sewerGravityMains_df = pd.read_excel(sewerexceptionfile, sheet_name='GravityMains', usecols=str('A'))
			sewerGravityMainExceptionFacIDs = sewerGravityMains_df['FacilityID'].tolist()

			userDateWhere_clause="((LASTEDITOR = '"+sewerUsername+"' And LASTUPDATE >= '"+sewerEditdate+"') Or (LASTMODBY = '"+sewerUsername+"' And LASTMODDATE >= '"+sewerEditdate+"'))"			
			sewerGravityMainUCWhere_clause=sewerGravityMainUCQueryItem
			sewerGravityMainActWhere_clause=sewerGravityMainActQueryItem
			print("Selecting "+sewerListedLayer+" where "+userDateWhere_clause+" And "+sewerGravityMainUCWhere_clause)
			sewerGravityMainUCUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+sewerGravityMainUCWhere_clause, invert_where_clause="")
			print("Selecting "+sewerListedLayer+" where "+userDateWhere_clause+" And "+sewerGravityMainActWhere_clause)
			sewerGravityMainUserDateSelect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="ADD_TO_SELECTION", where_clause=userDateWhere_clause+" And "+sewerGravityMainActWhere_clause, invert_where_clause="")
			for exFacID in sewerGravityMainExceptionFacIDs:
				print("Removing "+exFacID+" from selected "+sewerListedLayer)
				sewerGravityMainExDeselect = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dummySelect, selection_type="REMOVE_FROM_SELECTION", where_clause="FACILITYID = '"+exFacID+"'", invert_where_clause="")

print(" ")
print("Done selecting assets")