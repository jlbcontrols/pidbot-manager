import pidbotscripts.pb_mgr.pidgroups.members.member_pids as member_pids
import pidbotscripts.pb_mgr.pidtags.pid_interface as ptinterface
import pidbotscripts.utils.list_tools as list_tools

logger = system.util.getLogger(__name__)


def addTagsToGroup(newTagPaths,pidGroupPath,dropBeforeTagPath):
	valid,failureMessage = ptinterface.validatePidbotTags(newTagPaths)
	if not valid:
		system.gui.messageBox(failureMessage, "Not a Valid PID Tag.")
		return
	pidTagList = member_pids.getPidTagDict([pidGroupPath])[pidGroupPath]
	finalDropBeforeTagPath = getFinalDropBeforeTagPath(dropBeforeTagPath,newTagPaths,pidTagList)
	newPidTagList = list_tools.listExcludingItems(pidTagList,newTagPaths)
	if finalDropBeforeTagPath == "":
		insertIndex = len(newPidTagList)
	else:
		insertIndex = newPidTagList.index(finalDropBeforeTagPath)
	newPidTagList[insertIndex:insertIndex] = newTagPaths
	newPidTagDict = {pidGroupPath: newPidTagList}
	member_pids.updatePidTagLists(newPidTagDict)
	
	
def getFinalDropBeforeTagPath(dropBeforeTagPath,newTagPaths,currentTagPaths):
	if not dropBeforeTagPath in newTagPaths:
		return dropBeforeTagPath
	index = currentTagPaths.index(dropBeforeTagPath)
	if dropBeforeTagPath in newTagPaths:
		index = currentTagPaths.index(dropBeforeTagPath) + 1
		if index < len(currentTagPaths):
			dropBeforeTagPath = currentTagPaths[index]
			return getFinalDropBeforeTagPath(dropBeforeTagPath,newTagPaths,currentTagPaths)
		else:
			return ""
	else:
		return dropBeforeTagPath		
