"""
Goal: Train gestures using HMMs
Gestures: obtained using mobile inertial sensors
Asmaa Rabie - 2015
"""
from DataFileProcessor import *
from quantizer import *
from settings import settings

# Gesture 
gestures = {
	'root': settings['dataset_root'],			# Where dataset is
	'g_dir' : settings['gestures_dirs'], 		# Each gesture files is contained in a separate directory
	'file_count': [],				# Number of files per gesture
	'acc_readings': [],				# All Accelerometer readings for all files per all gestures 
	'gyro_readings': [],			# All Gyroscope readings for all files per all gestures 
	'acc_codebook' : [],			# Centroids of a gesture
	'acc_mapped_to_codebook': []	# Accelerometer readings mapped to gesture codebook
}
if settings['logging'] :
	with open('run.log', 'w+') as logger :
		logger.write("Started running ...\n")

# Step #1 : Read and prepare readings
# 	1.1 : read
gestures = get_gesture_readings(gestures)

# 	1.2 : filter
c_bef_filter = count_readings(gestures['acc_readings'])
gestures['acc_readings'] = filter_idle_and_dupl(gestures['acc_readings'])
c_after_filter = count_readings(gestures['acc_readings'])

# Step #2 : Quantize the readings and create clusters
for index, gesture in enumerate(gestures['acc_readings']):
	[codebook, distortion] = create_gesture_codebook (gesture)
	gestures['acc_codebook'].append(codebook)
	gestures['acc_mapped_to_codebook'].append(map_gesture_to_codebook(gesture, codebook))
	if settings['logging'] :
		with open('run.log', 'aw+') as logger :
			logger.write("Distortion for gesture: " + gestures['g_dir'][index] \
				+ " " + str(distortion) +" \n")




# Step #3 : Init HMM params

# Step #4 : Train models. Baum-welch to optimize the model

# Step #5 : Test models.


if settings['logging'] :
	with open('run.log', 'aw+') as logger :
		logger.write("Printing run settings: \n")
		logger.write(str(settings.items())+"\n")
		logger.write("Count of readings before filter: " + str (c_bef_filter) + "\n")
		logger.write("Count of readings after filter: " + str (c_after_filter) + "\n")
		logger.write("Printing gesture struct info: \n")
		logger.write(str(gestures.items()))