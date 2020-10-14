import pidbotscripts.utils.list_tools as list_tools

class AbstractListRequiredChecker():
	def __init__(self,failKey,requiredList,listDescription):
		self.requiredList = requiredList
		self.listDescription = listDescription
		self.failKey = failKey
	
	def check(self,tagConfigNode):
		return not self.missingItemsFrom(tagConfigNode)
					
	def getFailureMessage(self,tagConfigNode):
		missingItems = self.missingItemsFrom(tagConfigNode)
		if missingItems:
			path = str(tagConfigNode.tagConfig['path'])
			header = "Tag is not valid:\n%s\nMissing %s:" % (path,self.listDescription)
			return list_tools.createListMessage(missingItems,header)
		return ""
			
	def missingItemsFrom(self,tagConfigNode):
		actualList = self.itemsFoundForNode(tagConfigNode)
		return list_tools.itemsNotInList(self.requiredList,actualList)
	
	def itemsFoundForNode(self,tagConfigNode):
		raise NotImplementedError


class ChildrenRequiredChecker(AbstractListRequiredChecker):
	def __init__(self,requiredChildNames,failKey="missingChildren"):
		AbstractListRequiredChecker.__init__(self,failKey,requiredChildNames,"required child tags")
	
	def itemsFoundForNode(self,tagConfigNode):
		return [childNode.getName() for childNode in tagConfigNode.childNodes]


class ParamsRequiredChecker(AbstractListRequiredChecker):
	def __init__(self,requiredParamNames,failKey="missingParams"):
		AbstractListRequiredChecker.__init__(self,failKey,requiredParamNames,"required parameters")
	
	def itemsFoundForNode(self,tagConfigNode):
		return tagConfigNode.tagConfig.get('parameters',{}).keys()


class UdtMemberExcluder():
	def __init__(self,failKey="udtMember"):
		self.failKey = failKey
	
	def check(self,tagConfigNode):
		for ancestorNode in tagConfigNode.getAncestorNodes():
			if str(ancestorNode.tagConfig.get('tagType',"")) in ["UdtInstance","UdtType"]:
				return False
		return True

	def getFailureMessage(self,tagConfigNode):
		if not self.check(tagConfigNode):
			path = str(tagConfigNode.tagConfig['path'])
			return "Tag is not valid:\n%s\nCannot be a member of another tag." % path
		return ""
	

class DirectoryChecker():
	def __init__(self,allowedDirectoryPaths,failKey="directoryNotAllowed"):
		self.allowedDirectoryPaths = allowedDirectoryPaths
		self.failKey = failKey
	
	def check(self,tagConfigNode):
		for allowedDirectoryPath in self.allowedDirectoryPaths:
			if tagConfigNode.isDescendentOf(allowedDirectoryPath):
				return True
		return False

	def getFailureMessage(self,tagConfigNode):
		if not self.check(tagConfigNode):
			path = str(tagConfigNode.tagConfig['path'])
			header = "Tag is not valid:\n%s\nMust be located in directory:%s\n" % (path)
			return list_tools.createListMessage(self.allowedDirectoryPaths,header)
		return ""
	
	
class TagTypeChecker():
	def __init__(self,allowedTypes,failKey="typeNotAllowed"):
		self.allowedTypes = allowedTypes
		self.failKey = failKey

	def check(self,tagConfigNode):
		tagType = str(tagConfigNode.tagConfig['tagType'])
		return tagType in self.allowedTypes

	def getFailureMessage(self,tagConfigNode):
		if not self.check(tagConfigNode):
			path = str(tagConfigNode.tagConfig['path'])
			header = "Tag is not valid:\n%s\nType must be:" % path
			return list_tools.createListMessage(self.allowedTypes,header)
		return ""


class NodeExistsChecker():
	def __init__(self,failKey="doesNotExist"):
		self.failKey = failKey

	def check(self,tagConfigNode):
		return tagConfigNode.exists

	def getFailureMessage(self,tagConfigNode):
		if not self.check(tagConfigNode):
			path = str(tagConfigNode.tagConfig['path'])
			return "Tag not found or does not exist:\n%s" % path
		return ""
