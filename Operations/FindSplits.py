import json
import argparse
from Shared import Objects 

parser = argparse.ArgumentParser(description='Define car ')
parser.add_argument('-lapFile', help='lap file name')
parser.add_argument('-nSplits', help='number of split points to find')


def run():
	# load lap
	# 
	args = parser.parse_known_args()[0]

	lapFile = args.lapFile
	lap = loadLap(lapFile)

	print NotImplemented


def findSplits(lap):
	print NotImplemented
