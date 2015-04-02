import os
from numpy import linalg as LA
import numpy as np

def get_gesture_readings (gestures, dataset_source):

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
				readings = get_file_readings(file_name, dataset_source)

				# Append this gesture file readings to the whole gesture's readings (file / gesture)
				gesture_acc_readings.append(readings['acc'])
				gesture_gyro_readings.append(readings['gyro'])

		# Append whole gestures readings (gesture)
		gestures['acc_readings'].append(gesture_acc_readings)
		gestures['gyro_readings'].append(gesture_gyro_readings)
	return gestures

def get_file_readings(file_name, dataset_source):
	
	with open(file_name, 'r') as handler:
		readings= {'acc': [], 'gyro': []}
		if dataset_source == "MoGeRe":
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
				readings['acc'].append(line[2:5])
				readings['gyro'].append(line[5:])
		return readings

"""
 Removes readings that have a norm < idle threshold
 Removes readings that have a previous reading < dupl_thresh
"""

def filter_idle_and_dupl(readings, idle_thresh, dupl_thresh):
	for gesture in readings:
		for g_file in gesture:
			prev_reading = []
			for reading in g_file:
				# :TODO: test this threshold
				# reading = [reading_x, reading_y, reading_z]
				if 	(abs(reading[0]) < idle_thresh and 
					abs(reading[1] < idle_thresh) and 
					abs(reading[2]) < idle_thresh) :
					g_file.remove (reading)

				# :TODO: test this threshold
				if prev_reading and LA.norm(np.array(reading) - np.array(prev_reading)) < dupl_thresh:
					g_file.remove (reading)
				prev_reading = reading

	# :TODO: print some statistics about which readings are removed
	return readings

def count_readings (list):
	return sum(1 for row in list
      for i in row 
      for j in i if j)