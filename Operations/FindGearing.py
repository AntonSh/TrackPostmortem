#DefineStart
import json
import argparse
import sys
import collections
from collections import Counter
from Shared.Objects import Channels
from Shared import seriesReader

parser = argparse.ArgumentParser(description='Find gear ratios')
parser.add_argument('-input', help='input log file')

def setWorkingDir(dir):
	return

def run():
	args = parser.parse_known_args()[0]
	lapFileName = args.input
	lapData = seriesReader.loadSeriesFromFile(lapFileName)

	speed = lapData[Channels.GPSSpeedMPH]
	rpm   = lapData[Channels.EngineRpm]

	gearRatios = Counter([round(speed[i] / (rpm[i] + 0.001), 3) for i in range(len(speed))])

	print sorted(gearRatios.most_common(8), key=lambda ratio: ratio[0])
