logger = system.util.getLogger(__name__)


def getMembershipDict(pidTagPaths,pidGroupPaths):
	pidTagDict = getPidTagDict(pidGroupPaths)
	membershipDict = {}
	for pidTagPath in pidTagPaths:
		membershipDict[pidTagPath]=[]
		for pidGroupPath,groupMembers in pidTagDict.items():
			if pidTagPath in groupMembers:
				membershipDict[pidTagPath].append(pidGroupPath)
	return membershipDict


def getPidTagDict(pidGroupPaths):
	if isinstance(pidGroupPaths,str):
		pidGroupPaths = [pidGroupPaths]
	if pidGroupPaths:
		pidTagListPaths = [pidGroupPath + "/pidTagList" for pidGroupPath in pidGroupPaths]
		logger.debug("reading pidTagLists...\n" + str(pidTagListPaths))
		pidTagListQvs = system.tag.readBlocking(pidTagListPaths)
		pidTagLists = [qv.value for qv in pidTagListQvs]
		pidTagDict = {}
		for pidGroupPath,pidTagList in zip(pidGroupPaths,pidTagLists):
			pidTagDict[pidGroupPath]=pidTagList
		return pidTagDict
	return {}


def updatePidTagLists(pidTagDict):
	if logger.isDebugEnabled():
		import pprint
		logger.debug(
			"updating pid group tag lists...\n"+
			pprint.pformat(pidTagDict)
			)
	pidTagListPaths = []
	pidTagLists = []
	for pidGroupPath,pidTagList in pidTagDict.items():
		pidTagListPaths.append(pidGroupPath+"/pidTagList")
		pidTagLists.append(pidTagList)
	system.tag.writeBlocking(pidTagListPaths,pidTagLists)
	return





### Testing ###
def getPidTagDictTest(pidGroupPaths=["[default]PidbotInst/PidGroups/PidGroup0","[default]PidbotInst/PidGroups/PidGroup1"]):
	pidTagDict = getPidTagDict(pidGroupPaths)
	for pidGroupPath in pidGroupPaths:
		assert pidTagDict[pidGroupPath]==system.tag.read(pidGroupPath+"/pidTagList").value