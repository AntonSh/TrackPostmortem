import csv
import datetime
import collections

##### Magic numbers############
dateConversion = { 'GPS Time':'%a %b %d %H:%M:%S %Z %Y',
					'Device Time':'%d-%b-%Y %H:%M:%S.%f'}
###############################

debug = True

def saveToFile(lapSeries, fileName):
	if debug:
		print ('saving lap to file {}'.format(fileName))

	with open(fileName, 'wb') as csvfile:
		wt = csv.writer(csvfile, delimiter = ',')
		header = lapSeries.keys()
		wt.writerow(header)

		if debug :
			print ('lap length', len(lapSeries[header[0]]))

		for i in range(0, len(lapSeries[header[0]])):
			row = []
			for channel in header:
				# print (channel, i)
				value = lapSeries[channel][i]
				if channel in dateConversion.keys():
					format = dateConversion[channel]
					value = datetime.datetime.strftime(value, format)

				row.append(value)

			wt.writerow(row)
	if debug:
		print 'done writing file'

def loadSeriesFromFile(inputFileName):

	if debug:
		print ('Loading series from file', inputFileName)

	series = collections.OrderedDict()

	totalRows = 0

	with open(inputFileName, 'rb') as csvfile:
		rd = csv.reader(csvfile, delimiter = ',', skipinitialspace = True)
		attributeNames = rd.next();
		for name in attributeNames:
			series[name] = []

		for row in rd:
			totalRows+=1
			for i in range(0,len(series)):
				name = series.keys()[i]
				
				## sometimes header repeated in the middle of file
				if row[i] == name:
					break

				value = row[i]

				if name in dateConversion.keys():
					if value == '-':
						value = datetime.time() 
					else:
						format = dateConversion[name]
						value = datetime.datetime.strptime(value, format)
				else:
					if value == '-':
						value = 0
					value = float(value)
					
				series[name].append(value)

	if debug:
		print ('Done loading track')
		print '{0}: {1}; {2}: {3}'.format('Total channelss', len(series), 'Total data points', len(series[series.keys()[0]]))

	return series