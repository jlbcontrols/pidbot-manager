from java.awt.dnd import DropTargetListener, DropTarget
from java.awt.datatransfer import DataFlavor
from com.inductiveautomation.ignition.client.tags.dnd import ListOfNodeBrowseInfo
import pidbotscripts.utils.component_tools as component_tools
import pidbotscripts.pb_mgr.pidgroups.members.add_pid as add_pid


def addPidDropListener(pidDroppableComponent):
	# Check if component has required custom properties to add the PidDropListener
	requiredProps = ['pidGroupPath','dropBeforeTagPath','dragEntered']
	propsNotFound = component_tools.componentMissingProps(pidDroppableComponent,requiredProps)
	if propsNotFound:
		errorMessage = "Component %s does not have custom properties required to use addPidDropListener(component): %s" % (pidDroppableComponent.getName(),propsNotFound)
		system.gui.errorBox(errorMessage)
		return
	pidDropListener = PidDropListener(pidDroppableComponent)
	DropTarget(pidDroppableComponent, pidDropListener)
	

class PidDropListener(DropTargetListener):
	def __init__(self, pidDroppableComponent):
		DropTargetListener.__init__(self)
		self.pidDroppableComponent = pidDroppableComponent
			
	def drop(self, e):
		self.pidDroppableComponent.dragEntered=False		
		newTagPaths = getTagPathListFromDropEvent(e)
		pidGroupPath = self.pidDroppableComponent.pidGroupPath
		dropBeforeTagPath = self.pidDroppableComponent.dropBeforeTagPath
		add_pid.addTagsToGroup(newTagPaths,pidGroupPath,dropBeforeTagPath)
		
	def dragOver(self,e):
		return
	
	def dragEnter(self,e):
		self.pidDroppableComponent.dragEntered=True
	
	def dragExit(self,e):
		self.pidDroppableComponent.dragEntered=False


def getTagPathListFromDropEvent(e):
	if e.isDataFlavorSupported(ListOfNodeBrowseInfo.FLAVOR):
		transferData = e.getTransferable().getTransferData(ListOfNodeBrowseInfo.FLAVOR)
		tagPathList = [str(tag.getFullPath()) for tag in transferData]
	elif e.isDataFlavorSupported(DataFlavor.stringFlavor):
		transferData = e.getTransferable().getTransferData(DataFlavor.stringFlavor)
		tagPathList = [str(transferData)]
	else:
		raise Exception("Drop data types: %s not supported" % e.getCurrentDataFlavorsAsList())
	if len(tagPathList)>20:
		if not system.gui.confirm("Add %s tags to Tag Group?" % len(transferData)):
			return []
	return tagPathList
	