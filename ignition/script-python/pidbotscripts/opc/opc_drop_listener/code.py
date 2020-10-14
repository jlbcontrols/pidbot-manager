# This script is intended for use with the Vision Client OPC Browser component from JLB Controls as a drag source.

logger = system.util.getLogger('opc_drop_listener')
from com.jlbcontrols.vcob import OpcBrowseNodeListTransferable
from java.awt.dnd import DropTargetListener, DropTarget
from java.awt.datatransfer import DataFlavor
from com.inductiveautomation.ignition.client.tags.dnd import ListOfNodeBrowseInfo
import pidbotscripts.pb_mgr.pidtags.pidbot_instance_generator.PidbotInstanceGenerator as PidbotInstanceGenerator
import pidbotscripts.utils.component_tools as component_tools


def addOpcDropListener(opcDroppableComponent,instanceGenerator):
	# Check if component has required custom properties to add the OpcDropListener
	requiredProps = ['dragEntered']
	propsNotFound = component_tools.componentMissingProps(opcDroppableComponent,requiredProps)
	if propsNotFound:
		errorMessage = "Component %s does not have custom properties required to add an OpcDropListener: %s" % (opcDroppableComponent.getName(),propsNotFound)
		system.gui.errorBox(errorMessage)
		return
	opcDropListener = OpcDropListener(opcDroppableComponent,instanceGenerator)
	DropTarget(opcDroppableComponent, opcDropListener)


class OpcDropListener(DropTargetListener):
	def __init__(self, opcDroppableComponent,instanceGenerator):
		DropTargetListener.__init__(self)
		self.opcDroppableComponent = opcDroppableComponent
		self.instanceGenerator = instanceGenerator
			
	def drop(self, e):
		self.opcDroppableComponent.dragEntered=False
		browseNodes = getOpcBrowseNodesFromDropEvent(e)
		logger.debug("Dropped browseNodes="+str(browseNodes))
		self.instanceGenerator.createFromOpcBrowseNodes(browseNodes)
		self.opcDroppableComponent.dropComplete()
		
	def dragOver(self,e):
		return
	
	def dragEnter(self,e):
		self.opcDroppableComponent.dragEntered=True
	
	def dragExit(self,e):
		self.opcDroppableComponent.dragEntered=False


def getOpcBrowseNodesFromDropEvent(e):
	if e.isDataFlavorSupported(OpcBrowseNodeListTransferable.FLAVOR):
		browseNodes = e.getTransferable().getTransferData(OpcBrowseNodeListTransferable.FLAVOR)
	else:
		raise Exception("Drop data types: %s not supported" % e.getCurrentDataFlavorsAsList())
	if len(browseNodes)>20:
		if not system.gui.confirm("Create %s new tags?" % len(browseNodes)):
			return []
	return browseNodes
