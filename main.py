"""
Goal: Quanitzation of training data
Gestures: obtained using mobile inertial sensors
Asmaa Rabie - 2015
"""
from DataFileProcessor import *
from settings import settings
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
from scipy import io
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random 
import itertools

logging = settings['logging']

# Gesture 
gestures = {
	'train_root': settings['train_dataset_root'],			# Where train dataset is
	'test_root': settings['test_dataset_root'],			# Where test dataset is
	'train_dirs' : settings['train_dirs'], 		# Each gesture files is contained in a separate directory
	'test_dirs' : settings['test_dirs'], 
	'file_count': [],				# Number of files per gesture
	'acc_readings_train': [],				# All Accelerometer readings for all files per all gestures 
	'gyro_readings_train': [],			# All Gyroscope readings for all files per all gestures 
	'acc_codebook_train' : [],			# Centroids of a gesture
	'acc_mapped_to_codebook_train': [],	# Accelerometer readings mapped to gesture codebook
	'acc_readings_test': [],				# All Accelerometer readings for all files per all gestures 
	'gyro_readings_test': [],			# All Gyroscope readings for all files per all gestures 
	'acc_codebook_test' : [],			# Centroids of a gesture
	'acc_mapped_to_codebook_test': [],	# Accelerometer readings mapped to gesture codebook
}

def create_gesture_codebook_fixed(maxval,minval,midval):
	values = [maxval,maxval,maxval,minval,minval,minval,midval,midval,midval]
	permutations = list(itertools.permutations(values,3)) 
	
	# Permutations are in tuple form, we need them in list form
	codebook = [list(p) for p in set(permutations) ]

	# Return unique tuples
	file_path = 'codebook_fixed.npy'
	np.save(file_path,np.array(codebook))
	

def create_gesture_codebook (gestures) :
	"""
	Before running k-means, it is beneficial to rescale each feature dimension of the observation
	set with whitening. Each feature is divided by its standard deviation across all observations 
	to give it unit variance.
	"""

	# Flatten gesture readings: as each gesture has F files each containing R readings
	flattened = [reading for gesture in gestures for g_file in gesture for reading in g_file]

	# Normalize observations
	#whitened = whiten(flattened)
	kmean_res = KMeans(n_clusters=settings['codebook_size'], init='k-means++', precompute_distances = True)
	kmean_res.fit(flattened)
	#kmean_res.fit(whitened)
	return [kmean_res.cluster_centers_, kmean_res.inertia_ ]
	
	# kmean_res, dist = kmeans(whitened, settings['codebook_size'])
	# return [kmean_res, dist ]

def map_gesture_to_codebook (gesture, codebook):
	quantized_gesture=[]
	for rep, g_file in enumerate(gesture):
		# Sometimes the g_file is empty due to data cleanup, empty files should be removed
		# Since we need the size of samples to be the same / gesture, I'll replicate
		# samples randomly, :TODO: REMOVE THE REPLICATION
		index = 0
		while len(g_file) == 0 :
			random.seed(index)
			index = random.randint(0,len(gesture)-1)
			g_file = gesture[index]

		[code, distortion] = vq(np.array(g_file),codebook)
		code = code.tolist()
		
		if settings['HMM_library'] == "Murphy" :
			# as we're working on matlab, indices there starts with 1
			code  = [c+1 for c in code]

		quantized_gesture.append(code)
	return quantized_gesture


def main(gestures):
	distortion = 0
	############################### TRAIN DATA ############################### 
	# Step #1 : Read and prepare readings
	[gestures['acc_readings_train'], gestures['gyro_readings_train']] = get_gesture_readings(gestures['train_dirs'], gestures['train_root'])
	
	# Step #2 : Quantize the readings and create clusters
	
	if settings["fixed_codebook"]:
		file_path = 'codebook_fixed.npy'
		codebook = np.load(file_path)
		if logging: print codebook
	else:

		file_path = 'codebook.npy'
		if settings["load_codebook"] and os.path.exists(file_path):
			[codebook, distortion] = np.load(file_path)
		else:
			[codebook, distortion] = create_gesture_codebook (gestures['acc_readings_train'])
			np.save(file_path,np.array([codebook, distortion]))
	
	
	# Step #3 : Map each gesture sample to a codebook 
	for index, gesture in enumerate(gestures['acc_readings_train']):
		mapped_gesture = map_gesture_to_codebook(gesture, codebook)
		gestures['acc_mapped_to_codebook_train'].append(mapped_gesture)

	
	# Step #4 : save matrix
	path = 'Datasets/processed/line60hz_train.mat'
	try:
		os.remove(path)
	except OSError:
		pass
	io.savemat(path, mdict={'train': np.array(gestures['acc_mapped_to_codebook_train'])})
	
	############################### TEST DATA ############################### 
	# 1. Read test data
	[gestures['acc_readings_test'], gestures['gyro_readings_test']] = get_gesture_readings(gestures['test_dirs'], gestures['test_root'])
	
	# 2. Map test data to codebook
	for index, gesture in enumerate(gestures['acc_readings_test']):
		mapped_gesture = map_gesture_to_codebook(gesture, codebook)
		gestures['acc_mapped_to_codebook_test'].append(mapped_gesture)
	
	# 3. save matrix
	path = 'Datasets/processed/line60hz_test.mat'
	try:
		os.remove(path)
	except OSError:
		pass
	io.savemat(path, mdict={'test': np.array(gestures['acc_mapped_to_codebook_test'])})

	if logging: print "distortion: " + str(distortion)
	with open('run.log', 'w+') as logger :
		logger.write("========= Printing codebook: ========= \n")
		logger.write(str(codebook)+"\n")


main (gestures)