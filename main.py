#!/usr/bin/env python

# Missing functionality:
# 1. Fixing laps
# 2. finding and showing splits
# 3. Adjusting display to splits 

import Operations.DefineTrack
import Operations.DefineCar
import Operations.ExtractLaps
import Operations.FindSplits
import Operations.FindGearing
import Operations.DisplayLaps

from Shared import Objects

import argparse
import os

operations = { 'ExtractLaps': Operations.ExtractLaps,  
			   'FindSplits' : Operations.FindSplits, 
			   'DisplayLaps': Operations.DisplayLaps,
			   'FindGearing': Operations.FindGearing, 
			   'DefineTrack': Operations.DefineTrack, 
			   'DefineCar'  : Operations.DefineCar}

parser = argparse.ArgumentParser(description='Process and display track logs')
parser.add_argument('-op', choices=operations, required=True, help='operation to run', dest='operation')

args = parser.parse_known_args()[0]

print args.operation

dir = os.path.dirname(os.path.realpath(__file__))
Objects.setWorkingDirectory(dir)

op = operations[args.operation].run();
