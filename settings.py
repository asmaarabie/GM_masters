# Settings file 
# :TODO: Remove global and use  __all__
global settings 
settings = {
	'dataset_source' 	: "MoGeRe", 
	
	'idle_thresh' 		: 0.15 , # 0.07 should be used so that after cleanup there are no empty
								 # files (the file is wiped as the average of all windows < thresh)
	#'dupl_thresh'		: 0.1,
	'codebook_size' 	: 8,
	'logging' 			: 1,
	'train_dataset_root' 		: './Datasets/lines_60hz/Train/', # Where train dataset is
	'test_dataset_root' 		: './Datasets/lines_60hz/Test/', # Where test dataset is
	# 'train_dirs' 	: ['hline-left-s', 'hline-right-s'],
	
	'test_dirs'		: [ 'test-hline-left', 'test-hline-right', 'test-vline-down', 'test-vline-up',\
						'test-dline-ne-sw','test-dline-nw-se', 'test-dline-se-nw', 'test-dline-sw-ne',\
						'square-ldru', 'square-rdlu', 'triangle-cw', 'triangle-ccw', 'z', 'tick'],

	'train_dirs' 	: ['hline-left-r', 'hline-right-r', 'vline-down-r', 'vline-up-r',\
						'dline-ne-sw', 'dline-nw-se', 'dline-se-nw', 'dline-sw-ne'],

	#'hline-left-s', 'hline-right-s',\

	
	# 'train_dirs' 	: ['hline-left', 'hline-right', 'vline-down', 'vline-up',\
	# 'Diagonal-ne-sw', 'Diagonal-nw-se', 'Diagonal-se-nw'],

	'cross_validation'	: 0.3,					# percentage of test set for cross_validation
	'HMM_library'		: 'Murphy',				# Type of library used for HMM
	'window_size'		: 5,					# Window readings
	'overlap'			: 0.5,					# Shift window by step
	'delineation'		: 'both',			# Whether to filter stationary data at the beginning/ending of the file or not
	'normalize'			: 0,					# Whether to normalize or not
	'bias-calib-dir'	: './Datasets/lines_60hz/Train/calibration_bias',
	'remove_bias'		: 1,
	'remove_axis'		: '', 	# When we're in the 2D space we may need to remove the axis that doesn't 
								# contribute to the motion. '' means use all
	'load_codebook'		: 0,
	'load_bias'			: 1,
	'fixed_codebook'	: 0, 	# Is the codebook fixed? 
}


