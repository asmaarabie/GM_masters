
"""
Testing LB Algorithm
presentation:
https://docs.google.com/presentation/d/1gt-QapUMGKrRzYPIrpP5XNZDTSh9frIauYR34vcP-wo/edit#slide=id.gf7b53e11e_0_5
"""
from LBData import * 

def find_B_P_W_hat (P,BP, Q, T):
	Phat = [0 for j in range(0,T)]
	BPhat = [0 for i in range(0,T)]
	What = [0 for i in range(0,T)]

	max_t = 0 
	max_q = 0
	max_prob = 0 
	for t in range(0,T):
		for q in range(0,Q):
			if P[t][q] > max_prob:
				max_q = q
				max_t = t
				max_prob = P[t][q]
		Phat[t] = max_prob
		BPhat[t] = BP[t][max_q]
		What = max_q
	return [Phat, BPhat, What, max_t]

for q, model in enumerate(hmms):
	for t,o in enumerate(O):
		if t == 0:
			d[q][t][0] = B[model][0][o-1]
			continue
		for j in range(0,N):
			trans = []
			for i in range(0,N):
				trans.append(d[q][t-1][i] * A[model][i][j])
			# o is the observation at time t (observations are 1-base index)

			d[q][t][j] = max(trans)*B[model][j][o-1] 
		
		P[1][t][q] = d[q][t][N-1]

Phat[1], BPhat[1], W[1], max_t= find_B_P_W_hat (P[1],BP[1], len(hmms), len(O))

print "Phat\n" + str(Phat[1])
print "BP\n" + str(BP[1])
print "W\n" + str(W[1])
print "max_t\n" + str(max_t)