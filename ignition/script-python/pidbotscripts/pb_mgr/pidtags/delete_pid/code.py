import pidbotscripts.tagnode.tag_config_node as tag_config_node
import pidbotscripts.tagnode.node_checker as node_checker
import pidbotscripts.utils.list_tools as list_tools
import pidbotscripts.pb_mgr.pidgroups.members.remove_pid as remove_pid

# Checks if PID tags are allowed to be deleted, removes from all groups, then deletes.
def safeDelete(pidTagPaths,pidTagRootFolderPath,pidGroupPaths):
	tagDeleteDict = separateByDeletability(pidTagPaths,pidTagRootFolderPath)
	if confirmDelete(tagDeleteDict):
		remove_pid.removePidTagsFromGroups(tagDeleteDict["deletable"],pidGroupPaths,removeChildren=True)
		return system.tag.deleteTags(tagDeleteDict["deletable"])

def separateByDeletability(pidTagPaths,pidTagRootFolderPath):
	rootTagConfigNode = tag_config_node.createRootNodeForPath(pidTagRootFolderPath)
	
	dirChecker = node_checker.DirectoryChecker([pidTagRootFolderPath],failKey="notInDeleteablePath")
	existsChecker = node_checker.NodeExistsChecker("doesNotExist")
	udtMemberExcluder = node_checker.UdtMemberExcluder("udtMember")
	
	tagDeleteDict = {
		"deletable":[],
		"notDeletable":{
			dirChecker.failKey:[],
			existsChecker.failKey:[],
			udtMemberExcluder.failKey:[]
			}
		}
	
	for path in pidTagPaths:
		tagConfigNode = rootTagConfigNode.getNodeForPath(path)
		passedChecks = True
		for checker in [dirChecker,existsChecker,udtMemberExcluder]:
			if not checker.check(tagConfigNode):
				tagDeleteDict["notDeletable"][checker.failKey].append(path)
				passedChecks = False
				break
		if passedChecks:
			tagDeleteDict["deletable"].append(path)
	return tagDeleteDict

	
def confirmDelete(tagDeleteDict):
	notDeleteableMessage = list_tools.createListMessage(tagDeleteDict["notDeletable"]["notInDeleteablePath"],"Some tags cannot be deleted because they are not in a directory with deleting permission:")
	notDeleteableMessage += list_tools.createListMessage(tagDeleteDict["notDeletable"]["udtMember"],"Some tags cannot be deleted because they are members of another tag instance:")
	notDeleteableMessage += list_tools.createListMessage(tagDeleteDict["notDeletable"]["doesNotExist"],"Some tags cannot be deleted because they do not exist or cannot be found:")
	if notDeleteableMessage:
		system.gui.messageBox(notDeleteableMessage, "Not Deletable!")
	
	confirmMessage = list_tools.createListMessage(tagDeleteDict["deletable"],"Delete tags?  Note: If a folder is selected, all tags in the folder will be deleted.")
	if confirmMessage:
		if system.gui.confirm(confirmMessage, "Confirm Tag Deletion"):
			return True
	return False