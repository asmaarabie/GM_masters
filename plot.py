"""
Goal: Plotting data for better understanding
Gestures: obtained using mobile inertial sensors
Asmaa Rabie - 2015
"""
from DataFileProcessor import *
from settings import settings
import numpy as np
import matplotlib.pyplot as plt
import shutil
gestures = {
	'train_root': settings['train_dataset_root'],			# Where train dataset is
	'train_dirs' : settings['train_dirs'], 		# Each gesture files is contained in a separate directory
	'file_count': [],				# Number of files per gesture
	'acc_readings': [],				# All Accelerometer readings for all files per all gestures 
	'gyro_readings': [],			# All Gyroscope readings for all files per all gestures 
}

def main(gestures):
	# Step #1 : Read and prepare readings
	gestures = get_gesture_readings(gestures['train_dirs'], gestures['train_root'])
	
	dir_name = "plots/lines_60hz/";
	shutil.rmtree(dir_name)
	os.mkdir(dir_name, 0777)

	for g_index, gesture in enumerate(gestures['acc_readings']):
		os.mkdir(dir_name+"/"+gestures['g_dir'][g_index], 0777)
		for s_index, sample in enumerate(gesture):
			
			fig = plt.figure(figsize=(10,5))
			fig.suptitle("Gesture: "+ gestures['g_dir'][g_index] + ", sample: " + str(s_index), fontsize=18);
			#fig.subplots_adjust(wspace=1)

			t = np.arange(0,len(sample), 1)

			# sample is the accelerometer sample
			x_data = [x for x,y,z in sample ]
			y_data = [y for x,y,z in sample ]
			z_data = [z for x,y,z in sample ]


			# Plotting Acc 
			acc_plt = plt.subplot(121)
			acc_plt.set_title('Accelerometer data', fontsize=14)
			plt.xlabel('readings', fontsize=12)
			plt.ylabel('time', fontsize=12)

			plt.plot(t, x_data, 'r', label='X')
			plt.axhline(np.asarray(x_data).mean(), color='r', linestyle='dashed', linewidth=2)

			plt.plot(t, y_data, 'g', label='Y')
			plt.axhline(np.asarray(y_data).mean(), color='g', linestyle='dashed', linewidth=2)
			
			plt.plot(t, z_data, 'b', label='Z')
			plt.axhline(np.asarray(z_data).mean(), color='b', linestyle='dashed', linewidth=2)
			plt.legend()
			
			# g_sample is the gyro sample

			g_sample = gestures['gyro_readings'][g_index][s_index]; # 2 for the square gesture, 0 for the first sample
			t = np.arange(0,len(g_sample), 1)
			pitch_data = [x for x,y,z in g_sample ]
			roll_data = [y for x,y,z in g_sample ]
			yaw_data = [z for x,y,z in g_sample ]

			# Plotting Gyro
			gyro_plt = plt.subplot(122)
			gyro_plt.set_title('Gyroscope data', fontsize=14)
			plt.xlabel('readings', fontsize=12)
			plt.ylabel('time', fontsize=12)

			plt.plot(t, pitch_data, 'c', label='Pitch')
			plt.axhline(np.asarray(pitch_data).mean(), color='c', linestyle='dashed', linewidth=2)

			plt.plot(t, roll_data, 'm', label='Roll')
			plt.axhline(np.asarray(roll_data).mean(), color='m', linestyle='dashed', linewidth=2)
			
			plt.plot(t, yaw_data, 'y', label='Yaw')
			plt.axhline(np.asarray(yaw_data).mean(), color='y', linestyle='dashed', linewidth=2)
	
			plt.legend()
			plt.savefig(dir_name+"/"+gestures['g_dir'][g_index]+"/"+"rep"+str(s_index)+".png",  bbox_inches='tight')

			plt.close(fig)

main (gestures)



