# Query raw tag history data, extend bounding values to fill entire time range.
# Last known values are used for the new points (Should only use for step-interpolated/on-change historical data).
def queryTagHistoryFillRange(tagPath,startDate,endDate):
	# Query Raw data for time range	
	dsRaw = system.tag.queryTagHistory(
			paths=[tagPath],
			startDate=startDate,
			endDate=endDate,
			returnSize=-1,
			returnFormat="Wide",
			includeBoundingValues=True
			)
	
	#If there is no data recorded, return the empty dataset
	if dsRaw.getRowCount() == 0:
		return dsRaw
	
	#Move start bounding value to the chart start time
	dsWithStart = system.dataset.setValue(dsRaw,0,0,startDate)
	
	#Duplicate end value at chart end time 
	lastValue = dsRaw.getValueAt(dsRaw.getRowCount()-1,1)
	dsWithEnd = system.dataset.addRow(dsWithStart,[endDate,lastValue])
	return dsWithEnd