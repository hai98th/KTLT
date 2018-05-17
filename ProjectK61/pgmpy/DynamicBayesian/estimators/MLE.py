# coding:utf-8

import numpy as np

from pgmpy.DynamicBayesian.estimators.base import ParameterEstimator
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import DynamicBayesianNetwork


class MaximumLikelihoodEstimator(ParameterEstimator):
    def __init__(self, model, data, **kwargs):
        if not isinstance(model, DynamicBayesianNetwork):
            raise NotImplementedError("Maximum Likelihood Estimate is only implemented for BayesianModel")

        super(MaximumLikelihoodEstimator, self).__init__(model, data, **kwargs)

    def get_parameters(self):
        parameters = []

        for node in sorted(self.model.nodes()):
            cpd = self.estimate_cpd(node)
            parameters.append(cpd)

        return parameters

    def estimate_cpd(self, node):
        state_counts = self.state_counts(node)
        state_counts.ix[:, (state_counts == 0).all()] = 1

        parents = sorted(self.model.get_parents(node))
        parents_cardinalities = [len(self.state_names[parent]) for parent in parents]
        node_cardinality = len(self.state_names[node])

        cpd = TabularCPD(node, node_cardinality, np.array(state_counts),
                         evidence=parents,
                         evidence_card=parents_cardinalities,
                         state_names=self.state_names)
        cpd.normalize()
        return cpd
