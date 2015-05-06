from scipy.cluster.vq import vq, kmeans, whiten
import numpy as np
from settings import settings
from sklearn.cluster import KMeans
def create_gesture_codebook (gestures) :
	"""
	Before running k-means, it is beneficial to rescale each feature dimension of the observation
	set with whitening. Each feature is divided by its standard deviation across all observations 
	to give it unit variance.
	
	Modification: creating a single codebook for all classes
	"""
	# Flatten gesture readings: as each gesture has F files each containing R readings
	#for g_file in gesture:

	flattened = [reading for gesture in gestures for g_file in gesture for reading in g_file]

	# Normalize observations
	#whitened = whiten(flattened)

	#k-means
	#kmean_res = kmeans(whitened, settings['codebook_size'])

	kmean_res = KMeans(n_clusters=settings['codebook_size'], init='k-means++', max_iter=1000)
	kmean_res.fit(flattened)

	# :TODO: kmeans chooses the seed codebook randomly fix it to get consistent result every time
	# :TODO: minimize the distortion 
	#return kmean_res
	return [kmean_res.cluster_centers_, kmean_res.inertia_ ]

def map_gesture_to_codebook (gesture, codebook):
	quantized_gesture=[]
	for g_file in gesture:
		[code, distortion] = vq(np.array(g_file),codebook)
		quantized_gesture.append(code.tolist())
	return quantized_gesture
