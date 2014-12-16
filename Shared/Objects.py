import json
import collections
from Shared import seriesReader

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

##################################################
workingDir = ""
carSubdir  = "Data/Cars"
lapsSubdir = "Data/Laps"
trackSubdir= "Data/Tracks"

def setWorkingDirectory(directory):
		global workingDir
		workingDir = directory

def getTrackDirectory():
	return "{}/{}".format(workingDir, trackSubdir)

def getLapDirectory():
	return "{}/{}".format(workingDir, lapsSubdir)

def getCarDirectory():
	return "{}/{}".format(workingDir, carSubdir)


###############################################
def getCarFileName(carName):
	return "{}/{}.json".format(getCarDirectory(), carName)

def loadCar(carName):
	with open(getCarFileName(carName), 'r') as infile:
		value = json.loads(infile.read())
		return Car(value["name"], value["gears"])

class Car:
	name  = ""
	gears = []
	
	def __init__(self, name, gears):
		self.name = name
		self.gears = gears

	def saveCar(self):
		fileName = getCarName(self.name)
		with open(fileName, 'w') as outfile:
			outfile.write(json.dumps(self.__dict__))

################################################
def getTrackFileName(trackName):
	return "{}/{}.json".format(getTrackDirectory(), trackName)

def getTrackImageFileName(image):
	return "{}/{}".format(getTrackDirectory(), image)

def loadTrack(trackName):
	with open(getTrackFileName(trackName), 'r') as infile:
		value = json.loads(infile.read())
		result = Track(value["name"], value["startFinish"], value["splits"])
		result.imageName = value["imageName"]
		result.imagePosition = value["imagePosition"]
		result.textPosition = value["textPosition"]
		return result

class Track:
	name = ""
	startFinish = []
	splits = []
	imageName = None
	imagePosition = None
	textPosition = None

	def __init__(self, name, startFinish, splits):
		self.name = name
		self.startFinish = startFinish
		self.splits = splits

	def save(self):
		fileName = getTrackFileName(self.name)
		with open(fileName, 'w') as outfile:
			outfile.write(json.dumps(self.__dict__))
	
	def getImagePosition(self):
		result = []
		result= [self.imagePosition[0][1], self.imagePosition[1][1], self.imagePosition[0][0], self.imagePosition[1][0]]
		return result

	def loadImage(self):
		imageFile = getTrackImageFileName(self.imageName)
		img = mpimg.imread(imageFile)
		return img



##################################################
def getLapFileName(lapName):
	return "{}/{}.csv".format(getLapDirectory(), lapName)

def loadLap(lapName):
	result = Lap({})
	fileName = getLapFileName(lapName)
	result.channels = seriesReader.loadSeriesFromFile(fileName)
	result.name = lapName

	return result

class Lap:
	name = ""
	channels = {}

	def __init__(self, channelNames):
		self.channels = collections.OrderedDict()

		for name in channelNames:
			self.channels[name] = []

	def save(self):
		fileName = getLapFileName(self.name)
 		seriesReader.saveToFile(self.channels, fileName)

		print fileName

##################################################
class PlotConstants:
	TextSize = 10

	Colors = ['r', 
		  'b', 
		  'g', 
		  'y']

	def getFont(self, index):
		font = {'family' : 'serif',
			'color'  : self.Colors[index],
			'weight' : 'normal',
			'size'   : self.TextSize,
			}		

		return font


##################################################
class Channels:

	Progress = 'Track Progress'
	AdjustedProgress = 'Adjusted Track Progress'


	DeviceTime    = "Device Time"
	Longitude     = "Longitude"
	Latitude      = "Latitude"

	GPSTime 	  = "GPS Time"
	GPSSpeedMS    = "GPS Speed (Meters/second)"
	GPSDOP        = "Horizontal Dilution of Precision"
	GPSSpeedMPH   = "Speed (GPS)(mph)"
	GPSAccuracyM  = "GPS Accuracy(m)"
	GPSSatellites = "GPS Satellites"

	GPSAltitude   = "Altitude"
	GPSBearing    = "Bearing"
	Gx 		      = "G(x)"
	Gy		      = "G(y)"
	Gz		      = "G(z)"
	GCalibrated   = "G(calibrated)"
	AccX          = "Acceleration Sensor(X axis)(g)"
	AccY          = "Acceleration Sensor(Y axis)(g)"
	AccZ          = "Acceleration Sensor(Z axis)(g)"
	AccelPedal    = "Accelerator PedalPosition D(%)"
	EngineLoad    = "Engine Load(%)"
	EngineTemp    = "Engine Coolant Temperature(C)"
	EngineRpm     = "Engine RPM(rpm)"
	AmbientTemp   = "Ambient air temp(C)"