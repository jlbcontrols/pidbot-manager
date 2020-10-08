logger = system.util.getLogger('udt_instance_generator')
import pidbotscripts.utils.tag_tools as tag_tools

class AbstractUdtInstanceGenerator:
	def __init__(self,opcTypeRecognizer):
		self.opcTypeRecognizer = opcTypeRecognizer

	def createFromOpcBrowseNodes(self,opcBrowseNodes):
		unrecognizedOpcBrowseNodes = []
		for opcBrowseNode in opcBrowseNodes:
			udtPath = self.opcTypeRecognizer.recognizeOpcBrowseNode(opcBrowseNode)
			if udtPath:
				browseElement = opcBrowseNode.getBrowseElement()
				self.createInstance(udtPath,browseElement.getItemId(),browseElement.getServer())
			else:
				unrecognizedOpcBrowseNodes.append(str(opcBrowseNode))
		self.handleUnrecognizedOpcBrowseNodes(unrecognizedOpcBrowseNodes)
	
	def createInstance(self,udtPath,opcNodeId,opcServerName):
		folderPath = self.getInstanceFolderPath(udtPath,opcNodeId,opcServerName)
		tagConfig = {
			"name": self.getInstanceName(udtPath,opcNodeId,opcServerName),         
			"typeId" : tag_tools.shortenUdtPath(udtPath),
			"tagType" : "UdtInstance",
			"parameters" : self.getInstanceParams(udtPath,opcNodeId,opcServerName)
		}
		collisionPolicy = "a"
		tag_tools.createFolderAndParentFolders(folderPath)
		qualitycodes = system.tag.configure(folderPath, [tagConfig], collisionPolicy)
		if logger.isDebugEnabled():
			import pprint
			logger.debug(
				"new instance ... \n" + 
				"folderPath=" + folderPath+"\n" +
				"tagConfig=\n" + pprint.pformat(tagConfig)+"\n"+
				"configResults=\n" + str(qualitycodes)
				)
		if qualitycodes[0].isGood():
			self.onInstanceCreated(folderPath,tagConfig)
	
	def getInstanceName(self,udtPath,opcNodeId,opcServerName):
		raise NotImplementedError
	
	def getInstanceParams(self,udtPath,opcNodeId,opcServerName):
		raise NotImplementedError
	
	def getInstanceFolderPath(self,udtPath,opcNodeId,opcServerName):
		raise NotImplementedError
	
	def handleUnrecognizedOpcBrowseNodes(self,unrecognizedOpcBrowseNodes):
		return
		
	def onInstanceCreated(self,folderPath,tagConfig):
		return

	def getUnrecognizedOpcBrowseNodesMessage(self,unrecognizedOpcBrowseNodes):
		message = list_tools.createListMessage(unrecognizedOpcBrowseNodes,"Cannot auto-create tags from OPC Browse Node(s):")
		message += list_tools.createListMessage(self.opcTypeRecognizer.getRegisteredUdtPaths(),"Child nodes must match OPC requirements for one of the registered UDTs:")
		return message