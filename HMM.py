from ghmm import *
import numpy as np
from settings import settings
from sklearn.metrics import confusion_matrix

def train_gesture (gesture):
	
	# Initialize HMM
	[sigma, A, B, pi] = init_HMM()
	# TN: HMMFromMatrices, DiscreteDistribution
	m = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)

	# :TODO: Find how to train multiple sequences
	# All sequences (all files) for a gesture is used for Expectation maximization
	flattened = [reading for g_file in gesture for reading in g_file]
	train_seq = EmissionSequence(sigma, flattened)
	m.baumWelch(train_seq)

	
	if settings['HMM_library'] == 'GHMM':
		m = remove_silent_states(m)	
	return m 

"""
Test a gesture given:
	- gesture(s)
	- HM models
	- label(s) of a gesture
"""
def test_gesture(gestures, HMMs) :
	sigma = IntegerRange(0,settings['codebook_size'])
	results = []
	ground = []
	for label, gesture in enumerate(gestures):
		prediction=[]
		
		for HMM in HMMs:
			# gesture[0] is the sequence, gesture[1] is the label

			test_seq = EmissionSequence(sigma, gesture[0]) 
			v = HMM.viterbi(test_seq) 
			prediction.append(v[1])
			
		ground.append(gesture[1])
		results.append(prediction.index(max(prediction)))
	
	if settings['logging'] :
		with open('run.log', 'aw+') as logger :
			logger.write("========= Confusion Matrix ========= \n");
			logger.write(str(confusion_matrix(ground, results, [0, 1])) + "\n")

def init_HMM () :
	# HMM states number Q
	Q = settings['HMM_states']
	# Observation states number Y
	Y = settings['codebook_size']

	# A, B alphabets
	A_alpha = IntegerRange(0,Q)
	B_alpha = IntegerRange(0,Y)

	# Transition probabilities matrix A
	# 		Q0 Q1 .. Qq-1
	#	Q0
	#	Q1
	# 	.
	#	Qq-1
	# Probability of observation given state matrix B
	# 		Q0 Q1 .. Qq-1
	#	Y0
	#	Y1
	# 	.
	#	Yq-1

	A = [[0.0]* Q for _ in range(Q)]

	# Probability of observation given state --> initially uniform distribution
	init_obs_prob = 1.0 / Q
	B = [[init_obs_prob]* Q for _ in range(Y)]

	# Initial probability of states is 0 except for the first state
	pi = [1.0/Q]* Q
	#pi[0] = 1.0

	if settings['HMM_type'] == 'left_to_right' :
		# possible transitions from the ith state to other states (to self, [to HMM_step states])
		poss_trans = 1 + settings['HMM_step']
		init_stat_prob = 1.0 / poss_trans
		
		# :TODO: make this generic to any step
		for i in range (Q):
			if i == Q - 1:
				A[i][i] = 1.0
			else:	
				A[i][i] = init_stat_prob
			if i != Q - 1:
				A[i][i+1] = init_stat_prob
		

	return [B_alpha, A, B, pi]

"""
There are situations in which the HMM to be learned includes "silent states", which do
not emit a letter.
GHMM doesn't handle silent letters 
"""
def remove_silent_states (m):

	return m