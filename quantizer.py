from scipy.cluster.vq import vq, kmeans, whiten
import numpy as np
from settings import settings
def create_gesture_codebook (gesture) :
	"""
	Before running k-means, it is beneficial to rescale each feature dimension of the observation
	set with whitening. Each feature is divided by its standard deviation across all observations 
	to give it unit variance.
	"""
	# Flatten gesture readings: as each gesture has F files each containing R readings
	flattened = [reading for g_file in gesture for reading in g_file]

	# Whiten observations
	whitened = whiten(flattened)
	
	#k-means
	kmean_res = kmeans(whitened, settings['codebook_size'])
	
	# :TODO: kmeans chooses the seed codebook randomly fix it to get consistent result every time
	# :TODO: minimize the distortion 
	return kmean_res
	
def map_gesture_to_codebook (gesture, codebook):
	quantized_gesture=[]
	for g_file in gesture:
		[code, distortion] = vq(np.array(g_file),codebook)
		quantized_gesture.append(code.tolist())
	return quantized_gesture
