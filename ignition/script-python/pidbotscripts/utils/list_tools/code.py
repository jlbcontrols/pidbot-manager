logger = system.util.getLogger('pidbotscripts_util')

# Return a list of required items not found in another list
def itemsNotInList(requiredItems,items):
	itemsNotFound = []
	for requiredItem in requiredItems:
		if not requiredItem in items:
			itemsNotFound.append(requiredItem)
	return itemsNotFound


def listExcludingItems(fullList,itemsToExclude):
	return [item for item in fullList if item not in itemsToExclude]		
	

# Generate a titled message (i.e. for use in message box) for a list of objects. Returns "" if list is empty.
def createListMessage(items,title):
	if items:
		message = str(title) + "\n"
		for item in items:
			message += "-     " + str(item) + "\n"
		return message
	return ""

	

