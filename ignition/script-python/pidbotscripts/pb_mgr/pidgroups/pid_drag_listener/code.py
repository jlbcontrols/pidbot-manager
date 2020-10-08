from java.awt.dnd import DragSource,DragGestureListener
from java.awt.dnd import DragSourceListener 
from java.awt.dnd import DnDConstants
from java.awt.datatransfer import Transferable
from java.awt.datatransfer import StringSelection
import pidbotscripts.utils.component_tools as component_tools

def addPidDragListener(pidDraggableComponent):
	# Check if component has required custom properties to add the PidDragListener
	requiredProps = ['instancePath','draggedFrom']
	propsNotFound = component_tools.componentMissingProps(pidDraggableComponent,requiredProps)
	if propsNotFound:
		errorMessage = "Component %s does not have custom properties required to use addPidDragListener(component): %s" % (pidDraggableComponent.getName(),propsNotFound)
		system.gui.errorBox(errorMessage)
		return
	dragSource = DragSource()
	pidDragSourceListener = PidDragSourceListener(pidDraggableComponent)
	pidDragGestureListener = PidDragGestureListener(pidDraggableComponent, dragSource, pidDragSourceListener)
	dragSource.createDefaultDragGestureRecognizer(pidDraggableComponent,DnDConstants.ACTION_COPY_OR_MOVE, pidDragGestureListener)
	
	
class PidDragGestureListener(DragGestureListener):
	def  __init__(self,pidDraggableComponent, dragSource, dragSourceListener):
		DragGestureListener.__init__(self)
		self.pidDraggableComponent = pidDraggableComponent
		self.dragSource = dragSource
		self.dragSourceListener = dragSourceListener
		
	def dragGestureRecognized(self,DragGestureEvent): 
		self.pidDraggableComponent.draggedFrom=True
		transferable = StringSelection(self.pidDraggableComponent.instancePath);
		self.dragSource.startDrag(DragGestureEvent, DragSource.DefaultCopyDrop, transferable, self.dragSourceListener)


class PidDragSourceListener(DragSourceListener):
	def __init__(self,pidDraggableComponent):
		DragSourceListener.__init__(self)
		self.pidDraggableComponent = pidDraggableComponent
	
	def dragDropEnd(self,e):
		self.pidDraggableComponent.draggedFrom=False
	
	def dragOver(self,e):
		return
	
	def dragEnter(self,e):
		return
	
	def dragExit(self,e):
		return
	
