# Called by input comoponents to enable/diable based on role
def isAllowed(componentRoles):
	componentRoleList = componentRoles.getColumnAsList(0)
	if len(componentRoleList)==0:
		return True
	userRoles = system.tag.readBlocking(["[System]Client/User/RolesDataSet"])[0].value
	userRoleList = userRoles.getColumnAsList(0)
	for componentRole in componentRoleList:
		if componentRole in  userRoleList:
			return True
	return False