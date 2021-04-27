import os
from datetime import datetime

def build(parent):
	for i in range(11):
		inputText = getattr(parent, f'inputPB_{i}').text()
		if inputText ==  'E-Stop':
			external_estop = True
			break
		else:
			external_estop = False
	halFilePath = os.path.join(parent.configPath, parent.configNameUnderscored + '.hal')
	parent.outputPTE.appendPlainText(f'Building {halFilePath}')

	halContents = []
	halContents = ['# This file was created with the 7i95 Configuration Tool on ']
	halContents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	halContents.append('# If you make changes to this file DO NOT run the configuration tool again!\n')
	halContents.append('# This file will be replaced with a new file if you do!\n\n')
