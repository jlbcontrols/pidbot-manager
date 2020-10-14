import pidbotscripts.pb_mgr.pidgroups.members.member_pids as member_pids
import pidbotscripts.utils.list_tools as list_tools
logger = system.util.getLogger(__name__)


def removePidTagsFromGroups(pathsToRemove,pidGroupPaths,removeChildren=False):
	pidTagDict = member_pids.getPidTagDict(pidGroupPaths)
	for pidGroupPath in pidTagDict.keys():
		if removeChildren:
			pidTagDict[pidGroupPath] = removeTagsAndChildrenFromList(pathsToRemove, pidTagDict[pidGroupPath])
		else:
			pidTagDict[pidGroupPath] = list_tools.listExcludingItems(pidTagDict[pidGroupPath],pathsToRemove)
	member_pids.updatePidTagLists(pidTagDict)
	return

	
def removeTagsAndChildrenFromList(pathsToRemove,pathList):
	filteredList = []
	for path in pathList:
		remove = False
		for pathToRemove in pathsToRemove:
			if path.startswith(pathToRemove):
				remove = True
				break
		if not remove:
			filteredList.append(path)
	return filteredList
