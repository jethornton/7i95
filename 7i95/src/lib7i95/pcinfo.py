from lib7i95 import extcmd

"""
Usage extcmd.job(self, cmd="something", args="",
dest=self.QPlainTextEdit, clean="file to delete when done")

To pipe the output of cmd1 to cmd2 use the following
Usage extcmd.pipe_job(self, cmd1="something", arg1="", cmd2="pipe to",
arg2, "", dest=self.QPlainTextEdit)
"""

extcmd = extcmd.extcmd()

def cpuInfo(parent):
	extcmd.job(cmd="lscpu", args=None, dest=parent.infoPTE)

def nicInfo(parent):
	extcmd.job(cmd="lspci", args=None, dest=parent.infoPTE)

def nicCalc(parent):
	if parent.tMaxLE.text() != '' and parent.cpuSpeedLE.text() != '':
		tMax = int(int(parent.tMaxLE.text()) / 1000)
		cpuSpeed = float(parent.cpuSpeedLE.text()) * parent.cpuSpeedCB.currentData()
		packetTime = tMax / cpuSpeed
		parent.packetTimeLB.setText(f'{packetTime:.1%}')
		threshold = (cpuSpeed * 0.7) / cpuSpeed
		parent.thresholdLB.setText(f'{threshold:.0%}')
	else:
		errorText = []
		if parent.cpuSpeedLE.text() == '':
			errorText.append('CPU Speed can not be empty')
		if parent.tMaxLE.text() == '':
			errorText.append('tMax can not be empty')
		parent.errorMsgOk('\n'.join(errorText))

def readTmax(parent):
	extcmd.job(cmd="halcmd", args=['show', 'param', 'hm2*.tmax'], dest=parent.tmaxPTE)
