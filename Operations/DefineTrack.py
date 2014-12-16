#DefineStart
import json
import argparse
from Shared.Objects import Track

parser = argparse.ArgumentParser(description='Define coordinates for start-finish line')
parser.add_argument('-track', required=True, help='track name')
parser.add_argument('-lat', nargs=2, required=True, help='latitudes of start and finish point')
parser.add_argument('-long',nargs=2, required=True, help='longitudes of start and finish point')

def run():
	args = parser.parse_known_args()[0]

	startFinish = []
	for i in [0,1]:
		startFinish.append((args.lat[i], args.long[i]))

	track = Track(args.track, startFinish, [])
	track.save()