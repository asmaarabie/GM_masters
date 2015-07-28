import os
from numpy import linalg as LA
import numpy as np
from settings import settings
import copy
def get_gesture_readings (gestures):
	# Get bias values
	bias_ret = bias()
	if settings['logging']:
		print "bias is:" + str(bias_ret)
		if settings['remove_bias']:
			print 'remove bias'
		else: 
			print " don't remove bias"

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
				readings = get_file_readings(file_name, bias_ret)

				# Append this gesture file readings to the whole gesture's readings (file / gesture)
				gesture_acc_readings.append(readings['acc'])
				gesture_gyro_readings.append(readings['gyro'])

		# Append whole gestures readings (gesture)
		gestures['acc_readings'].append(gesture_acc_readings)
		gestures['gyro_readings'].append(gesture_gyro_readings)
	return gestures

def get_file_readings(file_name, bias_ret):
	
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
				#print file_name
				
				line = map(float, line)

				if settings['remove_axis'] == 'X':
					line[2] = 0.0
				elif settings['remove_axis'] == 'Y':
					line[3] = 0.0
				elif settings['remove_axis'] == 'Z':
					line[4] = 0.0

				if settings['remove_bias']:
					# Remove the bias from readings
					acc_reading = [sum(x) for x in zip(bias_ret[0], [line[2], line[3], line[4]+1])]
					gyro_reading = [sum(x) for x in zip(bias_ret[1], line[5:])]
				else:
					acc_reading = [line[2], line[3], line[4]+1]
					gyro_reading = line[5:]
				readings['acc'].append(acc_reading) # remove the -1 effect
				readings['gyro'].append(gyro_reading)

			# Count of zeros before delineation: 
			count_bef = len(readings['acc'])
			readings['acc'] = delineate (readings['acc'], file_name)
			count_aft = len(readings['acc'])
			

			if settings['logging'] :
				print "length before delineation: " + str(count_bef)
				count = [r for r in readings['acc'] if r != [0.0,0.0,0.0]]
				print "length after delineation: " + str(count_aft)

			# :TODO: delineate gyro
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


def normalize (readings): 
	new_readings = copy.deepcopy(readings)
	for g, gesture in enumerate (new_readings):
		for rep, g_file in enumerate(gesture):
			
			#normalized against oneself
			min_limit = min (min (g_file))
			max_limit = max (max (g_file))
			for record in g_file:

				record[0] = (record[0] - min_limit) / (max_limit - min_limit); # x
				record[1] = (record[1] - min_limit) / (max_limit - min_limit); # y
				record[2] = (record[2] - min_limit) / (max_limit - min_limit); # z
	return new_readings

"""
Delineation is to remove the stationary readings at both ends of the single gesture file
Delineation can be for the beginning only (forward), end only (backward), both ends or none
Input: the gesture file, and its name
Output: the delineated file according to the specified delineation in the settings file
"""
def delineate (g_file, file_name):

	if settings['delineation'] == 'both':
		g_file_del_for = delineate_forward (g_file, file_name)
		g_file_delineated = delineate_backward (g_file_del_for, file_name)
	elif settings['delineation'] == 'forward':
		g_file_delineated = delineate_forward (g_file, file_name)
	elif settings['delineation'] == 'backward':
		g_file_delineated = delineate_backward (g_file, file_name)
	else:
		g_file_delineated = g_file

	# Make sure that the first record is [0.0, 0.0,0.0], to indicate start of motion
	if g_file_delineated != [] and g_file_delineated[0] != [0.0, 0.0,0.0]:
		g_file_delineated.insert(0, [0.0, 0.0,0.0])
	
	# Make sure that the last record is [0.0, 0.0,0.0], to indicate end of motion
	if g_file_delineated != [] and g_file_delineated[len(g_file_delineated) - 1 ] != [0.0, 0.0,0.0]:
		g_file_delineated.append([0.0, 0.0,0.0])

	return g_file_delineated

"""
 Removes readings that have an average < idle threshold over a window of size size, with overlap overlap
 Values are removed from the beginning of the gesture only (to keep the relevant only)
 :TODO: do the same in the reverse direction (if necessary)
"""
# filter_idle_over_window
def delineate_forward(g_file, file_name):

	size = settings['window_size']
	overlap = settings['overlap']
	mark = [-0.0, -0.0,-0.0]
	#empty_files_after_cleanup = 0
	new_g_file = copy.deepcopy(g_file)
	
	x_ = [reading[0] for reading in new_g_file ]
	y_ = [reading[1] for reading in new_g_file ]
	z_ = [reading[2] for reading in new_g_file ]
	# x_all_avg = (sum(x_)/len(x_)) * 1.0
	# y_all_avg = (sum(y_)/len(y_)) * 1.0
	# z_all_avg = (sum(z_)/len(z_)) * 1.0
	
	for window_start in xrange(0,len(new_g_file), int (size*overlap)):
		# get average of the window 
		x_avg = (sum(x_[window_start: window_start+size])/ (size* 1.0)) 
		y_avg = (sum(y_[window_start: window_start+size])/ (size* 1.0))
		z_avg = (sum(z_[window_start: window_start+size])/ (size* 1.0)) 
		
		# :TODO: Using a fixed threshold maybe misleading, reconsider the threshold
			# 		 to be the average of the axis
			# if 	(x_avg < x_all_avg and 
			# 	y_avg < y_all_avg and
			# 	z_avg < z_all_avg):
	
	# I care about idle_threshold and -idle_threshold so the abs is used
		if 	(abs(x_avg) < settings['idle_thresh'] and 
			abs(y_avg) < settings['idle_thresh'] and
			abs(z_avg) < settings['idle_thresh']):
			
			# Remove values at the first half of the window as the other half contributes to 
			# the next window due to the overlap
			for i, value in enumerate(new_g_file[window_start : window_start+int (size*overlap)]) :
				# i is the index of the items in the sublist window_start : window_start+size
				# increment i with window_start to make sure that we're at the correct index
				# Don't use this --> new_g_file.remove(value), produces incorrect results as the index is not considered
				new_g_file[i+window_start] = mark
				x_[i+window_start] = 0
				y_[i+window_start] = 0
				z_[i+window_start] = 0
				
		# Once the data starts to show meaningful data, stop 
		else:
			break
		
	# Make sure that all records with the mark [-0.0, -0.0,-0.0] are removed 
	while mark in new_g_file:
			new_g_file.remove(mark)
		
	if len(new_g_file) == 0 and settings['logging']:
		print "Empty file after cleanup: " + str (file_name)
	return new_g_file

def delineate_backward(g_file, file_name):
	size = settings['window_size']
	overlap = settings['overlap']
	mark = [-0.0, -0.0,-0.0]
	
	new_g_file = copy.deepcopy(g_file)
	
	x_ = [reading[0] for reading in new_g_file ]
	y_ = [reading[1] for reading in new_g_file ]
	z_ = [reading[2] for reading in new_g_file ]
	
	for window_end in xrange(len(new_g_file), 0, -1 *int (size*overlap)):
		window_start = window_end - size
		
		# get average of the window 	
		x_avg = (sum(x_[window_start: window_end])/ (size* 1.0)) 
		y_avg = (sum(y_[window_start: window_end])/ (size* 1.0))
		z_avg = (sum(z_[window_start: window_end])/ (size* 1.0)) 
		
		# :TODO: Using a fixed threshold maybe misleading, reconsider the threshold
			# 		 to be the average of the axis
			# if 	(x_avg < x_all_avg and 
			# 	y_avg < y_all_avg and
			# 	z_avg < z_all_avg):
	
	# I care about idle_threshold and -idle_threshold so the abs is used
		if 	(abs(x_avg) < settings['idle_thresh'] and 
			abs(y_avg) < settings['idle_thresh'] and
			abs(z_avg) < settings['idle_thresh']):
			
			# I want to zero the second "half of the window 
			zeros_start = window_end - int (size*overlap)
			for i, value in enumerate(new_g_file[zeros_start: window_end]) :
				# i is the index of the items in the sublist window_start : window_start+size
				# increment i with window_start to make sure that we're at the correct index
				# Don't use this --> new_g_file.remove(value), produces incorrect results as the index is not considered
				
				new_g_file[i+zeros_start] = mark
				x_[i+zeros_start] = 0
				y_[i+zeros_start] = 0
				z_[i+zeros_start] = 0
				
		# Once the data starts to show meaningful data, stop 
		else:
			break
		
	# Make sure that all records with the mark [-0.0, -0.0,-0.0] are removed 
	while mark in new_g_file:
	 		new_g_file.remove(mark)
	
	if len(new_g_file) == 0 and settings['logging']:
		print "Empty file after cleanup: " + str (file_name)
	return new_g_file

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
				if settings['logging']:
					print str(i) + " i"
				for j in range (0, settings['window_size']):
					reading = [sum(x) for x in zip(reading, g_file[i+j])]
				reading = [ x*1.0 / settings['window_size'] for x in reading]
				if settings['logging']:
					print reading
				g_file_r.append(reading)
			gesture_r.append(g_file_r)
		final_readings.append(gesture_r)		
	return final_readings
def count_readings (list):
	return sum(1 for row in list
      for i in row 
      for j in i if j)


"""
Using a separate dataset for calibration, this function: 
1- Reads a bunch of accelerometer/gyro readings files collected while holding a mobile still in hand. 
2- Calculates the average values of these readings in X,Y,Z
3- Returns a list of acc bias and gyro bias
P.S. The values are multiplied by -1 so that they can be summed-up directly
"""
def bias ():
	line_count = 0.0
	acc_reading = [0,0,0]
	gyro_reading = [0,0,0]

	for root,_, files in os.walk(settings ['bias-calib-dir'], topdown=False):
		for name in files :	
			file_name = os.path.join(root, name)

			with open(file_name, 'r') as handler:
				# skip first line 
				handler.readline()
				while True:
					# lines: t --> epoch time in ms, tRel --> relative time in s, acc_x, acc_y, acc_z, gy_x, gy_y, gy_z
					line = handler.readline()
					if line == "": 
						break
					line_count = line_count + 1.0
					line = line.rstrip().split(',')

					# :TODO: check that file is read correctly
					line = map(float, line)
					acc_reading = [sum(x) for x in zip(acc_reading, [line[2], line[3], line[4]+1])]
					gyro_reading = [sum(x) for x in zip(acc_reading, line[5:])]

	acc_reading = [-1*a/line_count for a in acc_reading]
	gyro_reading = [-1*a/line_count for a in acc_reading]

	return [ acc_reading, gyro_reading]
