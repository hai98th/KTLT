# DEAP
import numpy as np
import random

from deap import base
from deap import creator
from deap import tools
creator.create('FitnessMax', base.Fitness, weights=(1, ))
creator.create('Individual', np.ndarray, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register('attr_float', np.random.uniform)
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_float, genom_dimension())
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
    np.save('population/cartpole-v1-hof.npy', hof[0])
    np.save('population/cartpole-v1-ind.npy', pop[0])

    return pop, log, hof
