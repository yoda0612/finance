import numpy as np
def findMax(filename):
    data = []
    with open(filename) as f:
        for line in f.readlines():
            row = line.split(',')
            data.append(row[:len(row) - 1])
    data = np.array(data)
    ind = np.unravel_index(np.argmax(data, axis=None), data.shape)
    return ind

print(findMax("max.csv"))
print(findMax("mean.csv"))
#print(findMax("min.csv"))
