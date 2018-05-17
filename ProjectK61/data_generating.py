import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import math

def truncated_normal_randomly_generate(mu = 15, sigma = 30, size = 1000, DPQ_data = [], C_data = []):
    random_list = []
    for i in range(size):
        mu1 = mu*(C_data[i]+1)*(5-DPQ_data[i])/10
        while (True):
            x = np.random.normal(mu1, sigma)
            if (x >= 0 and x <= 2*mu):
                random_list.append(int(x))
                break
    return np.array(random_list)

def binomial_randomly_generate(n_data = [], p_data = []):
    random_list = []
    for i in range(len(n_data)):
        x = np.random.binomial(n_data[i], (float)(p_data[i]) / 4)
        random_list.append(int(x))
    return np.array(random_list)

def found_probability_generate(n_data = [], p_data = []):
    random_list = []
    for i in range(len(n_data)):
        sigma = 0.001
        if p_data[i] == 0:
            mu = 0.1
        elif p_data[i] == 1:
            mu = 0.3
        elif p_data[i] == 2:
            mu = 0.5
        elif p_data[i] == 3:
            mu = 0.7
        elif p_data[i] == 4:
            mu = 0.9

        p = np.random.normal(mu, sigma)
        if p < 0:
            p = 0
        elif p > 1:
            p = 1

        random_list.append(int(n_data[i] * p))
    return np.array(random_list)

def finding_quality_generate(prior_data = []):
    random_list = []
    for i in range(len(prior_data)):
        x = int(math.ceil(np.random.normal(prior_data[i], 1)))
        if x > 4:
            x = 4
        elif x < 0:
            x = 0
        random_list.append(x)
    return np.array(random_list)


def randomly_int(data = []):
    random_list = [np.random.randint(low = 0, high = i + 1) for i in data]
    return np.array(random_list)

data_size = 10000

data = pd.DataFrame(np.random.randint(low = 0, high = 5, size = (data_size, 4)),
                                    columns = ['TQ','DPQ', 'C', 'OU'])
data['DI'] = truncated_normal_randomly_generate(mu = 15, sigma = 5, size = data_size, DPQ_data = data['DPQ'], C_data = data['C'])
data['DFT'] = found_probability_generate(data['DI'], data['TQ'])
data['RD'] = [a - b for a, b in zip(data['DI'], data['DFT'])]
data['DFO'] = found_probability_generate(data['RD'], data['OU'])

data['DPQ2'] = data['DPQ']
data['C2'] = data['C']
# data['TQ2'] = finding_quality_generate(data['TQ'])
data['TQ2'] = data['TQ']
data['OU2'] = data['OU']
data['DI2'] = data['RD']
data['DFT2'] = found_probability_generate(data['DI2'], data['TQ2'])
data['RD2'] = [a - b for a, b in zip(data['DI2'], data['DFT2'])]
data['DFO2'] = found_probability_generate(data['RD2'], data['OU2'])

data['DPQ3'] = data['DPQ2']
data['C3'] = data['C2']
# data['TQ3'] = finding_quality_generate(data['TQ2'])
data['TQ3'] = data['TQ']
data['OU3'] = data['OU2']
data['DI3'] = data['RD2']
data['DFT3'] = found_probability_generate(data['DI3'], data['TQ3'])
data['RD3'] = [a - b for a, b in zip(data['DI3'], data['DFT3'])]
data['DFO3'] = found_probability_generate(data['RD3'], data['OU3'])

data.to_csv("fisrm10000.csv", index = False)