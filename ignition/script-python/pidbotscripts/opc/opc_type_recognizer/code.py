logger = system.util.getLogger('opc_type_recognizer')

class OpcTypeRecognizer:
	def __init__(self,udtPath):
		opcBindings = getOpcBindingsInUdt(udtPath)
		self.requiredOpcChildNames = getRequiredOpcChildNames(opcBindings)
		self.udtPath = udtPath

	def recognize(self, opcChildNames):
		if logger.isDebugEnabled():
			logger.debug("requiredOpcChildNames="+str(self.requiredOpcChildNames))
		for requiredChildName in self.requiredOpcChildNames:
			if not requiredChildName in opcChildNames:
				if logger.isDebugEnabled():
					logger.debug("requiredChildName: " + requiredChildName + " not found in opcChildNames.")
				return False
		return self.udtPath
	
	def recognizeOpcBrowseNode(self, opcBrowseNode):
		return recognizeOpcBrowseNode(self, opcBrowseNode)

	def getRegisteredUdtPaths(self):
		return [self.udtPath]


class OpcMultiTypeRecognizer:
	def __init__(self,udtPaths):
		self.typeRecognizers = []
		for udtPath in udtPaths:
			self.typeRecognizers.append(OpcTypeRecognizer(udtPath))

	def recognize(self, opcChildNames):
		for recognizer in self.typeRecognizers:
			recognizedUdtPath = recognizer.recognize(opcChildNames)
			if recognizedUdtPath:
				return recognizedUdtPath
		return False

	def recognizeOpcBrowseNode(self, opcBrowseNode):
		return recognizeOpcBrowseNode(self, opcBrowseNode)
		
	def getRegisteredUdtPaths(self):
		return [typeRecognizer.udtPath for typeRecognizer in self.typeRecognizers]

def recognizeOpcBrowseNode(typeRecognizer, opcBrowseNode):
	childNodes = opcBrowseNode.getChildNodes()
	if childNodes:
		opcChildNames = [childNode.getBrowseElement().getItemName() for childNode in childNodes]
		recognizedUdtPath = typeRecognizer.recognize(opcChildNames)
		return recognizedUdtPath
	return False

# Get "top level" child names in a given OPC node/server address
def getOpcChildNames(serverName, nodeId):
	children = system.opc.browseServer(serverName, nodeId)
	childNames = []
	for child in children:
		childNames.append(child.getDisplayName())
	return childNames

# Get OPC members that are required for a given UDT definition, given all of the UDT's OPC binding information
def getRequiredOpcChildNames(opcBindings):
	requiredOpcChildNames = []
	for opcBinding in opcBindings:
		if "." in opcBinding:
			requiredOpcChildNames.append(opcBinding.split(".")[1])  # Note, this only looks for "top level" opc child paths. If grandchildren, etc. are included in OPC bindings, only the child folder name will be returned.
	return requiredOpcChildNames

# Returns all OPC binding paths in a UDT Type that include "parameter bindings"
def getOpcBindingsInUdt(udtPath):
	tagConfig = system.tag.getConfiguration(udtPath,True)[0]
	logger.debug("UdtName="+ tagConfig['name'])
	if str(tagConfig['tagType'])=='Unknown':
		raise Exception("Cannot recognize tags for type:\n%s\nType definition not found." % udtPath)
	if str(tagConfig['tagType'])!='UdtType':
		raise Exception("Cannot recognize tags for type:\n%s\nis not a valid UDT Type." % udtPath)
	return getOpcBindingsRecursive(tagConfig,[])
		
from com.inductiveautomation.ignition.common.config import BoundValue
def getOpcBindingsRecursive(tagConfig,bindingList):
	for childConfig in tagConfig.get('tags',[]):
		if childConfig.get('tags',False):
			getOpcBindingsRecursive(childConfig,bindingList)
		elif str(childConfig.get('valueSource',False))=='opc':
			if isinstance(childConfig['opcItemPath'],BoundValue):
				bindingList.append(str(childConfig['opcItemPath'].getBinding()))
	logger.debug("bindingList="+str(bindingList))
	return bindingList

# Testing
def opcTypeRecognizerTest():
	path = "[default]_types_/PidbotTypes/Pid/Studio5000/P_PIDE"
	p_pideTypeRecognizer = OpcTypeRecognizer(path)
	serverName = 'Ignition OPC UA Server'
	nodeId = 'ns=1;s=[plc1]LC1'
	opcChildNames = getOpcChildNames(serverName, nodeId)
	assert p_pideTypeRecognizer.recognize(opcChildNames) == path

