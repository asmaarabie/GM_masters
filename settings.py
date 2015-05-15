# Settings file 
# :TODO: Remove global and use  __all__
global settings 
settings = {
	'dataset_source' 	: "MoGeRe", 
	'idle_thresh' 		: 0.2 ,
	'dupl_thresh'		: 0.1,
	'codebook_size' 	: 8,
	'logging' 			: True,
	'dataset_root' 		: './Datasets/square_parts_dataset/', # Where dataset is
	'gestures_dirs' 	: ['hline-left', 'hline-right', 'square', 'vline-down', 'vline-up'], 		# Each gesture files is contained in a separate directory
	# 'dataset_root' 		: './Datasets/tick_z/', # Where dataset is
	# 'gestures_dirs' 	: ['tick', 'z'], 		# Each gesture files is contained in a separate directory

	'HMM_states'		: 8,					# Number of states per model
	'HMM_type'			: 'left_to_right',		# Type of the HMM 
	'HMM_step'			: 1,					# HMM state transition step
	'cross_validation'	: 0.3,					# percentage of test set for cross_validation
	'HMM_library'		: 'GHMM',				# Type of library used for HMM
	'window_size'		: 4,					# Window readings
	'overlap'			: 0.5,					# Shift window by step
	'filter'			: 1,
}
