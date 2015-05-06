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

def create_gesture_codebook (gestures) :
	"""
	Before running k-means, it is beneficial to rescale each feature dimension of the observation
	set with whitening. Each feature is divided by its standard deviation across all observations 
	to give it unit variance.
	
	Modification: creating a single codebook for all classes
	"""
	# Flatten gesture readings: as each gesture has F files each containing R readings
	flattened = [reading for gesture in gestures for g_file in gesture for reading in g_file]

	# Normalize observations
	whitened = whiten(flattened)

	#kmean_res = kmeans(whitened, settings['codebook_size'])

	kmean_res = KMeans(n_clusters=settings['codebook_size'], init='k-means++', precompute_distances = True)
	kmean_res.fit(flattened)

	return [kmean_res.cluster_centers_, kmean_res.inertia_ ]

def map_gesture_to_codebook (gesture, codebook):
	quantized_gesture=[]
	for g_file in gesture:
		[code, distortion] = vq(np.array(g_file),codebook)
		quantized_gesture.append(code.tolist())
	return quantized_gesture

def main(gestures):
	# Step #1 : Read and prepare readings
	gestures = get_gesture_readings(gestures)

	# Step #2 : Quantize the readings and create clusters
	[codebook, distortion] = create_gesture_codebook (gestures['acc_readings'])

	# Step #3 : Map each gesture sample to a codebook 
	for index, gesture in enumerate(gestures['acc_readings']):
		mapped_gesture = map_gesture_to_codebook(gesture, codebook)
		gestures['acc_mapped_to_codebook'].append(mapped_gesture)

	# Step #4 : save matrix
		
	io.savemat('acc_mapped_to_codebook.mat', mdict={'acc_mapped_to_codebook': np.array(gestures['acc_mapped_to_codebook'])})

	print "distortion: " + str(distortion)

main (gestures)