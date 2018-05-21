# DEAP
import os
import numpy as np
import random
from deap import creator, base, tools, algorithms
import matplotlib.pyplot as plt

X = np.array([float(line.split(',')[0]) for line in open('ex1data1.txt').read().strip().split('\n')])
Y = np.array([float(line.split(',')[1]) for line in open('ex1data1.txt').read().strip().split('\n')])


def evaluate(genotype):
    w, b = genotype
    return - np.sum((Y - X * w - b) ** 2),


creator.create('FitnessMax', base.Fitness, weights=(1,))
creator.create('Individual', np.ndarray, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register('attr_float', np.random.uniform)
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_float, 2)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('evaluate', evaluate)
toolbox.register('mate', tools.cxSimulatedBinaryBounded, eta=100, low=0, up=1)
toolbox.register('mutate', tools.mutPolynomialBounded, eta=100, low=0, up=1, indpb=0.01)
toolbox.register('select', tools.selTournament, tournsize=3)


def main():
    os.system('rm population/*')

    np.random.seed(1337)

    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1, similar=np.array_equal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register('avg', np.mean)
    stats.register('std', np.std)
    stats.register('min', np.min)
    stats.register('max', np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.1, ngen=40,
                                   stats=stats, halloffame=hof, verbose=True)
    total_nevals = sum(log.select('nevals'))

    return pop, log, hof


_, _, hof = main()

w, b = hof[0][0], hof[0][1]
_X = np.linspace(min(X), max(X), num=1000)
_Y = _X * w + b

plt.scatter(X, Y)
plt.plot(_X, _Y)
plt.show()
