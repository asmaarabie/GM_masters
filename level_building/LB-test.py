
"""
Testing LB Algorithm
presentation:
https://docs.google.com/presentation/d/1gt-QapUMGKrRzYPIrpP5XNZDTSh9frIauYR34vcP-wo/edit#slide=id.gf7b53e11e_0_5
"""

"""
DP 
Set Min[i] equal to Infinity for all of i
Min[0]=0

For i = 1 to S
For j = 0 to N - 1
   If (Vj<=i AND Min[i-Vj]+1<Min[i])
Then Min[i]=Min[i-Vj]+1

Output Min[S]
"""

from LBData import * 

def init_delta_alpha(level, O, Phat, d, alpha):
	d = [[[0 for k in xrange(N)] for k in xrange(T)] for j in xrange(M)]
 	alpha = [[[0 for k in xrange(N)] for k in xrange(T)] for j in xrange(M)]
	tmax = 0 
	for q, model in enumerate (hmms):
		if level == 0:
				d[q][0][0] = B[model][0][O[0]-1]
		else:
			for t in range (1, len(O)):
				# Appropriate place
				app= d[q][t-1][0] * A[model][0][0]
				d[q][t][0] = max(Phat[level-1][t-1], app) * B[model][0][O[t]-1]
				if Phat[level-1][t-1] > app:
					alpha[q][t][0] = t-1
					tmax = t - 1
				else: 
					alpha[q][t][0] =  alpha[q][t - 1][0]
	return [d, alpha, tmax]

def find_B_P_W_hat (P,BP):
	Phat = [0 for j in range(T)]
	BPhat = [0 for i in range(T)]
	What = [-1 for i in range(T)]

	
	for t in range(0,len(O)):
		max_q = -1
		max_prob = 0
		max_prev = -1
		for q in range(0,M):
			if P[t][q] > max_prob:
				max_q = q
				max_prob = P[t][q]
				max_prev = BP[t][q]
		Phat[t] = max_prob
		BPhat[t] = max_prev
		What[t] = max_q
	return [Phat, BPhat, What]

# Paper: an hmm-based character recognition network using level building
def backtrack (BPhat, W):
	level = L - 1
	back = T -1 
	res = []
	while level >= 0:
		res.append(W[level][back])
		back = BPhat[level][back]
		level = level - 1

	res.reverse()
	print res

def process_level():
	d = [[[0 for k in xrange(N)] for k in xrange(T)] for j in xrange(M)]
 	alpha = [[[0 for k in xrange(N)] for k in xrange(T)] for j in xrange(M)]
	print len(O)

	for l in range (0, L):
		print "Level ==== > " + str (l)
		
		d, alpha, tmax = init_delta_alpha(l, O, Phat,d,alpha)	
		for q, model in enumerate(hmms):

			for t in range(tmax+1, len(O)):
				for j in range(0,N):
					trans = []
					
					"""
					This is a 2-state model
					Since each state at each observation can be reached by (0 to 2)  prev states
					Find the prev state that makes the value at d[t][curr state] max
					"""
					for i in range (max(j-1, 0), j+1):
						trans.append (d[q][t-1][i] * A[model][i][j])
					
					d[q][t][j] = max(trans) *B[model][j][O[t]-1] 

					"""
					Since the trans matrix is of size (0 to 2), to determine which prev state 
					makes the value at d[t][curr state] max, minus the index of max trans from 
					the current state index to get the correct prev state
					"""
					if trans.index(max(trans)) == 1 or j == 0:
						alpha[q][t][j] = alpha[q][t-1][j]
					else: 
						alpha[q][t][j] = alpha[q][t-1][j - 1]	
					

				P[l][t][q] = d[q][t][N-1]
				BP[l][t][q] = alpha[q][t][N-1]
		
		Phat[l], BPhat[l], W[l]= find_B_P_W_hat (P[l],BP[l])
		

		print "Phat\n" + str(Phat[l])
		print "BPhat\n" + str(BPhat[l])
		print "W\n" + str(W[l])
		print "tmax= " + str(tmax) + "\n"
		#print alpha[l]
		# print W[l]
		# #print BP
	backtrack (BPhat, W)	
	

process_level()
