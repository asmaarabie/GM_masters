"""
Goal: Train gestures using HMMs
Gestures: obtained using mobile inertial sensors
Asmaa Rabie - 2015
"""
from DataFileProcessor import *

dataset_source = "MoGeRe"
idle_thresh = 0.1 
dupl_thresh = 0.1
# Gesture 
gestures = {
	'root': './Datasets/tick_z/',	# Where dataset is
	'g_dir' : ['tick', 'z'], 		# Each gesture files is contained in a separate directory
	'file_count': [],				# Number of files per gesture
	'acc_readings': [],				# All Accelerometer readings for all files per all gestures 
	'gyro_readings': []				# All Gyroscope readings for all files per all gestures 
}

# Step #1 : Read and prepare readings
# 	1.1 : read
gestures = get_gesture_readings(gestures, dataset_source)

# 	1.2 : filter
print "Count of readings before filter: " + str (count_readings(gestures['acc_readings']))

gestures['acc_readings'] = filter_idle_and_dupl(gestures['acc_readings'], idle_thresh, dupl_thresh)

print "Count of readings after filter: " + str (count_readings(gestures['acc_readings']))


# Step #2 : Quantize the readings and create clusters

# Step #3 : Init HMM params

# Step #4 : Train models. Baum-welch to optimize the model

# Step #5 : Test models.


