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
	'train_root': settings['train_dataset_root'],			# Where train dataset is
	'test_root': settings['test_dataset_root'],			# Where test dataset is
	'train_dirs' : settings['train_dirs'], 		# Each gesture files is contained in a separate directory
	'test_dirs' : settings['test_dirs'], 
	'file_count': [],				# Number of files per gesture
	'acc_readings': [],				# All Accelerometer readings for all files per all gestures 
	'gyro_readings': [],			# All Gyroscope readings for all files per all gestures 
	'acc_codebook' : [],			# Centroids of a gesture
	'acc_mapped_to_codebook': [],	# Accelerometer readings mapped to gesture codebook
	'HMM': [],						# HM models for each gesture
	'train': [],					# Filtered & Quantized subset of the gesture data for training
	'test': [],						# Filtered & Quantized subset of the gesture data for testing
}
def main(gestures):
	
	# Step #1 : Read and prepare readings
	gestures = get_gesture_readings(gestures['train_dirs'], gestures['train_root'])
	path = 'Datasets/processed/acc_readings.mat'
	
	try:
		os.remove(path)
	except OSError:
		pass

	print len(gestures['acc_readings'])
	io.savemat(path, mdict={'acc_readings': np.array(gestures['acc_readings'])})
main (gestures)