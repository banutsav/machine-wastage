#!/bin/python

# Generic imports
import os
import sys
import logging
import pandas as pd

# Path to library file
LIBRARY_FILE = '../libraries.py'

# Load library file and import
sys.path.append(os.path.dirname(os.path.expanduser(LIBRARY_FILE)))
import libraries as lp

# Helper module imports
import viz as vz
import datastructs as ds

# Create CSV file for wastage by day
def createWastageByDayCSV(w_dict, machines, des, filename):
	# Construct filename for output
	waste_per_day_file = filename + '-by-day.csv'
	# Create output dataframe and write to CSV
	output_df = ds.createWastageByDayDict(w_dict, machines)
	lp.writeDfToCSV(output_df, des, waste_per_day_file)
	# Create line graph
	vz.lineGraphWastageByDay(output_df, des, filename)

# Iterate over each individual csv file
def createVizualisationFiles(source, destination):

	for filename in os.listdir(source):
		if not filename.endswith('.csv'):
			continue
		try:
			# Create data frame
			df = ds.createDfWastageFile(source, filename)
			# Get start and end columns over which summation takes place
			machine_cols = [col for col in df.columns if 'machine' in col.lower()]
			# Get the list of Unique Days	
			days = df['Date'].unique()
			# Create Master data dictionary
			day_dict = ds.createDateMachineDict(df, days, machine_cols)
			# Generate Vizualisations and Reports
			fname = filename.split('.')[0]
			vz.createCharts(day_dict, machine_cols, destination, fname)
			createWastageByDayCSV(day_dict, machine_cols, destination, fname)

		except:
			print('[ERROR] There was an issue with file ' + filename + ', it will be skipped over')
			logging.exception('There was an issue with file ' + filename + ', it will be skipped over')

	logging.info('Iterations over the source folder have been completed...')

if __name__ == '__main__':

	# Start logging and begin execution
	lp.setLogging()

	try:
		print('Execution started...')
		source = lp.getDataSource()
		des = lp.getDataDestinantion()
		createVizualisationFiles(source, des)
	except:
		print('[ERROR] There was a problem in the execution...')
		logging.exception('There was a problem in the execution...')
	finally:
		print('Completed...')