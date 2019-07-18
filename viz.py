#!/bin/python

# Generic imports
import os
import sys
import logging
import statistics
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Path to library file
LIBRARY_FILE = '../libraries.py'

# Load library file and import
sys.path.append(os.path.dirname(os.path.expanduser(LIBRARY_FILE)))
import libraries as lp

# Total Machine wastage plot
def createTotalWastageChart(tw_dict,plt, des, filename):
	f_name = filename + '-total-per-machine.png'
	machines = list(tw_dict.keys())
	total_wastage_machine = [tw_dict[machine] for machine in machines]
	machine_no = [machine.lower().split('machine-')[1].replace(" ", "") for machine in machines]
	lp.saveDonutChart(total_wastage_machine, machine_no, plt, des, f_name)

# Average Machine wastage plot
def createAvgWastageChart(av_dict,plt, des, filename):
	f_name = filename + '-avg-per-machine.png'
	machines = list(av_dict.keys())
	avg_wastage_machine = [av_dict[machine] for machine in machines]
	machine_no = [machine.lower().split('machine-')[1].replace(" ", "") for machine in machines]	
	lp.saveDonutChart(avg_wastage_machine, machine_no, plt, des, f_name)	

# Create a line graph for total wastage by day
def lineGraphWastageByDay(df, des, filename):
	# Create lists for x and y axis - days, total wastage
	days = df.index.values.tolist()
	days = [day.split('/')[0] + '/' + day.split('/')[1] for day in days]
	totals = list(df.loc[:, 'Total-Wastage-kg'])
	# Generate plot
	plt.plot(days, totals)
	plt.gcf().set_size_inches(8, 6)
	f_name = filename  + '-by-day.png'
	lp.saveLineGraph(plt,'','','',des,f_name)

# Multiline graph for different machines across days
def lineGraphWastagePerMachinePerDay(days,mw_dict,plt,des,filename):
	# Get date without the year field
	d_short = [day.split('/')[0] + '/' + day.split('/')[1] for day in days]
	# Get list of machines
	machines = list(mw_dict.keys())
	# Get unique color list for each line graph
	colors = lp.getUniqueColors(len(machines))
	i = 0

	# Plot line for each machine
	for machine in machines:
		plt.plot(d_short, mw_dict[machine], label = str(machine), color=colors[i])
		i = i+1
	
	#plt.gcf().set_size_inches(8, 6)
	f_name = filename + '-by-machine.png'
	lp.saveLineGraph(plt,'','','',des,f_name)

# Generate data structures and create all charts
def createCharts(w_dict, machines, des, filename):
	days = list(w_dict.keys())
	
	# Dicts for -
	# Mean wastage per machine across all days
	# Total wastage per machine across all days
	tw_dict = {}
	av_dict = {}
	
	# Dict for Wastage for a machine by each day
	machine_wastage_by_day = {}

	# Create each line plot for each machine
	for machine in machines:
		m_total = []
		# Sum up wastages across all days for a machine
		for day in days:
			m_total.append(round(sum(w_dict[day][machine]), 2))
			
		# Wastage for a machine
		machine_wastage_by_day[machine] = m_total
		# Average machine wastage
		a_sum = round(statistics.mean(m_total),2)
		# Ignore small values for donut chart
		if a_sum>0:
			av_dict[machine] = a_sum
		# Total Machine wastage
		t_sum = round(sum(m_total),2)
		if t_sum>0:
			tw_dict[machine] = t_sum

	# Line graph for all machines across all days
	lineGraphWastagePerMachinePerDay(days,machine_wastage_by_day,plt,des,filename)
	
	# Average and total wastage charts
	createTotalWastageChart(tw_dict,plt,des,filename)
	createAvgWastageChart(av_dict,plt,des,filename)
