import arcpy
import pythonaddins
import arceditor
import pandas as pd
import numpy as np
import time
import re, os, errno
import subprocess
import shutil
from shutil import copyfile
arcpy.SetLogHistory(False)
arcpy.env.overwriteOutput = True

class ButtonClass37(object):
    """Implementation for DupFacIDs_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
		sub_foldNam = r"Storm"


		# Database Connection details
		# The name you choose to give the SDE connection goes here
		databaseConnectionName = "SAS_StormWater_QA"

		# The unchanging information about the database connection goes here
		targetDatabase = "SAS_Stormwater"
		targetInstance = "t1itpgisdbs02"
		targetUsername = "eng_storm"
		targetPassword = "Q!az12345"
		targetVersion = "ENG_STORM.ENG_Storm_QA"
		Database_Connection_Folder_Path = "Database Connections"
		Database_Connections = Database_Connection_Folder_Path

		# The attribute for which you are seaching for duplicates
		statsFields = [["FACILITYID", "COUNT"]]





		# PREPARE AND VALIDATE WORKING FOLDERS
		

		# Local Variables
		# Do not change root 'C:' location without having write permissions to that location
		rootlocation = r"C:"
		arcpy.env.workspace = r"C:"
		# Path is verified or constructed by variables below
		main_folder_path = r"\QAQC"
		main_foldNam1 = r"\Duplicates"
		sub_foldNam1 = "\\" + sub_foldNam 
		sub_foldNam2 = r"\Duplicates"
		sourceTablePath = r"\\main\eng\englibrary\Maps\Data\Geodatabases" + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2
		sourceTable = r"issues_all_dupfacidsort.csv"
		sourceTableName = "\\" + sourceTable

		# Execute main_folder_path CreateFolder
		if arcpy.Exists(main_folder_path):
			print main_folder_path, " folder exists.", "\n"
		else:
			arcpy.CreateFolder_management(rootlocation, main_folder_path)
			print "Making " + main_folder_path + " folder..."

		#    if os.path.isdir(os.path.join(main_folder_path, main_foldNam1)) == True:
		if arcpy.Exists(main_folder_path + main_foldNam1):
			print main_folder_path + main_foldNam1, " folder exists.", "\n"
		else:  
			arcpy.CreateFolder_management(main_folder_path, main_foldNam1)
			print "Making " + main_foldNam1 + " folder in " +  main_folder_path

		# Execute sub_foldNam1 CreateFolder
		if arcpy.Exists(main_folder_path + main_foldNam1 + sub_foldNam1):
			print main_folder_path + main_foldNam1 + sub_foldNam1, " folder exists.", "\n"
		else:  
			arcpy.CreateFolder_management(main_folder_path + main_foldNam1, sub_foldNam1)
			print "Making " + sub_foldNam1 + " folder in " +  main_folder_path + main_foldNam1

		try:
			shutil.rmtree(rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2)
			print "Deleted " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2
		except:
			print "Could not delete " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2

		# Execute sub_foldNam2 delete and CreateFolder
		if arcpy.Exists(main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2):
			print main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2, " folder exists.", "\n"
		else:  
			arcpy.CreateFolder_management(main_folder_path + main_foldNam1 + sub_foldNam1, sub_foldNam2)
			print "Making " + sub_foldNam2 + " folder in " +  main_folder_path + main_foldNam1 + sub_foldNam1

		try:
			copyfile(sourceTablePath + sourceTableName, rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + sourceTableName)
			print "Copied the " + sourceTableName + " file from " + sourceTablePath + " to " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2
		except:
			print "Could not copy the " + sourceTableName + " file from " + sourceTablePath + " to " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2



		# CONFIRM OR ESTABLISH CONNECTIONS


		# The root path to which you want the data sent goes here
		SavePath = "C:\\QAQC\\Duplicates\\" + sub_foldNam1
		duplicate = "C:\\QAQC\\Duplicates\\" + sub_foldNam1 + "\\Duplicates"
		# The information about the temporary file geodatabase goes here
		tempFileGDBName = "AllDefault"
		# additional folder-path \\ elements added to aid in path creation
		OutputPath = SavePath + "\\"
		resubPath = targetDatabase + ".SDE."

		# Test for databaseConnectionName and Create Connection if necessary	
		if arcpy.Exists('Database Connections\\' + databaseConnectionName + '.sde'):
			print "Connection to " + databaseConnectionName + ".sde already exists"
		else:
				
			# Process: Create Database Connection
			arcpy.CreateDatabaseConnection_management(Database_Connection_Folder_Path, databaseConnectionName, "SQL_SERVER", targetInstance, "DATABASE_AUTH", targetUsername, targetPassword, "SAVE_USERNAME", targetDatabase, "", "TRANSACTIONAL", targetVersion, "")
			print "Created connection to " + databaseConnectionName + ".sde"

			
		# Test for file geodatabase and Create file geodatabase if necessary	
		# Local variables:
		AllDefault_gdb = SavePath

		if arcpy.Exists(OutputPath + tempFileGDBName + '.gdb'):
			print "Connection to " + OutputPath + tempFileGDBName + ".gdb already exists"
		else:
			# Process: Create Database Connection
			# Process: Create File GDB
			arcpy.CreateFileGDB_management(SavePath, tempFileGDBName, "CURRENT")
			print "Created connection to " + OutputPath + tempFileGDBName + ".gdb"

			
		# START TO WORK	
				
		# Convert feature classes within feature datasets to shapefiles
		arcpy.env.workspace = "Database Connections\\" + databaseConnectionName + ".sde"

		# Print all the feature datasets 
		datasets = arcpy.ListDatasets("", "")

		for dataset in datasets:
			print(dataset)	
			 
		# Rename and export all the feature classes within each dataset
		for dataset in datasets:
			arcpy.env.workspace = "Database Connections\\" + databaseConnectionName + ".sde\\" + dataset
				
			# get a list of feature classes in arcpy.env.workspace
			listFC = arcpy.ListFeatureClasses()
			# reformats the array/list of feature classes and datasets
			print listFC
			for fc in listFC:
				fZc = fc
				func = re.sub(resubPath, '', fZc)
				fundc = re.sub('[.]', '', func)
				fbrlc = re.sub('\[', '', fundc)
				fbrrc = re.sub('\]', '', fbrlc)
				f_c = fbrrc

				print "Trying " + fc + " as " + f_c
				# Variables
				try:
					# Local variables:
					stats_swcasing_dupfacids__2_ = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\stats_" + f_c + "_dupfacids"
					Delete_succeeded = "true"
					issues_swcasing_dupfacids_csv__2_ = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\issues_" + f_c + "_dupfacids.csv"
					Delete_succeeded__2_ = "true"
					issues_swcasing_dupfacidsort__2_ = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\issues_" + f_c + "_dupfacidsort"
					Delete_succeeded__3_ = "true"
					SAS_Stormwater_SDE_swCasing = "Database Connections\\" + databaseConnectionName + ".sde\\" + dataset + "\\" + fc
					Stats_swCasing_DupFacIDs = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\stats_" + f_c + "_dupfacids"
					stats_swcasing_dupfacids__3_ = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\stats_" + f_c + "_dupfacids"
					issues_swcasing_dupfacids_csv = stats_swcasing_dupfacids__3_
					Duplicates = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2
					issues_swcasing_dupfacidsort = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\issues_" + f_c + "_dupfacidsort"
					swcasing_sorteddupfacid_csv = issues_swcasing_dupfacidsort
					Duplicates__2_ = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2

					# Process: Delete
					arcpy.Delete_management(stats_swcasing_dupfacids__2_, "")

					# Process: Delete (2)
					arcpy.Delete_management(issues_swcasing_dupfacids_csv__2_, "")

					# Process: Delete (3)
					arcpy.Delete_management(issues_swcasing_dupfacidsort__2_, "")
					try:
						# Process: Summary Statistics
						arcpy.Statistics_analysis(SAS_Stormwater_SDE_swCasing, Stats_swCasing_DupFacIDs, statsFields, "FACILITYID")
						# Process: Table to Table
						arcpy.TableToTable_conversion(stats_swcasing_dupfacids__3_, Duplicates, "issues_" + f_c + "_dupfacids.csv", "\"FREQUENCY\" > 1", "FACILITYID \"FACILITYID\" true true false 30 Text 0 0 ,First,#," + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\stats_" + f_c + "_dupfacids,FACILITYID,-1,-1;FREQUENCY \"FREQUENCY\" true true false 4 Long 0 0 ,First,#," + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\stats_" + f_c + "_dupfacids,FREQUENCY,-1,-1;COUNT_FACI \"COUNT_FACI\" true true false 4 Long 0 0 ,First,#," + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\stats_" + f_c + "_dupfacids,COUNT_FACILITYID,-1,-1", "")

						# Process: Sort
						arcpy.Sort_management(issues_swcasing_dupfacids_csv, issues_swcasing_dupfacidsort, "FREQUENCY DESCENDING", "UR")
						
						# Process: Table to Table (2)
						arcpy.TableToTable_conversion(issues_swcasing_dupfacidsort, Duplicates__2_, "" + f_c + "_sorteddupfacid.csv", "", "OBJECTID \"OBJECTID\" true true false 4 Long 0 0 ,First,#," + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\issues_" + f_c + "_dupfacidsort,OBJECTID,-1,-1;OID_ \"OID\" true true false 4 Long 0 0 ,First,#," + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\issues_" + f_c + "_dupfacidsort,OID_,-1,-1;FACILITYID \"FACILITYID\" true true false 30 Text 0 0 ,First,#," + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\issues_" + f_c + "_dupfacidsort,FACILITYID,-1,-1;FREQUENCY \"FREQUENCY\" true true false 4 Long 0 0 ,First,#," + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\issues_" + f_c + "_dupfacidsort,FREQUENCY,-1,-1;COUNT_FACI \"COUNT_FACI\" true true false 4 Long 0 0 ,First,#," + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + "\\issues_" + f_c + "_dupfacidsort,COUNT_FACI,-1,-1", "")
						
						print "Created a issues_" + f_c + "_dupfacidsort table in " + OutputPath + "Duplicates..."
					except:
						print "Couldn't create issues_" + f_c + "_dupfacidsort table in " + OutputPath + "Duplicates..."
								
				except OSError as e:
					if e.errno != errno.EEXIST:
						raise
					print "Couldn't create a table from the " + fc + " feature class into the " + OutputPath + "Duplicates folder.  " + fc + " may not have contained a FACILITYID field."
					
					del stats_swcasing_dupfacids__2_
					del Delete_succeeded
					del issues_swcasing_dupfacids_csv__2_
					del Delete_succeeded__2_
					del issues_swcasing_dupfacidsort__2_
					del Delete_succeeded__3_
					del SAS_Stormwater_SDE_swCasing
					del Stats_swCasing_DupFacIDs
					del stats_swcasing_dupfacids__3_
					del issues_swcasing_dupfacids_csv
					del Duplicates
					del issues_swcasing_dupfacidsort
					del Duplicates__2_
					
					
					
				print "Next..."
			print "Done."
			
		arcpy.env.workspace = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2
		pathToCSV = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2

		dupCSVoutput = arcpy.ListFiles("*_dupfacids.csv")
		print dupCSVoutput
		for dupCSVs in dupCSVoutput:
			dupTruncEnd = dupCSVs[:-14]
			dupTrunc = dupTruncEnd[7:]
			dupPath = pathToCSV + "\\" + dupCSVs
			print dupPath
			print dupTrunc
			# Local variables:
			fetclas = "FEATURE_CLASS"
			print "Trying " + dupCSVs
			try:
				df = pd.read_csv(dupPath)
				print "Read " + dupCSVs
				try:
					df.insert(4,fetclas,dupTrunc)
					print "Inserted " + fetclas + " column and populated with " + dupTrunc
					try:
						df.to_csv(pathToCSV + "\\a_" + dupTrunc + "_apnd.csv")
						print "Wrote data to " + pathToCSV + "\\" + dupTrunc + "_apnd.csv"
					except:
						print "Couldn't save output"
				except:
					print "Could't insert column"
			except:
				print "Couldn't read in file"
			print "Next........"
			
		arcpy.env.workspace = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2
		pathToCSV = rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2
		appendTargetCSV = "issues_all_dupfacidsort.csv"
		csvFilePath = pathToCSV + "\\" + appendTargetCSV

		appndCSVoutput = arcpy.ListFiles("*_apnd.csv")
		print appndCSVoutput
		for appndCSVs in appndCSVoutput:
			appndPath = pathToCSV + "\\" + appndCSVs
			print appndPath
			print appndCSVs
			# Local variables:
			
			print "Trying to append " + appndCSVs + " to issues_all_dupfacidsort.csv"
			def appendDFToCSV_void(df, csvFilePath, sep=","):
				if not os.path.isfile(csvFilePath):
					df.to_csv(csvFilePath, mode='a', index=False, sep=sep)
				elif len(df.columns) != len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns):
					raise Exception("Columns do not match!! Dataframe has " + str(len(df.columns)) + " columns. CSV file has " + str(len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns)) + " columns.")
				elif not (df.columns == pd.read_csv(csvFilePath, nrows=1, sep=sep).columns).all():
					raise Exception("Columns and column order of dataframe and csv file do not match!!")
				else:
					df.to_csv(csvFilePath, mode='a', index=False, sep=sep, header=False)
			try:
				df = pd.read_csv(appndPath)
				print "Read " + appndCSVs
				try:
					appendDFToCSV_void(df, csvFilePath, sep=",")
					print "Appended " + appndCSVs + " to " + appendTargetCSV
				except:
					print "Could't append " + appndCSVs + " to " + appendTargetCSV
			except:
				print "Couldn't read in file"

		timestr = time.strftime("-%Y%m%d-%H%M%S")

		try:
			copyfile(rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + sourceTableName, rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + "\\" + sub_foldNam + timestr + "-" + sourceTable)
			print "Copied the " + sourceTable + " file as " + sub_foldNam + timestr + "-" + sourceTable + " from " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + " to " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 
		except:
			print "Could not copy the " + sourceTable + " file from " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2 + " to " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1

		try:
			shutil.rmtree(rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2)
			print "Deleted " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2
		except:
			print "Could not delete " + rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2

		if arcpy.Exists(main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2):
			print main_folder_path + main_foldNam1 + sub_foldNam1 + sub_foldNam2, " folder exists.", "\n"
		else:  
			arcpy.CreateFolder_management(main_folder_path + main_foldNam1 + sub_foldNam1, sub_foldNam2)
			print "Making " + sub_foldNam2 + " folder in " +  main_folder_path + main_foldNam1 + sub_foldNam1
			
		os.startfile(rootlocation + main_folder_path + main_foldNam1 + sub_foldNam1 + "\\" + sub_foldNam + timestr + "-" + sourceTable)
		
		print "Done."		