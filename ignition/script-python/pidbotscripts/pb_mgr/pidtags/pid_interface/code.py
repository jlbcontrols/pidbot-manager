import pidbotscripts.tagnode.node_checker as node_checker
import pidbotscripts.tagnode.tag_config_node as tag_config_node
import pidbotscripts.utils.tag_tools as tag_tools

logger = system.util.getLogger(__name__)

def validatePidbotTags(paths):
	logger = system.util.getLogger("pid_interface")
	tagDict = tag_tools.sortTagsByProvider(paths)
	for provider in tagDict.keys():
		baseTagPath = tag_tools.commonAncestorOf(tagDict[provider],provider)
		baseNode = tag_config_node.createRootNodeForPath(baseTagPath)
		if logger.isDebugEnabled():
			import pprint
			logger.debug(
				"checking tags in configuration tree ... \n" + 
				pprint.pformat(baseNode.tagConfig)
				)
		for path in tagDict[provider]:
			node = baseNode.getNodeForPath(path)
			for checker in createPidbotNodeCheckers():
				if not checker.check(node):
					return False,checker.getFailureMessage(node)
	return True,""			
	

def createPidbotNodeCheckers():
	tagExistsChecker = node_checker.NodeExistsChecker()
	tagIsUdtInstanceChecker = node_checker.TagTypeChecker(["UdtInstance"])
	childChecker = node_checker.ChildrenRequiredChecker([
		'currentP',
		'currentI',
		'currentD',
		'cv',
		'cvScaleHigh',
		'cvScaleLow',
		'loopIdentifier',
		'loopName',
		'pidAction',
		'pidForm',
		'processDeadTime',
		'processGain',
		'processTimeConst',
		'processType',
		'pv',
		'pvScaleHigh',
		'pvScaleLow',
		'sp',
		'timeUnit' 
	])
	paramChecker = node_checker.ParamsRequiredChecker([
		'recordingTagGroup'
	])
	return [tagExistsChecker,tagIsUdtInstanceChecker,childChecker,paramChecker]
