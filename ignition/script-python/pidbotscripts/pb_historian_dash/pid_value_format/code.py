def formatPidbotValue(rawValue,name):
	# Map enumerated properties to text values
	textSwitcher = {
		'pidForm':{0:'Independent',1:'Dependent'},
		'pidAction':{0:'E=SP-PV',1:'E=PV-SP'},
		'timeUnit':{3:'Seconds',4:'Minutes'},
		'processType':{0:'FOPDT',1:'IPDT'}
	}
	if textSwitcher.get(name,{}):
		return textSwitcher.get(name,{}).get(rawValue,"Undefined")
	# Format float values with significant digits
	if isinstance(rawValue,(float)):
		if(rawValue<1000):
			return '%.3g' % (rawValue)
		return '%1.0f' % (rawValue)
	return rawValue