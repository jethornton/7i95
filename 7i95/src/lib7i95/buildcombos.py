def build(parent):
	ipAddress = [
	['Select', False],
	['10.10.10.10', '"10.10.10.10"'],
	['192.168.1.121', '"192.168.1.121"']
	]
	for item in ipAddress:
		parent.ipAddressCB.addItem(item[0], item[1])

	axes = [
		['Select', False],
		['X', 'X'],
		['Y', 'Y'],
		['Z', 'Z'],
		['A', 'A'],
		['B', 'B'],
		['C', 'C'],
		['U', 'U'],
		['V', 'V'],
		['W', 'W']
		]
	for i in range(6):
		for item in axes:
			getattr(parent, f'axisCB_{i}').addItem(item[0], item[1])

	linearUnits = [
		['Select', False],
		['Imperial', 'inch'],
		['Metric', 'metric']
		]

	for item in linearUnits:
		parent.linearUnitsCB.addItem(item[0], item[1])

	gui = [
		['Select', False],
		['Axis', 'axis'],
		['Touchy', 'touchy']
		]

	for item in gui:
		parent.guiCB.addItem(item[0], item[1])

	positionOffset = [
		['Select', False],
		['Relative', 'RELATIVE'],
		['Machine', 'MACHINE']
		]

	for item in positionOffset:
		parent.positionOffsetCB.addItem(item[0], item[1])

	positionFeedback = [
		['Select', False],
		['Commanded', 'COMMANDED'],
		['Actual', 'ACTUAL']
		]

	for item in positionFeedback:
		parent.positionFeedbackCB.addItem(item[0], item[1])

	ssCards = [
		['Select', False],
		['7i64', '7i64'],
		['7i69', '7i69'],
		['7i70', '7i70'],
		['7i71', '7i71'],
		['7i72', '7i72'],
		['7i73', '7i73'],
		['7i84', '7i84'],
		['7i87', '7i87']
		]

	for item in ssCards:
		parent.ssCardCB.addItem(item[0], item[1])

	drives = [
		['Custom', False],
		['Gecko 201', ['500', '4000', '20000', '1000']],
		['Gecko 202', ['500', '4500', '20000', '1000']],
		['Gecko 203v', ['1000', '2000', '200', '200']],
		['Gecko 210', ['500', '4000', '20000', '1000']],
		['Gecko 212', ['500', '4000', '20000', '1000']],
		['Gecko 320', ['3500', '500', '200', '200']],
		['Gecko 540', ['1000', '2000', '200', '200']],
		['L297', ['500', '4000', '4000', '1000']],
		['PMDX 150', ['1000', '2000', '1000', '1000']],
		['Sherline', ['22000', '22000', '100000', '100000']],
		['Xylotex BS-3', ['2000', '1000', '200', '200']],
		['Parker 750', ['1000', '1000', '1000', '200000']],
		['JVL SMD41/42', ['500', '500', '2500', '2500']],
		['Hobbycnc', ['2000', '2000', '2000', '2000']],
		['Keling 4030', ['5000', '5000', '20000', '20000']]
		]

	for i in range(6):
		for item in drives:
			getattr(parent, f'driveCB_{i}').addItem(item[0], item[1])