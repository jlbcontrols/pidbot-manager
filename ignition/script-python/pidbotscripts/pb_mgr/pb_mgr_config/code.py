# These methods may be updated for project specific requirements.

import pidbotscripts.utils.data_mapping as data_mapping


### Tag Provider Settings ###
def getPrimaryTagProvider():
	return str(system.tag.read("[System]Client/System/DefaultTagProvider").value)

def getPidGroupTagProvider():
	return getPrimaryTagProvider()

# Add more providers here to allow user to create/delete tags in additional providers.
def getManageableTagProviders(asDataset=False):
	providerList = [
		getPrimaryTagProvider(),
		"testProv"
	]
	deduplicatedList = list(set(providerList))
	if asDataset:
		return data_mapping.listToColumnDs(deduplicatedList)
	return deduplicatedList


### PID Group Settings (aka Displays) ###
def getPidGroupFolderPath(tagProvider=getPrimaryTagProvider()):
	return "["+tagProvider+"]PidbotInst/PidGroups"
	
def getPidGroupUdtPath(tagProvider=getPrimaryTagProvider()):
	return "["+tagProvider+"]_types_/PidbotTypes/PidGroup"


### OPC Tag Generator Settings ###
def getPidTagRootPath(tagProvider):
	return "["+tagProvider+"]PidbotInst/PidTags"

def getPidTagUdtPaths(tagProvider,asDataset=False):
	paths = [
		"_types_/PidbotTypes/Pid/Studio5000/PIDE",
		"_types_/PidbotTypes/Pid/Studio5000/P_PIDE",
		"_types_/PidbotTypes/Pid/Studio5000/PID"
	]
	fullPaths = ["["+tagProvider+"]"+path for path in paths]
	if asDataset:
		return data_mapping.listToColumnDs(fullPaths)
	return fullPaths