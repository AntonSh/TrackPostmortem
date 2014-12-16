#DefineStart
import json
import argparse
from Shared.Objects import Car

carProfile = "{}/{}.json"

parser = argparse.ArgumentParser(description='Define car ')
parser.add_argument('-car', help='car name')
parser.add_argument('-gears', nargs=6, help='ratio of RPM to speed(mph)')

def run():
	args = parser.parse_known_args()[0]

	car = Car(args.car, args.gears) 
	with open(carProfile.format(workingDirectory, car.name), 'w') as outfile:
  		outfile.write(car.toJSON())
