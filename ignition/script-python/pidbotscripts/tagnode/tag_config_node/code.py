from com.inductiveautomation.ignition.common.tags.model import TagPath
from com.inductiveautomation.ignition.common.tags.paths.parser import TagPathParser
import pidbotscripts.utils.tag_tools as tag_tools

class TagConfigNode:
	def __init__(self,tagConfig,parentNode=None,exists=True):
		self.tagConfig = tagConfig
		self.parentNode = parentNode
		self.exists = exists
		self.childNodes = self.createChildNodes()
	
	def createChildNodes(self):
		childNodes = []
		for tagConfig in self.tagConfig.get('tags',[]):
			childNodes.append(TagConfigNode(tagConfig,self))
		return childNodes
	
	def getAncestorNodes(self,nodes=[]):
		if self.parentNode:
			nodes.append(self.parentNode)
			self.parentNode.getAncestorNodes(nodes)
		return nodes
		
	def getRootNode(self):
		ancestorNodes = self.getAncestorNodes()
		if ancestorNodes:
			return ancestorNodes.pop()
	
	def getChildNode(self,childName):
		for childNode in self.childNodes:
			if childNode.getName()==childName:
				return childNode
		return createImaginaryNode(childName,parentNode=self)
	
	def getName(self):
		return str(self.tagConfig.get('name',""))
	
	def getFullPath(self):
		tagPath = self.tagConfig['path']
		if self.parentNode:
			return self.parentNode.getFullPath().getChildPath(tagPath.toStringFull())
		return tagPath
	
	def getNodeForPath(self,path):
		tagPath = tag_tools.coerceToTagPathObject(path)
		if self.pathEquals(tagPath):
			return self
		if self.isAncestorOf(tagPath):
			childName = tagPath.getPathComponent(self.getFullPath().getPathLength())
			childNode = self.getChildNode(childName)
			return childNode.getNodeForPath(tagPath)
		if self.parentNode:
			return self.parentNode.getNodeForPath(tagPath)
		return createImaginaryNode(path)

	def pathEquals(self,path):
		tagPath = tag_tools.coerceToTagPathObject(path)
		return self.getFullPath().toStringFull().lower() == tagPath.toStringFull().lower()
	
	# Check if a path would be a descendent of this node. A node for this path does not need to exist.
	def isAncestorOf(self,path):
		tagPath = tag_tools.coerceToTagPathObject(path)
		return self.getFullPath().isAncestorOf(tagPath)
	
	# Check if a path would be an ancestor of this node. A node for this path does not need to exist.
	def	isDescendentOf(self,path):
		tagPath = tag_tools.coerceToTagPathObject(path)
		return tagPath.isAncestorOf(self.getFullPath())
	

def createImaginaryNode(path,parentNode=None):
	tagPath = tag_tools.coerceToTagPathObject(path)
	tagConfig = {
		'name':tagPath.getItemName(),
		'path':tagPath
		}
	return TagConfigNode(tagConfig,parentNode,exists=False)


def createRootNodeForPath(path):
	rootConfig = system.tag.getConfiguration(path,True)[0]
	return TagConfigNode(rootConfig,None)

