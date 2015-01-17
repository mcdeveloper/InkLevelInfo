import sys
import datetime
import subprocess

class HpInkLevel:
	def setColor(self, color):
		self.color = color

	def setPartNo(self, partNo):
		self.partNo = partNo

	def setLevel(self, level):
		self.level = level

	def isComplete(self):
		return hasattr(self, 'color') and hasattr(self, 'partNo') and hasattr(self, 'level')

	def __str__(self):
		return 'Color: %s; Sku: %s; Level: %s' % (self.color, self.partNo, self.level)

class HpInfo:
	def __init__(self, printerName, hpInkLevelArray):
		self.name = printerName
		self.inkLevels = hpInkLevelArray

	def getName(self):
		return self.name

	def getInkLevels(self):
		return self.inkLevels

	def __str__(self):
		inkResult = ''
		for i in self.inkLevels:
			inkResult = inkResult + ('\t%s\n' % str(i))

		return 'Printer: %s\nInk/toner levels:\n%s' % (self.name, inkResult)
	
class HpLevelInfoJSONserializer:
	@staticmethod
	def serialize(hpInfo):
		date = datetime.datetime.now().replace(microsecond=0).isoformat()
		l1 = '{\n\t"printer": "%s",\n\t"timestamp": "%s",\n\t"inkLevels": [' % (hpInfo.getName(),date)
		l2 = ''
		l3 = '\n\t]\n}'
		for i in hpInfo.getInkLevels():
			if (len(l2) != 0):
				l2 = l2 + ','

			l2 = l2 + '\n\t\t{"color": "%s", "sku": "%s", "level": "%s"}' % (i.color, i.partNo, i.level)

		return l1 + l2 + l3

class HpInfoParser:
	@staticmethod
	def parseAgent(inputLine):
		agentString = 'agent'
		asp = inputLine.find(agentString)
		asl = len(agentString)
		
		if (asl+asp+2 >= len(inputLine)):
			return False

		if (asp == -1 or inputLine[asl+asp+1] != '-' or not inputLine[asl+asp].isdigit()):
			return False

		blankAfterParamName = inputLine.find(' ', asl+asp+2)			
		if (blankAfterParamName == -1):
			return False

		agentNo    = int(inputLine[asl+asp])
		paramName  = inputLine[asl+asp+2:blankAfterParamName]
		paramValue = inputLine[blankAfterParamName:].strip()

		return {'agentNo': agentNo, 'name': paramName, 'value': paramValue}

	@staticmethod
	def handleAgent(agentArray, agi, hpInk):
		if (agi != agentArray['agentNo']):
			hpInk = HpInkLevel()

		name  = agentArray['name']
		value = agentArray['value']
		if (name == 'desc'):
			vSpacePos = value.find(' ')

			if (vSpacePos != -1):
				hpInk.setColor(value[:vSpacePos])
			else:
				hpInk.setColor(value)
		elif (name == 'level'):
			hpInk.setLevel(value)
		elif (name == 'sku'):
			hpInk.setPartNo(value)

		return hpInk

	@staticmethod
	def parse(hpOutput):
		name = ''
		inkLevels = []

		currentAgentIndex = -1
		currentHpInk = HpInkLevel()

		for i in hpOutput:
			ap = HpInfoParser.parseAgent(i)
			if (ap != False):
				currentHpInk = HpInfoParser.handleAgent(ap, currentAgentIndex, currentHpInk)
				currentAgentIndex = ap['agentNo']
			else:
				model = i.find('model-ui')
				if (model != -1):
					name = i[model+8:].strip()
			
			if (currentHpInk.isComplete()):
				inkLevels.append(currentHpInk)
				currentHpInk = HpInkLevel()

		return HpInfo(printerName = name, hpInkLevelArray = inkLevels)
	
def invoke(checkForSysArgv):
	raw = ''

	try:
		if (checkForSysArgv):
			if (len(sys.argv) >= 3):
				raw = subprocess.check_output([sys.argv[1], sys.argv[2]])

		if (len(raw) == 0):
			raw = subprocess.check_output(["hp-info", ""])
	except OSError, oe:
		return '{"error": "Internal error. No hplip?"}'

	hpInfo = HpInfoParser.parse(raw.split('\n'))
	
	return HpLevelInfoJSONserializer.serialize(hpInfo) 
	
if __name__ == "__main__":
	print 'Running in direct command mode!'
	print '  - if run without arguments then hp-info will be queried directly for data'
	print '  - however for testing purposes you can pass 2 arguments: first is application'
	print '    that will be run and second is an argument for that app (e.g. cat fake-data.txt)'
	print '             '
	print 'Output:'
	print invoke(True)
