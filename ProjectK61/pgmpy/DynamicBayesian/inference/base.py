from pgmpy.models import DynamicBayesianNetwork
from pgmpy.utils import StateNameInit
from collections import defaultdict

class Inference(object):
    @StateNameInit()
    def __init__(self, model):
        self.model = model
        model.check_model()

        self.variables = model.get_slice_nodes(0) + model.get_slice_nodes(1)

        if not isinstance(model, DynamicBayesianNetwork):
            raise TypeError("model must be a Dynamic Bayesian Network")

        self.cardinality = {}
        self.factors = defaultdict(list)

        for node in list(model.get_slice_nodes() + model.get_slice_nodes(1)):
            cpd = model.get_cpds(node)
            cpd_as_factor = cpd.to_factor()
            self.cardinality[node] = cpd.variable_card

            for var in cpd.variables:
                self.factors[var].append(cpd_as_factor)

