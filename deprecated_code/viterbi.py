
def viterbi (A,B,Pi, O, S, Os):
	vpathlen = len(Os)
	
	max_p = 0
	x = ''
	v = []
	for state in Pi:
		v1 = B[state][Os[0]] * Pi[state]
		if v1 > max_p:
			x = state
			max_p = v1
	v.append([x, max_p])
	
	for i, o in enumerate(Os):
		if i == 0 : continue; 
		max_p = 0
		x = ''
		for s in S:
			x = v[i-1][0]
			print str (i) + " " + str(s) + " " + str(o) + " " + str (x)
		
			current_v = B[s][o] * A[x][s] * v[i-1][1]
			print "v " + str (current_v)
			if current_v > max_p:
				max_p =current_v
				x = s
		v.append([x, max_p])
	print v 


# Example

S = ('Healthy', 'Fever')
O = ('normal', 'cold', 'dizzy')
 
Pi = {'Healthy': 0.6, 'Fever': 0.4}
 
A = {
'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
}

B  = {
'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
}

Os = ('normal', 'cold', 'dizzy')

viterbi(A,B,Pi, O, S, Os)