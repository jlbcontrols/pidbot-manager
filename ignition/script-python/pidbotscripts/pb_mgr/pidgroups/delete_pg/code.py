import pidbotscripts.utils.list_tools as list_tools

def deletePidGroupsWithPrompts(pidGroupPaths):
	pidGroupNamePaths = [path+"/displayName" for path in pidGroupPaths]
	pidGroupNameQvs = system.tag.readBlocking(pidGroupNamePaths)
	pidGroupNames = [qv.value for qv in pidGroupNameQvs]
	confirmMessage = list_tools.createListMessage(pidGroupNames,"Delete Displays?")
	if system.gui.confirm(confirmMessage,"Confirm Delete"):
		system.tag.deleteTags(pidGroupPaths)
