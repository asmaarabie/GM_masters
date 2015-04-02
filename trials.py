#tests
a = [1,2,3]
file_r = [a] * 3
gesture = [file_r] * 3
print gesture

flattened = [reading for g_file in gesture for reading in g_file]

print str(len(flattened))