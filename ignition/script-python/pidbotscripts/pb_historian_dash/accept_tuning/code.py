import pidbotscripts.utils.list_tools as list_tools
import pidbotscripts.utils.tag_tools as tag_tools

def confirmTuning(logEntryDict,instancePath,namedQueryFolderPath):
	warningMessage = "CAUTION!\n\nChanging PID tuning values may result in poor or unstable control. Injury, equipment damage, poor product quality, and other negative outcomes may occur. The simulation displayed may not accurately predict PID performance. PID tuning values should only be changed by a responsible professional, who can mitigate risks associated with changes to PID tuning.\n\nAre you sure you want to update the PID tuning values?"
	if system.gui.confirm(warningMessage,"Update Tuning and Create Log Entry"):
		try:
			writeTuningTags(logEntryDict,instancePath)
		except tag_tools.TagWriteQualityException as e:
			title = "Error Writing PID Tags"
			message = "Error updating PID tuning values.\nCheck PID controller to ensure it is in a safe state.\n\n"
			message += e.getTagQualMessage()
			system.gui.messageBox(message,title)
			return False
		try:
			writeProcessModelTags(logEntryDict,instancePath)
		except tag_tools.TagWriteQualityException as e:
			title = "Error Writing Process Model Tags"
			message = "Error updating Process Model values.\nPID values were updated, but a tuning log entry was not made.\n\n"
			message += e.getTagQualMessage()
			system.gui.messageBox(message,title)
			return False
		try:
			createLogEntry(logEntryDict,namedQueryFolderPath)
		except:
			title = "Database Write Error"
			message = "Error creating tuning log entry.\nPID values and process model values were updated, but a tuning log entry was not made."
			system.gui.messageBox(message,title)
			return False
		title = "Success"
		message = "Tuning updated, and logged.\nTest and monitor the PID controller to confirm it performs as required."
		system.gui.messageBox(message,title)
		return True


def writeTuningTags(logEntryDict,instancePath):
	tuneDict = {
		"currentP": logEntryDict["tunedP"],
		"currentI": logEntryDict["tunedI"],
		"currentD": logEntryDict["tunedD"]
	}
	writeChildTags(tuneDict,instancePath,tuneDict.keys(),timeout=5000)
	

def writeProcessModelTags(logEntryDict,instancePath):
	childNames = ["processGain","processDeadTime","processTimeConst","processType"]
	writeChildTags(logEntryDict,instancePath,childNames)


def createLogEntry(logEntryDict,namedQueryFolderPath):
	# Create Database Tables if they don't exist
	system.db.runNamedQuery(namedQueryFolderPath+"/createLogTable",{"database":logEntryDict["database"]})
	system.db.runNamedQuery(namedQueryFolderPath+"/createChartImageTable",{"database":logEntryDict["database"]})
	
	# Add entry to log and chart image table
	pidbot_log_ndx = system.db.runNamedQuery(namedQueryFolderPath + "/insertLogEntry", logEntryDict, getKey=True)
	logEntryDict['pidbot_log_ndx']=pidbot_log_ndx
	system.db.runNamedQuery(namedQueryFolderPath + "/insertChartImages", logEntryDict)
	return pidbot_log_ndx


def writeChildTags(valueDict,parentPath,childNames,timeout=45000):
	tagPaths = []
	values = []
	for childName in childNames:
		tagPaths.append(parentPath + "/" + childName)
		values.append(valueDict[childName])
	tag_tools.writeBlockingRaiseException(tagPaths,values,timeout)


