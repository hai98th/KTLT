geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
target = "Chao cac ban"

import random
import datetime
import matplotlib.pyplot as plt
def initialize_chromosomes(length):
    chromosomes = []
    while len(chromosomes) < length:
        sampleSize = min(length - len(chromosomes), len(geneSet))
        chromosomes.extend(random.sample(geneSet, sampleSize))
    return ''.join(chromosomes)
def error_function(chromosome):
    return len(target) - sum(1 for expected, actual \
                             in zip(target, chromosome)  \
                             if expected == actual)
def mutate(parent):
    index = random.randrange(0, len(parent))
    childGenes = list(parent)
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate \
    if newGene == childGenes[index] \
    else newGene
    return ''.join(childGenes)

def display(guess):
    timeDiff = (datetime.datetime.now() - startTime)
    fitness = error_function(guess)
    print("{0}\t{1}\t{2}".format(guess, fitness, str(timeDiff)))
    return fitness, timeDiff
error = []
times = []
random.seed(1)
startTime = datetime.datetime.now()
bestParent = initialize_chromosomes(len(target))
bestFitness = error_function(bestParent)
display(bestParent)
while True:
    child = mutate(bestParent)
    childFitness = error_function(child)

    if bestFitness < childFitness:
        continue
    fitness, timeDiff =  display(child)
    error.append(fitness)
    times.append(str(timeDiff))
    if childFitness == 0:
        break
    bestFitness = childFitness
    bestParent = child


plt.plot(times, error)
plt.title("Error")
plt.xlabel("time")
plt.ylabel("error")
plt.show()
