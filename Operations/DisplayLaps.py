import numpy as np
import matplotlib.pyplot as plt
import sys
import collections
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from matplotlib.collections import PatchCollection
import json
import argparse
from Shared.Objects import Channels
from Shared.Objects import PlotConstants
from Shared import Objects
from Shared import seriesReader


parser = argparse.ArgumentParser(description='Run lap comparison')
parser.add_argument('-car', help='car name')
parser.add_argument('-track', help='track name')
parser.add_argument('-laps', nargs="*", help='lap files')
parser.add_argument('-channels', nargs="*", help='channels to compare')

def run():
	args = parser.parse_known_args()[0]

	car = Objects.loadCar(args.car)
	track = Objects.loadTrack(args.track)
	lapFiles = args.laps
	channels = args.channels

	laps = []
	for lapFile in lapFiles:
		laps.append(Objects.loadLap(lapFile))

	displayLaps(car, track, laps, channels)


def displayLaps(car, track, laps, channels):
	progress = Channels.Progress
	GxChannel = Channels.AccX
	GyChannel = Channels.AccY
	
	varPlots = len(channels)
	
	baseGrid = gridspec.GridSpec(1, 2)
	baseGrid.update(left=0.05, right=0.99, top=0.99, bottom=0.05, wspace=0.1, hspace=0.01)

	graphGrid = gridspec.GridSpecFromSubplotSpec(varPlots, 1, subplot_spec=baseGrid[0], hspace=0.05)

	mapGGrid = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=baseGrid[1], hspace=0.1)

	mapPlot = plt.subplot(mapGGrid[0])
	plt.xlabel("TrackMap")
	mapPlot.imshow(track.loadImage(), extent = track.getImagePosition())
	mapPlot.grid()
	mapPlot.axis('equal')

	gPlot = plt.subplot(mapGGrid[1])
	plt.xlabel("G plot")
	gPlot.grid()
	gPlot.axis('equal')

	gGridMarks = 4
	maxG = 0.999
	gGrid = []
	for step in range(1, gGridMarks + 1):
		gGrid.append(mpatches.Circle([0, 0], maxG * step / gGridMarks))

	collection = PatchCollection(gGrid, cmap=plt.cm.hsv, alpha=1.0/gGridMarks)
	gPlot.add_collection(collection)

	graphPlots = {}
	for i in range(varPlots):
		channelName = channels[i]
		ax = plt.subplot(graphGrid[i])
		plt.ylabel(channelName)
		ax.grid()
		graphPlots[channelName] = ax

	# draw splits
	splits = list(track.splits) + [track.startFinish]
	for split in splits:
		plotSplit = toPlotLine(split)
		mapPlot.plot(plotSplit[0],plotSplit[1] , 'bo-')

	i = 0
	for lap in laps:

		for channel in channels:
			channelPlot = graphPlots[channel] 
			print channel
			channelPlot.plot(lap.channels[progress], lap.channels[channel])
		
		# Draw G(x) G(y) Plot
		gPlot.plot(lap.channels[GxChannel],lap.channels[GyChannel], '.')
		
		# Draw Track map
		mapPlot.plot(lap.channels[Channels.Longitude], lap.channels[Channels.Latitude])

		# Print lap time
		lapTime = lap.channels[Channels.DeviceTime][-1] - lap.channels[Channels.DeviceTime][0]
		mapPlot.text(track.textPosition[1], track.textPosition[0] - 0.00001 * i * PlotConstants.TextSize, '{0} - {1} - {2}'.format(i + 1, lap.name,  lapTime), fontdict = PlotConstants().getFont(i))

		i += 1

	figManager = plt.get_current_fig_manager()
	figManager.set_window_title("Track comparison")	
	plt.show()

def toPlotLine(line):
	result = [[line[0][1], line[1][1]], [line[0][0], line[1][0]]]
	return result
