import os
from numpy import linalg as LA
import numpy as np
from settings import settings
import copy
def get_gesture_readings (gestures):

	for gesture in gestures['g_dir']: 
		gesture_acc_readings = []
		gesture_gyro_readings = []
		# Walk through all files in a gesture directory
		for root,_, files in os.walk(gestures['root']+gesture, topdown=False):
			
			# Count the number of files per gesture directory
			gestures['file_count'].append(len(files))
			file_acc_readings = []
			file_gyro_readings = []

			for name in files :
				file_name = os.path.join(root, name)
				readings = get_file_readings(file_name)

				# Append this gesture file readings to the whole gesture's readings (file / gesture)
				gesture_acc_readings.append(readings['acc'])
				gesture_gyro_readings.append(readings['gyro'])

		# Append whole gestures readings (gesture)
		gestures['acc_readings'].append(gesture_acc_readings)
		gestures['gyro_readings'].append(gesture_gyro_readings)
	return gestures

def get_file_readings(file_name):
	
	with open(file_name, 'r') as handler:
		readings= {'acc': [], 'gyro': []}
		if settings['dataset_source'] == "MoGeRe":
			# skip first line 
			handler.readline()
			while True:
				# lines: t --> epoch time in ms, tRel --> relative time in s, acc_x, acc_y, acc_z, gy_x, gy_y, gy_z
				line = handler.readline()
				if line == "": 
					break
				line = line.rstrip().split(',')

				# :TODO: check that file is read correctly
				line = map(float, line)
				readings['acc'].append([line[2], line[3], line[4]+1]) # remove the -1 effect
				readings['gyro'].append(line[5:])
		return readings

"""
 Removes readings that have a norm < idle threshold
 Removes readings that have a previous reading < dupl_thresh
"""
def filter_idle(readings):
	for gesture in readings:
		for g_file in gesture:
			for reading in g_file:
				# :TODO: test this threshold
				# reading = [reading_x, reading_y, reading_z]
				if 	(abs(reading[0]) < settings['idle_thresh']):
					reading[0] = 0.0
				if (abs(reading[1]) < settings['idle_thresh']):
					reading[1] = 0.0
				if (abs(reading[2]) < settings['idle_thresh']) :
					reading[2] = 0.0
	return readings

"""
 Removes readings that have a norm < idle threshold over a window of size size
"""
def filter_idle_over_window(readings):
	size = settings['window_size']
	overlap = settings['overlap']

	new_readings = copy.deepcopy(readings)
	for gesture in new_readings:
		for g_file in gesture:
			x_ = [abs(reading[0]) for reading in g_file ]
			y_ = [abs(reading[1]) for reading in g_file ]
			z_ = [abs(reading[2]) for reading in g_file ]
			# x_all_avg = (sum(x_)/len(x_)) * 1.0
			# y_all_avg = (sum(y_)/len(y_)) * 1.0
			# z_all_avg = (sum(z_)/len(z_)) * 1.0
			flag = 0
			for window_start in xrange(0,len(g_file), int (size*overlap)):
  				# get average of the window 
  				x_avg = (sum(x_[window_start: window_start+size])/size) * 1.0
  				y_avg = (sum(y_[window_start: window_start+size])/size) * 1.0
  				z_avg = (sum(z_[window_start: window_start+size])/size) * 1.0
  				if 	(x_avg < settings['idle_thresh'] and 
  					y_avg < settings['idle_thresh'] and
  					z_avg < settings['idle_thresh']):
  				# if 	(x_avg < x_all_avg and 
  				# 	y_avg < y_all_avg and
  				# 	z_avg < z_all_avg):
  					for i in g_file[window_start : window_start + int(size*overlap)] :
  						g_file.remove(i)
  					flag = 1
  				
  				# if flag == 1: 
  				# 	break

	return new_readings

def filter_idle_and_dupl(readings):
	for gesture in readings:
		for g_file in gesture:
			prev_reading = []
			for reading in g_file:
				# :TODO: test this threshold
				# reading = [reading_x, reading_y, reading_z]
				if 	(abs(reading[0]) < settings['idle_thresh'] and 
					abs(reading[1] < settings['idle_thresh']) and 
					abs(reading[2]) < settings['idle_thresh']) :
					g_file.remove (reading)

				# :TODO: test this threshold
				if (prev_reading and 
					LA.norm(np.array(reading) - np.array(prev_reading)) < settings['dupl_thresh']):
					g_file.remove (reading)
				prev_reading = reading

	#readings = runningAverage(readings)		
	#print readings	
	# :TODO: print some statistics about which readings are removed
	return readings

def runningAverage(readings):
	# Smoothed readings
	final_readings=[]
	for gesture in readings:
		gesture_r = []
		for g_file in gesture:
			g_file_r = []
			for i in range (0, len(g_file) - settings['window_size'], settings['step_size']):
				reading = [0,0,0]
				print str(i) + " i"
				for j in range (0, settings['window_size']):
					reading = [sum(x) for x in zip(reading, g_file[i+j])]
				reading = [ x*1.0 / settings['window_size'] for x in reading]
				print reading
				g_file_r.append(reading)
			gesture_r.append(g_file_r)
		final_readings.append(gesture_r)		
	return final_readings
def count_readings (list):
	return sum(1 for row in list
      for i in row 
      for j in i if j)