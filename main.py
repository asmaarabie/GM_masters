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

"""
:TODO: write this function's describtion
"""
def replicate (gesture) :
	for rep, g_file in enumerate(gesture):
		if len(g_file) != 0 :
			replica = g_file
			break
	return replica

def map_gesture_to_codebook (gesture, codebook):
	quantized_gesture=[]
	for rep, g_file in enumerate(gesture):
		# Sometimes the g_file is empty due to data cleanup, empty files should be removed
		# Since we need the size of samples to be the same / gesture, I'll replicate
		# samples randomly, :TODO: find another way 
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

def plot (sample):
	
	t = np.arange(0,len(sample), 1)

	# sample is the accelerometer sample
	x_data = [x for x,y,z in sample ]
	y_data = [y for x,y,z in sample ]
	z_data = [z for x,y,z in sample ]


	# Plotting Acc 
	plt.plot(t, x_data, 'r', label='X')
	plt.axhline(np.asarray(x_data).mean(), color='r', linestyle='dashed', linewidth=2)

	plt.plot(t, y_data, 'g', label='Y')
	plt.axhline(np.asarray(y_data).mean(), color='g', linestyle='dashed', linewidth=2)
	
	plt.plot(t, z_data, 'b', label='Z')
	plt.axhline(np.asarray(z_data).mean(), color='b', linestyle='dashed', linewidth=2)
	plt.legend()
	

def main(gestures):
	
	# Step #1 : Read and prepare readings
	gestures = get_gesture_readings(gestures)
	
	# Plot first sample of the first gesture
	plot(gestures['acc_readings'][0][0])
	plt.show()

	# Step #2 : Quantize the readings and create clusters
	[codebook, distortion] = create_gesture_codebook (gestures['acc_readings'])
	
	# Step #3 : Map each gesture sample to a codebook 
	for index, gesture in enumerate(gestures['acc_readings']):
		mapped_gesture = map_gesture_to_codebook(gesture, codebook)
		gestures['acc_mapped_to_codebook'].append(mapped_gesture)

	# Step #4 : save matrix
	
	
	path = 'Datasets/processed/square_parts_mapped_filtered_1431887536.mat'
	try:
		os.remove(path)
	except OSError:
		pass
	io.savemat(path, mdict={'acc_mapped_to_codebook': np.array(gestures['acc_mapped_to_codebook'])})
	print "distortion: " + str(distortion)
	with open('run.log', 'w+') as logger :
		logger.write("========= Printing codebook: ========= \n")
		logger.write(str(codebook)+"\n")


	

main (gestures)