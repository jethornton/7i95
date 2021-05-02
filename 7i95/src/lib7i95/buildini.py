import os
from datetime import datetime

def build(parent):
	buildErrors = []
	iniFilePath = os.path.join(parent.configPath, parent.configNameUnderscored + '.ini')
	parent.outputPTE.appendPlainText(f'Building {iniFilePath}')

	if os.path.isfile(iniFilePath):
		pass

	if not os.path.exists(parent.configPath):
		try:
			os.mkdir(parent.configPath)
		except OSError:
			parent.outputPTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	iniContents = ['# This file was created with the 7i95 Configuration Tool on ']
	iniContents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	iniContents.append('# Changes to most things are ok and will be read by the Configuration Tool\n')

	# build the [7i95] section
	iniContents.append('\n[7I95]\n')
	iniContents.append(f'VERSION = {parent.version}\n')

	# build the [EMC] section
	iniContents.append('\n[EMC]\n')
	iniContents.append(f'VERSION = {parent.emcVersion}\n')
	iniContents.append(f'MACHINE = {parent.configNameUnderscored}\n')
	iniContents.append(f'DEBUG = {parent.debugCB.currentData()}\n')

	# build the [HOSTMOT2] section
	iniContents.append('\n[HOSTMOT2]\n')
	iniContents.append('DRIVER = hm2_eth\n')
	iniContents.append(f'IPADDRESS = {parent.ipAddressCB.currentData()}\n')
	iniContents.append('BOARD = 7i95\n')
	iniContents.append(f'STEPGENS = {str(parent.stepgensCB.currentData())}\n')
	iniContents.append(f'ENCODERS = {str(parent.encodersCB.currentData())}\n')
	iniContents.append(f'PWMS = {str(parent.pwmsCB.currentData())}\n')
	#iniContents.append(f'SSERIAL_PORT = {str(parent.sserialSB.value())}\n')
	iniContents.append(f'FIRMWARE = {parent.firmwareCB.currentData()}\n')

	# build the [DISPLAY] section maxFeedOverrideLE
	iniContents.append('\n[DISPLAY]\n')
	iniContents.append(f'DISPLAY = {parent.guiCB.itemData(parent.guiCB.currentIndex())}\n')
	iniContents.append(f'POSITION_OFFSET = {parent.positionOffsetCB.currentData()}\n')
	iniContents.append(f'POSITION_FEEDBACK = {parent.positionFeedbackCB.currentData()}\n')
	iniContents.append(f'MAX_FEED_OVERRIDE = {parent.maxFeedOverrideSB.value()}\n')
	iniContents.append('CYCLE_TIME = 0.1\n')
	iniContents.append(f'INTRO_GRAPHIC = {parent.introGraphicLE.text()}\n')
	iniContents.append(f'INTRO_TIME = {parent.splashScreenSB.value()}\n')
	iniContents.append('OPEN_FILE = ""\n')
	if parent.pyvcpCB.isChecked():
		iniContents.append(f'PYVCP = {parent.configNameUnderscored}.xml\n')
	if parent.frontToolLatheCB.isChecked():
		iniContents.append('LATHE = 1\n')
	if parent.frontToolLatheCB.isChecked():
		iniContents.append('BACK_TOOL_LATHE = 1\n')

	# build the [KINS] section
	iniContents.append('\n[KINS]\n')
	if len(set(parent.coordinatesLB.text())) == len(parent.coordinatesLB.text()): # 1 joint for each axis
		iniContents.append('KINEMATICS = trivkins coordinates={parent.coordinatesLB.text()}\n')
	else: # more than one joint per axis
		iniContents.append(f'KINEMATICS = trivkins coordinates={parent.coordinatesLB.text()} kinstype=BOTH\n')
	iniContents.append(f'JOINTS = {len(parent.coordinatesLB.text())}\n')

	# build the [EMCIO] section
	iniContents.append('\n[EMCIO]\n')
	iniContents.append('EMCIO = iov2\n')
	iniContents.append('CYCLE_TIME = 0.100\n')
	iniContents.append('TOOL_TABLE = tool.tbl\n')

	# build the [RS274NGC] section
	iniContents.append('\n[RS274NGC]\n')
	iniContents.append(f'PARAMETER_FILE = {parent.configNameUnderscored}.var\n')

	# build the [EMCMOT] section
	iniContents.append('\n[EMCMOT]\n')
	iniContents.append('EMCMOT = motmod\n')
	iniContents.append(f'SERVO_PERIOD = {parent.servoPeriodSB.value()}\n')

	# build the [TASK] section
	iniContents.append('\n[TASK]\n')
	iniContents.append('TASK = milltask\n')
	iniContents.append('CYCLE_TIME = 0.010\n')

	# build the [TRAJ] section
	iniContents.append('\n[TRAJ]\n')
	iniContents.append(f'COORDINATES = {parent.coordinatesLB.text()}\n')
	iniContents.append(f'LINEAR_UNITS = {parent.linearUnitsCB.currentData()}\n')
	#iniContents.append(f'ANGULAR_UNITS = {parent.angularUnitsCB.currentData()}\n')
	iniContents.append(f'MAX_LINEAR_VELOCITY = {parent.maxLinearVel.text()}\n')

	# build the [HAL] section
	iniContents.append('\n[HAL]\n')
	iniContents.append(f'HALFILE = {parent.configNameUnderscored}.hal\n')
	iniContents.append('HALFILE = io.hal\n')
	if parent.ssCardCB.currentData():
		iniContents.append('HALFILE = sserial.hal\n')
	if parent.customhalCB.isChecked():
		iniContents.append('HALFILE = custom.hal\n')
	if parent.postguiCB.isChecked():
		iniContents.append('POSTGUI_HALFILE = postgui.hal\n')
	if parent.shutdownCB.isChecked():
		iniContents.append('SHUTDOWN = shutdown.hal\n')
	if parent.haluiCB.isChecked():
		iniContents.append('HALUI = halui\n')

	# build the [HALUI] section
	iniContents.append('\n[HALUI]\n')

	# build the axes
	for i in range(parent.card['joints']):
		axis = getattr(parent, f'axisCB_{i}').currentData()
		if axis:
			jointTab = getattr(parent, f'axisCB_{i}').objectName()[7]
			iniContents.append(f'\n[AXIS_{axis}]\n')
			iniContents.append(f'MIN_LIMIT = {getattr(parent, f"minLimit_{jointTab}").text()}\n')
			iniContents.append(f'MAX_LIMIT = {getattr(parent, f"maxLimit_{jointTab}").text()}\n')
			iniContents.append(f'MAX_VELOCITY = {getattr(parent, f"maxVelocity_{jointTab}").text()}\n')
			iniContents.append(f'MAX_ACCELERATION = {getattr(parent, f"maxAccel_{jointTab}").text()}\n')

	# build the [JOINT_n] sections
	for i in range(parent.card['joints']):
		if getattr(parent, f"axisCB_{i}").currentData():
			iniContents.append(f'\n[JOINT_{i}]\n')
			iniContents.append(f'AXIS = {getattr(parent, f"axisCB_{i}").currentData()}\n')
			iniContents.append(f'MIN_LIMIT = {getattr(parent, f"minLimit_{i}").text()}\n')
			iniContents.append(f'MAX_LIMIT = {getattr(parent, f"maxLimit_{i}").text()}\n')
			iniContents.append(f'MAX_VELOCITY = {getattr(parent, f"maxVelocity_{i}").text()}\n')
			iniContents.append(f'MAX_ACCELERATION = {getattr(parent, f"maxAccel_{i}").text()}\n')
			iniContents.append(f'TYPE = {getattr(parent, f"axisType_{i}").text()}\n')
			if parent.reverse_0.isChecked():
				iniContents.append(f'SCALE = -{getattr(parent, f"scale_{i}").text()}\n')
			else:
				iniContents.append(f'SCALE = {getattr(parent, f"scale_{i}").text()}\n')
			iniContents.append(f'STEPGEN_MAX_VEL = {str(float(getattr(parent, f"maxVelocity_{i}").text()) * 1.2)}\n')
			iniContents.append(f'STEPGEN_MAX_ACC = {str(float(getattr(parent, f"maxAccel_{i}").text()) * 1.2)}\n')
			if parent.linearUnitsCB.currentData() == 'inches':
				iniContents.append('FERROR = 0.0002\n')
				iniContents.append('MIN_FERROR = 0.0001\n')
			else:
				iniContents.append('FERROR = 0.0051\n')
				iniContents.append('MIN_FERROR = 0.0025\n')
			iniContents.append(f'DIRSETUP = {getattr(parent, f"dirSetup_{i}").text()}\n')
			iniContents.append(f'DIRHOLD = {getattr(parent, f"dirHold_{i}").text()}\n')
			iniContents.append(f'STEPLEN = {getattr(parent, f"stepTime_{i}").text()}\n')
			iniContents.append(f'STEPSPACE = {getattr(parent, f"stepSpace_{i}").text()}\n')
			iniContents.append(f'DEADBAND = {getattr(parent, f"deadband_{i}").text()}\n')
			iniContents.append(f'P = {getattr(parent, f"p_{i}").text()}\n')
			iniContents.append(f'I = {getattr(parent, f"i_{i}").text()}\n')
			iniContents.append(f'D = {getattr(parent, f"d_{i}").text()}\n')
			iniContents.append(f'FF0 = {getattr(parent, f"ff0_{i}").text()}\n')
			iniContents.append(f'FF1 = {getattr(parent, f"ff1_{i}").text()}\n')
			iniContents.append(f'FF2 = {getattr(parent, f"ff2_{i}").text()}\n')
			iniContents.append(f'BIAS = {getattr(parent, f"bias_{i}").text()}\n')
			iniContents.append(f'MAX_OUTPUT = {getattr(parent, f"maxOutput_{i}").text()}\n')
			iniContents.append(f'MAX_ERROR = {getattr(parent, f"maxError_{i}").text()}\n')

	# build the [SPINDLE] section if enabled
	#print(parent.spindleTypeCB.currentText())
	if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()):
		iniContents.append('\n[SPINDLE]\n')
		iniContents.append(f'OUTPUT_TYPE = {parent.spindleTypeCB.currentData()}\n')
		iniContents.append(f'SCALE = {parent.spindleScale.text()}\n')
		iniContents.append(f'PWM_FREQUENCY = {parent.pwmFrequencySB.value()}\n')
		iniContents.append(f'MAX_RPM = {parent.spindleMaxRpm.text()}\n')
		iniContents.append(f'MIN_RPM = {parent.spindleMinRpm.text()}\n')
		iniContents.append(f'DEADBAND = {parent.deadband_s.text()}\n')
		iniContents.append(f'P = {parent.p_s.text()}\n')
		iniContents.append(f'I = {parent.i_s.text()}\n')
		iniContents.append(f'D = {parent.d_s.text()}\n')
		iniContents.append(f'FF0 = {parent.ff0_s.text()}\n')
		iniContents.append(f'FF1 = {parent.ff1_s.text()}\n')
		iniContents.append(f'FF2 = {parent.ff2_s.text()}\n')
		iniContents.append(f'BIAS = {parent.bias_s.text()}\n')
		iniContents.append(f'MAX_ERROR = {parent.maxError_s.text()}\n')

	iniContents.append('\n# Everything below this line is only used to\n')
	iniContents.append('# setup the Configuration Tool when loading the ini.\n')

	# build the [INPUTS] section from pushbuttons
	iniContents.append('\n[INPUT_PB]\n')
	iniContents.append('# DO NOT change the inputs text\n')
	for i in range(24):
		iniContents.append(f'INPUT_PB_{i} = {getattr(parent, f"inputPB_{i}").text()}\n')
		iniContents.append(f'INPUT_INVERT_{i} = {getattr(parent, f"inputInvertCB_{i}").isChecked()}\n')

	# build the [OUTPUTS] section from pushbuttons
	iniContents.append('\n[OUTPUT_PB]\n')
	iniContents.append('# DO NOT change the outputs text\n')
	for i in range(6):
		iniContents.append(f'OUTPUT_PB_{i} = {getattr(parent, f"outputPB_{i}").text()}\n')

	# build the [OPTIONS] section
	iniContents.append('\n[OPTIONS]\n')
	iniContents.append('# DO NOT change the options text\n')
	iniContents.append(f'INTRO_GRAPHIC = {parent.splashScreenCB.isChecked()}\n')
	iniContents.append(f'INTRO_GRAPHIC_TIME = {parent.splashScreenSB.value()}\n')
	iniContents.append(f'MANUAL_TOOL_CHANGE = {parent.manualToolChangeCB.isChecked()}\n')
	iniContents.append(f'CUSTOM_HAL = {parent.customhalCB.isChecked()}\n')
	iniContents.append(f'POST_GUI_HAL = {parent.postguiCB.isChecked()}\n')
	iniContents.append(f'SHUTDOWN_HAL = {parent.shutdownCB.isChecked()}\n')
	iniContents.append(f'HALUI = {parent.haluiCB.isChecked()}\n')
	iniContents.append(f'PYVCP = {parent.pyvcpCB.isChecked()}\n')
	iniContents.append(f'GLADEVCP = {parent.gladevcpCB.isChecked()}\n')
	iniContents.append(f'LADDER = {parent.ladderGB.isChecked()}\n')
	iniContents.append(f'BACKUP = {parent.backupCB.isChecked()}\n')

	if parent.ladderGB.isChecked(): # check for any options
		for option in parent.ladderOptionsList:
			if getattr(parent, option).value() > 0: #******** work to be done here
				iniContents.append(f'{getattr(parent, option).property("item")} = {getattr(parent, option).value()}\n')

	# build the [SSERIAL] section
	if parent.ssCardCB.currentData():
		iniContents.append('\n[SSERIAL]\n')
		iniContents.append('# DO NOT change the sserial text\n')
		iniContents.append(f'ssCardCB = {parent.ssCardCB.currentText()}\n')
	if parent.ssCardCB.currentText() == '7i64':
		# 24 ss7i64in_
		# 24 ss7i64out_
		for i in range(24):
			iniContents.append(f'ss7i64in_{i} = {getattr(parent, f"ss7i64in_{i}").text()}\n')
		for i in range(24):
			iniContents.append(f'ss7i64out_{i} = {getattr(parent, f"ss7i64out_{i}").text()}\n')

	elif parent.ssCardCB.currentText() == '7i69':
		print('here')
		# 24 ss7i69in_
		# 24 ss7i69out_
		for i in range(24):
			iniContents.append(f'SS_INPUT_{i} = {getattr(parent, f"ss7i69in_{i}").currentData()}\n')
		for i in range(24):
			iniContents.append(f'SS_OUTPUT_{i} = {getattr(parent, f"ss7i69out_{i}").currentData()}\n')

	elif parent.ssCardCB.currentText() == '7i70':
		# 48 ss7i70in_
		for i in range(48):
			iniContents.append(f'SS_INPUT_{i} = {getattr(parent, f"ss7i70in_{i}").currentData()}\n')

	elif parent.ssCardCB.currentText() == '7i71':
		# 48 ss7i71out_
		for i in range(48):
			iniContents.append(f'SS_OUTPUT_{i} = {getattr(parent, f"ss7i71out_{i}").currentData()}\n')

	elif parent.ssCardCB.currentText() == '7i72':
		# 48 ss7i72out_
		for i in range(48):
			iniContents.append(f'SS_OUTPUT_{i} = {getattr(parent, f"ss7i72out_{i}").currentData()}\n')

	elif parent.ssCardCB.currentText() == '7i73':
		# 16 ss7i73key_
		# 12 ss7i73lcd_
		# 16 ss7i73in_
		# 2 ss7i73out_
		for i in range(16):
			iniContents.append(f'SS_KEY_{i} = {getattr(parent, f"ss7i73key_{i}").currentData()}\n')
		for i in range(12):
			iniContents.append(f'SS_LCD_{i} = {getattr(parent, f"ss7i73lcd_{i}").currentData()}\n')
		for i in range(16):
			iniContents.append(f'SS_INPUT_{i} = {getattr(parent, f"ss7i73in_{i}").currentData()}\n')
		for i in range(2):
			iniContents.append(f'SS_OUTPUT_{i} = {getattr(parent, f"ss7i73out_{i}").currentData()}\n')

	elif parent.ssCardCB.currentText() == '7i84':
		# 32 ss7i84in_
		# 16 ss7i84out_
		for i in range(32):
			iniContents.append(f'SS_INPUT_{i} = {getattr(parent, f"ss7i84in_{i}").currentData()}\n')
		for i in range(16):
			iniContents.append(f'SS_OUTPUT_{i} = {getattr(parent, f"ss7i84out_{i}").currentData()}\n')

	elif parent.ssCardCB.currentText() == '7i87':
		# 8 ss7i87in_
		for i in range(8):
			iniContents.append(f'SS_INPUT_{i} = {getattr(parent, f"ss7i87in_{i}").currentData()}\n')

	try:
		with open(iniFilePath, 'w') as iniFile:
			iniFile.writelines(iniContents)
	except OSError:
		parent.outputPTE.appendPlainText(f'OS error\n {traceback.print_exc()}')
