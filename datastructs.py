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

# Create a DataFrame of Day - Total Wastage
def createWastageByDayDict(w_dict, machines):
	days = list(w_dict.keys())
	output = []
	# Iterate over each day
	for day in days:
		day_total = 0
		# Sum up the total across all machines for that day
		for machine in machines:
			day_total += sum(w_dict[day][machine])
		day_total = round(day_total, 2)
		output.append([day, day_total])
	output_df = lp.createDataFrame(output, ['Date', 'Total-Wastage-kg'], 'Date')

	return output_df

# Create a Data Frame from the wastage file
def createDfWastageFile(source, filename):
	logging.info('Processing file ' + filename)
	df = lp.putCSVToDf(source, filename)
	df.fillna(0, inplace=True)
	return df

# Create a master date-machine-wastage dictionary for all further use
def createDateMachineDict(df, days, machines):
	# Iterating over each day
	day_dict = {}
	for day in days:
		# Getting the rows for that day
		rows = df.loc[df['Date']==day]
		# Extracting columns for each machine for that day
		machine_dict = {}
		for machine in machines:
			m_rows = rows.loc[:, machine]
			# Converting to list for ease
			m_list = list(m_rows)
			machine_dict[machine] = m_list

		day_dict[day] = machine_dict
	return day_dict