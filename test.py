def filter_idle_over_window(readings, size, overlap):
	#for gesture in readings:
	for g_file in readings:
		x_ = [abs(reading[0]) for reading in g_file ]
		y_ = [reading[1] for reading in g_file ]
		z_ = [reading[2] for reading in g_file ]

		print x_
		print y_
		print z_
		print "yahoo"
		g_file.remove()
	return readings
filter_idle_over_window ([[[-1,2,3],[4,5,6]] , [[7,8,9],[10,11,12]]], 4, 0.5)
