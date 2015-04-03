"""
Goal: Train gestures using HMMs
Gestures: obtained using mobile inertial sensors
Asmaa Rabie - 2015
"""
from DataFileProcessor import *
from quantizer import *
from settings import settings
from HMM import *
from sklearn import cross_validation

# Gesture 
gestures = {
	'root': settings['dataset_root'],			# Where dataset is
	'g_dir' : settings['gestures_dirs'], 		# Each gesture files is contained in a separate directory
	'file_count': [],				# Number of files per gesture
	'acc_readings': [],				# All Accelerometer readings for all files per all gestures 
	'gyro_readings': [],			# All Gyroscope readings for all files per all gestures 
	'acc_codebook' : [],			# Centroids of a gesture
	'acc_mapped_to_codebook': [],	# Accelerometer readings mapped to gesture codebook
	'HMM': [],						# HM models for each gesture
	'train': [],					# Filtered & Quantized subset of the gesture data for training
	'test': [],						# Filtered & Quantized subset of the gesture data for testing
}

if settings['logging'] :
	with open('run.log', 'w+') as logger :
		logger.write("========= Started running ... =========\n")

# Step #1 : Read and prepare readings
# 	1.1 : read
gestures = get_gesture_readings(gestures)

# 	1.2 : filter
c_bef_filter = count_readings(gestures['acc_readings'])
#gestures['acc_readings'] = filter_idle_and_dupl(gestures['acc_readings'])
c_after_filter = count_readings(gestures['acc_readings'])


for index, gesture in enumerate(gestures['acc_readings']):

# Step #2 : Quantize the readings and create clusters
	[codebook, distortion] = create_gesture_codebook (gesture)
	gestures['acc_codebook'].append(codebook)
	mapped_gesture = map_gesture_to_codebook(gesture, codebook)
	gestures['acc_mapped_to_codebook'].append(mapped_gesture)

# Step #3 Select a subset for training 
	[train_set, test_set] = cross_validation.train_test_split(mapped_gesture, test_size=0.3)
	train_set = train_set.tolist()
	test_set = test_set.tolist()
	gestures['train'].append(train_set)
	labels = [index]* len(test_set)
	labled_test_set = zip (test_set, labels)
	gestures['test'].append(labled_test_set)
	
# Step #4 : Init HMM params
# Step #5 : Train models. Baum-welch to optimize the model
	m = train_gesture(train_set)
	gestures['HMM'].append(m)

	if settings['logging'] :
		with open('run.log', 'aw+') as logger :
			logger.write("Distortion for gesture: " + gestures['g_dir'][index] \
				+ " " + str(distortion) +" \n")
			logger.write("========= Printing HMM model settings after BW for gesture \""+ \
				gestures['g_dir'][index]+"\" : ========= \n")
			logger.write(str(m))

# Step #5 : Test models.
# Test set is already labled, flatten it 
test_set = [ g_file for gesture in gestures['test'] for g_file in gesture]
test_gesture(test_set, gestures['HMM'])

print m.cmodel
if settings['logging'] :
	with open('run.log', 'aw+') as logger :
		logger.write("========= Printing run settings: ========= \n")
		logger.write(str(settings.items())+"\n")
		logger.write("Count of readings before filter: " + str (c_bef_filter) + "\n")
		logger.write("Count of readings after filter: " + str (c_after_filter) + "\n")
		logger.write("========= Printing gesture struct info: ========= \n")
		logger.write(str(gestures.items()))