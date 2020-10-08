import pidbotscripts.utils.list_tools as list_tools


# Check if a component (e.g. template) has a list of property names as custom properties
def componentMissingProps(component,requiredPropNames):
	customPropNames = [str(prop) for prop in component.getProperties()]
	return list_tools.itemsNotInList(requiredPropNames,customPropNames)