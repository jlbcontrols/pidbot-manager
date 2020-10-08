from com.inductiveautomation.ignition.common.tags.model import TagPath
from com.inductiveautomation.ignition.common.tags.paths.parser import TagPathParser
import pidbotscripts.utils.list_tools as list_tools

logger = system.util.getLogger(__name__)

def coerceToTagPathObject(path):
	if isinstance(path,TagPath):
		return path
	return TagPathParser.parseSafe(path)
	

def commonAncestorOf(paths,tagProvider):
	shortestPathLength = sys.maxsize #sys.maxint
	shortestPath = None
	tagPaths = []
	for path in paths:
		tagPath = coerceToTagPathObject(path)
		tagPaths.append(tagPath)
		if tagPath.getPathLength()<shortestPathLength:
			shortestPathLength=tagPath.getPathLength()
			shortestPath = tagPath
	
	ancestorPath = "["+tagProvider+"]"
	for i in range(0,shortestPathLength):
		pathSegment = shortestPath.getPathComponent(i).lower()
		for tagPath in tagPaths:
			if tagPath.getPathComponent(i).lower() != pathSegment:
				return ancestorPath
		ancestorPath += pathSegment + '/'
	return ancestorPath


def sortTagsByProvider(paths):
	tagPaths = [coerceToTagPathObject(path) for path in paths]
	tagDict = {}
	for tagPath in tagPaths:
		provider = tagPath.getSource()
		if provider not in tagDict.keys():
			tagDict[provider]=[tagPath.toStringFull()]
		else:
			tagDict[provider].append(tagPath.toStringFull())
	return tagDict
	
	
def shortenUdtPath(udtPath):
	splitPath = udtPath.split("_types_/")
	if len(splitPath)==2:
		return splitPath[1]
	return udtPath
	
	
def getUdtInstancePathsInFolder(udtPath,folderPath):
	children = system.tag.browse(folderPath).getResults()
	pathList = []
	if children!=None:
		shortUdtPath = shortenUdtPath(udtPath)
		for child in children:      
			if str(child['tagType']) == "UdtInstance" and str(child['typeId']).endswith(shortUdtPath):
				childPath = str(child['fullPath'])
				pathList.append(childPath)
	return pathList


def createFolderAndParentFolders(folderPath):
	if system.tag.exists(folderPath):
		return
	pathSegments = folderPath.split("/")
	if pathSegments[0].startswith("["):
		parentPath = pathSegments.pop(0)
	else:
		parentPath = ""
	collisionPolicy = "a"
	for pathSegment in pathSegments:
		folderConfig = {
			"name": pathSegment,         
			"tagType" : "Folder",
		}
		qc = system.tag.configure(parentPath, [folderConfig], collisionPolicy)
		if logger.isDebugEnabled():
			logger.debug(str(qc[0]))
		parentPath+= "/" + pathSegment
	if not system.tag.exists(folderPath):
		raise Exception("Folder '%s' could not be created." % folderPath)


class TagQualityException(Exception):
	def __init__(self, tagPaths, qualitycodes, baseMessage="Error updating tags."):
		self.qualDict = dict(zip(tagPaths,qualitycodes))
		self.baseMessage = baseMessage
		Exception.__init__(self,self.getTagQualMessage(includeGood=False))
	def getTagsByQuality(self):
		tagsByQual = {
			"good":[],
			"notGood":{}
		}
		for tagPath,qc in self.qualDict.items():
			if qc.good:
				tagsByQual["good"].append(tagPath)
			else:
				tagsByQual["notGood"].setdefault(qc, []).append(tagPath)
		return tagsByQual
	def getTagQualMessage(self,includeGood=True):
		tagsByQual = self.getTagsByQuality()
		message = self.baseMessage + "\n"
		for qc,tagPaths in tagsByQual["notGood"].items():
			message += list_tools.createListMessage(tagPaths,"Quality Code=%s" % str(qc)) + "\n"
		if includeGood:
			message += list_tools.createListMessage(tagsByQual["good"],"The following tags were updated successfully:") + "\n"
		return message


class TagConfigQualityException(TagQualityException):
	def __init__(self, tagPaths, qualitycodes, baseMessage="Error configuring tags."):
		TagQualityException.__init__(self, tagPaths, qualitycodes, baseMessage)
			
			
class TagWriteQualityException(TagQualityException):
	def __init__(self, tagPaths, qualitycodes, baseMessage="Error writing to tags."):
		TagQualityException.__init__(self, tagPaths, qualitycodes, baseMessage)


def writeBlockingRaiseException(tagPaths,values,timeout=45000):
	qualitycodes = system.tag.writeBlocking(tagPaths,values,timeout)
	for qc in qualitycodes:
		if not qc.good:
			raise TagWriteQualityException(tagPaths,qualitycodes)		
		
		
def configureRaiseException(basePath, tags, collisionPolicy="a"):
	qualitycodes = system.tag.configure(basePath, tags, collisionPolicy)
	for qc in qualitycodes:
		if not qc.good:
			tagPaths = [basePath+"/"+tag['name'] for tag in tags]
			raise TagConfigQualityException(tagPaths,qualitycodes)



### Testing ####
def createFolderAndParentFoldersTest():
	folderPath = "[default]test22341/test352341/test41/test5253"
	createFolderAndParentFolders(folderPath)
	assert system.tag.exists(folderPath)
	folderPath = "test2478/test33568/test43568/test53568"
	createFolderAndParentFolders(folderPath)
	assert system.tag.exists(folderPath)