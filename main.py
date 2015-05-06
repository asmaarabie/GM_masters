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
import numpy as np
from scipy import io
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

if settings['fix_codebook']:
	codebook = [[-2.58032872,  1.22232672, -3.19769464],[-0.23537363,  0.9377733 , -3.25300466],[ 2.05304668,  1.73431208, -1.45511493],[ 0.24254074, -1.29714679, -1.11262586],[ 1.12014571, -0.04378861, -0.2754391 ],[-0.63469265, -0.87085437, -1.66018654],[-0.53616722,  0.92212641, -0.18549875],[ 0.11771225, -0.3502949 , -1.86334384]], [[ 1.17318087, -0.10933118, -0.3075629 ],[ 2.01992254,  4.51979286,  0.77842361],[ 1.12594249,  0.8938325 ,  0.71254726],[-0.06466168, -0.61330756, -1.86071025],[-0.67497638, -0.54428757, -1.60033961],[-1.61999701,  1.14632941, -0.95398697],[-0.08261172,  0.05013973, -1.79958783],[ 1.8348483 , -0.27255504, -1.87235827]]
	codebook = np.asarray(codebook)
	distortion = 0
	gestures['acc_codebook'] = codebook

for index, gesture in enumerate(gestures['acc_readings']):

# Step #2 : Quantize the readings and create clusters
	if not settings['fix_codebook']:
		[codebook, distortion] = create_gesture_codebook (gesture)
		gestures['acc_codebook'].append(codebook)
	
	mapped_gesture = map_gesture_to_codebook(gesture, gestures['acc_codebook'][index])
	gestures['acc_mapped_to_codebook'].append(mapped_gesture)
	
	

# Step #3 Select a subset for training 
# 	[train_set, test_set] = cross_validation.train_test_split(mapped_gesture, test_size=0.3)
# 	train_set = train_set.tolist()
# 	test_set = test_set.tolist()
# 	gestures['train'].append(train_set)
# 	labels = [index]* len(test_set)
# 	labled_test_set = zip (test_set, labels)
# 	gestures['test'].append(labled_test_set)
	
# # Step #4 : Init HMM params
# # Step #5 : Train models. Baum-welch to optimize the model
# 	m = train_gesture(train_set)
# 	gestures['HMM'].append(m)

# 	if settings['logging'] :
# 		with open('run.log', 'aw+') as logger :
# 			logger.write("Distortion for gesture: " + gestures['g_dir'][index] \
# 				+ " " + str(distortion) +" \n")
# 			logger.write("========= Printing HMM model settings after BW for gesture \""+ \
# 				gestures['g_dir'][index]+"\" : ========= \n")
# 			logger.write(str(m))

# # Step #5 : Test models.
# # Test set is already labled, flatten it 
# test_set = [ g_file for gesture in gestures['test'] for g_file in gesture]
# test_gesture(test_set, gestures['HMM'])

io.savemat('acc_mapped_to_codebook.mat', mdict={'acc_mapped_to_codebook': np.array(gestures['acc_mapped_to_codebook'])})

#print m.cmodel
if settings['logging'] :
	with open('run.log', 'aw+') as logger :
		logger.write("========= Printing run settings: ========= \n")
		logger.write(str(settings.items())+"\n")
		logger.write("Count of readings before filter: " + str (c_bef_filter) + "\n")
		logger.write("Count of readings after filter: " + str (c_after_filter) + "\n")
		logger.write("========= Printing codebook: ========= \n")
		logger.write(str(gestures['acc_codebook'])+ "\n")
		logger.write("========= Printing gesture struct info: ========= \n")
		logger.write(str(gestures.items()))

		