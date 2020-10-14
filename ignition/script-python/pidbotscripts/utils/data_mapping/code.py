def listToColumnDs(list,header="values"):
	headers = [header]
	data = [[item] for item in list]
	return system.dataset.toDataSet(headers,data)

def dictToRowDs(dict):
	row = []
	headers = []
	for key, value in dict.items():
		headers.append(key)
		row.append(value)
	return system.dataset.toDataSet(headers,[row])

def rowDsToDict(dataset):
	dict = {}
	for col in range(0,dataset.getColumnCount()):
		dict[dataset.getColumnName(col)] = dataset.getValueAt(0,col)
	return dict