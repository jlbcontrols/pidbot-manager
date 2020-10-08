import pidbotscripts.opc.udt_instance_generator as udt_instance_generator
import pidbotscripts.opc.opc_type_recognizer as opc_type_recognizer
import pidbotscripts.utils.list_tools as list_tools
import pidbotscripts.utils.tag_tools as tag_tools

class PidbotInstanceGenerator(udt_instance_generator.AbstractUdtInstanceGenerator):
	def __init__(self,instanceRootFolderPath,opcRecognizedUdtPaths):
		self.instanceRootFolderPath = instanceRootFolderPath
		opcTypeRecognizer = opc_type_recognizer.OpcMultiTypeRecognizer(opcRecognizedUdtPaths)
		udt_instance_generator.AbstractUdtInstanceGenerator.__init__(self,opcTypeRecognizer)
	
	def getInstanceName(self,udtPath,opcNodeId,opcServerName):
		return opcNodeId.split(']')[1].replace(".","_")
	
	def getInstanceParams(self,udtPath,opcNodeId,opcServerName):
		params = {}
		params['opcPrefix'] = opcNodeId.split('[')[0]
		params['plcName'] = opcNodeId.split('[')[1].split(']')[0]
		params['plcTag'] = opcNodeId.split(']')[1]
		params['opcServName'] = opcServerName
		return params
	
	def getInstanceFolderPath(self,udtPath,opcNodeId,opcServerName):
		params = self.getInstanceParams(udtPath,opcNodeId,opcServerName)
		return self.instanceRootFolderPath + "/" + params['opcServName'] + "/" + params['plcName']
	
	def onInstanceCreated(self,folderPath,tagConfig):
		loopNamePath = folderPath + "/" + tagConfig['name'] + "/loopName"
		system.tag.write(loopNamePath, tagConfig['name'])
	
	def handleUnrecognizedOpcBrowseNodes(self,unrecognizedOpcBrowseNodes):
		if unrecognizedOpcBrowseNodes:
			errorMessage = self.getUnrecognizedOpcBrowseNodesMessage(self,unrecognizedOpcBrowseNodes)
			system.gui.messageBox(errorMessage, "Error recognizing some requested tags.")	


# Testing
def createInstanceTest(plcTag = "LC1", udtPath = "[default]_types_/PidbotTypes/Pid/Studio5000/P_PIDE",instanceRootFolderPath="[default]PidbotInst/PidTags"):
	opcPrefix = "ns=1;s="
	plcName = "plc1"
	opcNodeId = opcPrefix+"["+plcName+"]"+plcTag
	opcServerName = "Ignition OPC UA Server"
	pidInstanceGenerator = PidbotInstanceGenerator(instanceRootFolderPath,[udtPath])
	tagName = pidInstanceGenerator.getInstanceName(udtPath,opcNodeId,opcServerName)
	instancePath = pidInstanceGenerator.getInstanceFolderPath(udtPath,opcNodeId,opcServerName)+"/"+tagName
	if system.tag.exists(instancePath):
		raise Exception("createInstanceTest not valid, tag already exists")
	pidInstanceGenerator.createInstance(udtPath,opcNodeId,opcServerName)
	newTagConfig = system.tag.getConfiguration(instancePath)[0]
	assert str(newTagConfig['tagType']) == 'UdtInstance'
	assert str(newTagConfig['typeId']) == tag_tools.shortenUdtPath(udtPath)
	params = newTagConfig['parameters']
	# .value needed for 8.0.16, not 8.0.12
	assert params['opcPrefix'].value==opcPrefix
	assert params['opcServName'].value==opcServerName
	assert params['plcTag'].value==plcTag
	assert params['plcName'].value==plcName
	loopName = system.tag.read(instancePath+"/loopName").value
	print loopName
	assert loopName == plcTag


def getInstanceParamsTest(plcTag = "LC1", opcPrefix = "ns=1;s=", plcName = "plc1", opcServerName = "Ignition OPC UA Server"):
	opcNodeId = opcPrefix+"["+plcName+"]"+plcTag
	udtPath = "[default]_types_/PidbotTypes/Pid/Studio5000/P_PIDE"
	instanceRootFolderPath="some/path/for/test"
	pidInstanceGenerator = PidbotInstanceGenerator(instanceRootFolderPath,[udtPath])
	params = pidInstanceGenerator.getInstanceParams("",opcNodeId,opcServerName)
	assert params['opcPrefix'] == opcPrefix
	assert params['plcName'] == plcName
	assert params['plcTag'] == plcTag