import numpy as np
import matplotlib.pyplot as plt
import sys
import collections
from Shared import seriesReader
from Shared.Objects import *
import sys
import argparse
import datetime

parser = argparse.ArgumentParser(description='Creates laps objects for given track session')
parser.add_argument('-input', required=True, help='track log')
parser.add_argument('-track', required=True, help='track name')

def run():

	args = parser.parse_known_args()[0]

	trackName = args.track
	inputFile = args.input

	track = loadTrack(trackName)
	sessionData = seriesReader.loadSeriesFromFile(inputFile)

	laps = extractLaps(sessionData, track)

 	for lap in laps:
 		lap.save()	

def extractLaps(series, track):
	lapNumber = -1
	allLaps = []
	channelNames = series.keys()
	lap = None

	totalSamples = len(series[Channels.Latitude])
	for i in range(0, totalSamples-1):

		if lap == None:
			lap = Lap(channelNames + [Channels.Progress, Channels.AdjustedProgress])
			lapNumber += 1

		for key in channelNames:
			lap.channels[key].append(series[key][i])

		# check if we are at the end of the lap
		lineToNextPosition = [(series[Channels.Latitude][i], series[Channels.Longitude][i]), 
							  (series[Channels.Latitude][i+1], series[Channels.Longitude][i+1])]

		if linesIntersect(track.startFinish, lineToNextPosition) or i == (totalSamples - 2):

			# Copy next value to make sure the lap is comlete
			for key in channelNames:
				lap.channels[key].append(series[key][i+1])

			lapSamples = len(lap.channels[Channels.Latitude])
			progressChannel = [1.0*x/(lapSamples) for x in range(0, lapSamples)]
			lap.channels[Channels.Progress] = list(progressChannel)
			lap.channels[Channels.AdjustedProgress] = list(progressChannel)

			del lap.channels[Channels.GPSTime]

			timeChannel = lap.channels[Channels.DeviceTime]
	 		startTime = datetime.datetime.strftime(timeChannel[0], '%Y-%m-%d-%H-%M-%S')

			lap.name = "{}[{}]".format(track.name, startTime)

			allLaps.append(lap)
			lap = None
	
	return allLaps 

def linesIntersect(line1, line2):
	x = 0
	y = 1
	s1 = (line1[1][x]-line1[0][x], line1[1][y]-line1[0][y])
	s2 = (line2[1][x]-line2[0][x], line2[1][y]-line2[0][y])

	den = (-s2[x]*s1[y] + s1[x]*s2[y])
	if den != 0:
		s = (-s1[y]*(line1[0][x]-line2[0][x]) + s1[x] * (line1[0][y] - line2[0][y])) / den
		t = ( s2[x]*(line1[0][y]-line2[0][y]) - s2[y] * (line1[0][x] - line2[0][x])) / den

		if s >= 0 and s <= 1 and t >= 0 and t <= 1 :
			return True

	return False