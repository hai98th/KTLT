import numpy as np
import matplotlib.pyplot as plt

X = np.array([float(line.split(',')[0]) for line in open('ex1data1.txt').read().strip().split('\n')])
Y = np.array([float(line.split(',')[1]) for line in open('ex1data1.txt').read().strip().split('\n')])



def evaluate(genotype):

    w, b = ... *genotype
    return (Y - X * w - b)**2
plt.scatter(X, Y)
plt.show()