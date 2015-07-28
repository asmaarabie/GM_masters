# Settings file 
# :TODO: Remove global and use  __all__
global settings 
settings = {
	'dataset_source' 	: "MoGeRe", 
	
	'idle_thresh' 		: 0.15 , # 0.07 should be used so that after cleanup there are no empty
								 # files (the file is wiped as the average of all windows < thresh)
	'dupl_thresh'		: 0.1,
	'codebook_size' 	: 8,
	'logging' 			: True,
	'dataset_root' 		: './Datasets/Lines/', # Where dataset is
	#'gestures_dirs' 	: ['scale-calibration','Bias-calibration'],
	
	# 'gestures_dirs' 	: ['hline-left', 'hline-right', 'Paused-square', 'vline-down', 'vline-up',\
	# 'Long-vs-short', 'Diagonal-ne-sw', 'Diagonal-nw-se', 'Diagonal-se-nw', 'Square-l-d-r-u', \
	# 'Square-u-l-d-r', 'Triangle', 'Z'], 		# Each gesture files is contained in a separate directory
	
	'gestures_dirs' 	: ['hline-left', 'hline-right', 'vline-down', 'vline-up',\
	'Diagonal-ne-sw', 'Diagonal-nw-se', 'Diagonal-se-nw'],
	
	#'gestures_dirs' 	: ['hline-left'],
	'HMM_states'		: 8,					# Number of states per model
	'HMM_type'			: 'left_to_right',		# Type of the HMM 
	'HMM_step'			: 1,					# HMM state transition step
	'cross_validation'	: 0.3,					# percentage of test set for cross_validation
	'HMM_library'		: 'Murphy',				# Type of library used for HMM
	'window_size'		: 5,					# Window readings
	'overlap'			: 0.5,					# Shift window by step
	'delineation'		: 'both',			# Whether to filter stationary data at the beginning/ending of the file or not
	'normalize'			: 0,					# Whether to normalize or not
	'bias-calib-dir'	: './Datasets/Lines/Bias-calibration',
	'remove_bias'		: 1,
	'remove_axis'		: 'Y', 	# When we're in the 2D space we may need to remove the axis that doesn't 
								# contribute to the motion. '' means use all
}
