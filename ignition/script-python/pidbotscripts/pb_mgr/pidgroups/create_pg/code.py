import pidbotscripts.utils.tag_tools as tag_tools

def createPidGroup(pidGroupDisplayName,pidGroupFolderPath,pidGroupUdtPath):
	tag_tools.createFolderAndParentFolders(pidGroupFolderPath)
	pidGroupTag = {
            "name": getNewPidGroupTagName(pidGroupFolderPath),         
            "typeId" : tag_tools.shortenUdtPath(pidGroupUdtPath),
            "tagType" : "UdtInstance",
    }
	collisionPolicy = "a"
	tag_tools.configureRaiseException(pidGroupFolderPath, [pidGroupTag], collisionPolicy)
	pidGroupPath = pidGroupFolderPath + "/" + pidGroupTag['name']
	displayNameTagPath = pidGroupPath + "/displayName"
	tag_tools.writeBlockingRaiseException([displayNameTagPath], [pidGroupDisplayName])
	return pidGroupPath
	
	
def getNewPidGroupTagName(pidGroupFolderPath):
	# Creates an unused name for the new PidGroup.
	# Note PidGroup tag names do not need to be called 'PidGroup<n>'. The tag name is automatically generated to reduce user input at creation time.
	existingTags = system.tag.browse(pidGroupFolderPath).getResults()
	existingPaths = [str(tag['fullPath']) for tag in existingTags]
	for i in range(0,1000):
		pidGroupTagName = "PidGroup" + str(i)
		pidGroupPath = pidGroupFolderPath + "/" + pidGroupTagName
		if not pidGroupPath in existingPaths:
			return pidGroupTagName
	raise Exception("Please delete a PID Group before creating a new one.")