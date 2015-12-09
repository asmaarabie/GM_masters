import pprint
hmms = ["left", "right", "down", "up"]
# Concatenated left, down, right, up observation sequence
# Observation sequence
O = [
8,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,5,5,5,1,1,1,1,1,1,1,1,1,1,1,1,8,8,8,8, # down
8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8, # right
8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,7,7,7,7,7,7,7,7,7,7,7,7,3,3,8,8, # up
8,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,2,2,2,2,2,2,8,8,8,8,8,8,8,8,8,8,8,8 # left
]
A = {}
B = {}			
T= len(O)			# Length of the observation sequence
N = 8			# Number of states
M = len (hmms)		# Number of models
L = 4				# Levels

# Joint probability of partial sequence
# Access as: d[Model q][at time t][at state j] 
d = [[[0 for k in xrange(N)] for j in xrange(T)] for i in xrange(M)]

# Level output probability at each time frame for each model
#Access as: P[Level][at time t][for model q]
P = [[[0 for k in xrange(M)] for j in xrange(T)] for i in xrange(L)]

# Level output BEST probability at each time frame
#Access as: Phat[Level][at time t]
Phat = [[0 for j in xrange(T)] for i in xrange(L)]

# Level output backpointer at each time frame
#Access as: BP[Level][at time t][for model q]
BP = [[[0 for k in xrange(M)] for j in xrange(T)] for i in xrange(L)]

# Level output backpointer at each time frame
#Access as: BP[Level][at time t]
BPhat = [[0 for j in xrange(T)] for i in xrange(L)]

# Level output model indicator
#Access as: W[Level][at time t]
W = [[0 for j in xrange(T)] for i in xrange(L)]



A["left"] = [
[0,    1.0000,         0,         0,         0,         0,         0,         0],
[0,    0.5151,    0.4849,         0,         0,         0,         0,         0],
[0,         0,    0.6822,    0.3178,         0,         0,         0,         0],
[0,         0,         0,    0.7603,    0.2397,         0,         0,         0],
[0,         0,         0,         0,    0.8113,    0.1887,         0,         0],
[0,         0,         0,         0,         0,    0.8043,    0.1957,         0],
[0,         0,         0,         0,         0,         0,    0.7571,    0.2429],
[0,         0,         0,         0,         0,         0,         0,    1.0000]
]
A["right"] = [
[0.5402,    0.4598,     0,         	0,         	0,         0,         0,         0],
[0,    		0.6078,    	0.3922,     0,         	0,         0,         0,         0],
[0,         0,   		0.6281,    	0.3719,     0,         0,         0,         0],
[0,         0,         	0,    		0.6327,    	0.3673,    0,         0,         0],
[0,         0,         	0,         	0,    		0.6313,    0.3687,         0,         0],
[0,         0,         	0,         	0,         0,    		0.6013,    0.3987,         0],
[0,         0,         	0,         	0,         0,         	0,    		0.7301,    0.2699],
[0,         0,         	0,         	0,         0,         	0,         0,    1.0000]
]
A["down"] = [
[0,    1.0000,         0,         0,         0,         0,         0,         0],
[0,    0.9349,    0.0651,         0,         0,         0,         0,         0],
[0,         0,    0.9115,     0.0885,         0,         0,         0,         0],
[0,         0,         0,    0.1224,     0.8776,         0,         0,         0],
[0,         0,         0,         0,    0.4219,    0.5781,         0,         0],
[0,         0,         0,         0,         0,    0.9181,     0.0819,         0],
[0,         0,         0,         0,         0,         0,     0.6915,    0.3085],
[0,         0,         0,         0,         0,         0,         0,    1.0000]
]
A["up"] = [
[0,    1.0000,         0,         0,         0,         0,         0,         0],
[0,    0.9043,     0.0957,         0,         0,         0,         0,         0],
[0,         0,     0.9272,     0.0728,         0,         0,         0,         0],
[0,         0,         0,    0.3263,      0.6737,         0,         0,         0],
[0,         0,         0,         0,     0.5756,    0.5781,         0,         0],
[0,         0,         0,         0,         0,    0.9181,     0.4244,         0],
[0,         0,         0,         0,         0,         0,      0.9040,    0.1861],
[0,         0,         0,         0,         0,         0,         0,    1.0000]
]

B["left"]= [
[0,         0,         0,    0.0000,         0,         0,         0,    1.0000],
[0,         0,         0,    1.0000,         0,         0,         0,    0.0000],
[0,         0,         0,    0.9998,         0,    0.0000,         0,    0.0002],
[0,         0,         0,    0.9969,         0,    0.0000,         0,    0.0031],
[0,    0.0000,         0,    0.9999,    0.0000,    0.0000,         0,    0.0001],
[0,    0.0000,         0,    1.0000,    0.0000,    0.0000,         0,    0.0000],
[0,    0.0001,         0,    0.8522,    0.0123,    0.1355,         0,    0.0000],
[0,    0.0860,         0,    0.0000,    0.0000 ,   0.0000,         0,    0.9140]
]
B["right"]= [
[0,         0,         0,         0,         0,         0,         0,    1.0000],
[0,         0,         0,         0,         0,         0,         0,    1.0000],
[0,         0,         0,         0,         0,         0,    0.0000,    1.0000],
[0,    0.0000,         0,         0,         0,         0,    0.0000,    1.0000],
[0,    0.0000,         0,    0.0000,         0,         0,    0.0000,    1.0000],
[0,    0.0000,         0,    0.0000,    0.0000,         0,   0.0000 ,   1.0000],
[0,    0.4723,         0,    0.0000,    0.0000,    0.0000,    0.0450,    0.4827],
[0,    0.0000,         0,    0.9001,    0.0073,    0.0473,    0.0000,    0.0453]
]
B["down"]= [
[0,    0.0000,    0.0000,    0.0000,         0,         0,    0.0000,    1.0000],
[0,    0.0026,    0.9974,    0.0000,         0,         0,    0.0000,    0.0000],
[0,    0.0036,    0.9964,    0.0000,         0,    0.0000,    0.0000,    0.0000],
[0,    0.0000,    0.1454,    0.0000,         0,    0.0000,    0.8546,    0.0000],
[0.0000,    0.0000,    0.0470,    0.0788,         0,    0.0000,    0.5437,    0.3306],
[0.0000,  0.0000,    0.0000,    0.0000,    0.0000,    0.0635,    0.9364,    0.0000],
[0.0005,    0.0000,    0.0140,    0.0841,    0.0000,    0.0272,    0.1516,    0.7225],
[0.1729,    0.7891,    0.0000,    0.0000,    0.0173,    0.0000,    0.0007,    0.0200],
]
B["up"]= [
[0.0000,    0.0000,         0,         0,   0.0000,         0,         0,    1.0000],
[0.0000,    1.0000,         0,         0,    0.0000,         0,         0,    0.0000],
[0.0000,    1.0000,         0,         0,    0.0000,         0,         0,    0.0000],
[0.5454,    0.2907,         0,         0,    0.1621,         0,         0,    0.0018],
[0.3032,    0.0420,         0,    0.0000,    0.2161,         0,    0.0000,    0.4386],
[0.9402,    0.0000,         0,    0.0000,    0.0598,    0.0000,    0.0000,    0.0000],
[0.0002,    0.3954,    0.0000,    0.0372,    0.0259,    0.0000,    0.0193,    0.5219],
[0.0000,    0.0000,    0.6914,    0.0000,    0.0000,    0.0017,    0.2817,    0.0253],
]
