from pgmpy.utils import StateNameDecorator
from pgmpy.factors.discrete import factor_product
from pgmpy.DynamicBayesian.inference import Inference
import itertools

class DBNInferenceRewritten(Inference):

    @StateNameDecorator(argument='evidence', return_val=None)
    def _variable_elimination(self, variables, operation, evidence=None, elimination_order=None):
        # Dealing with the case when variables is not provided.
        if not variables:
            all_factors = []
            for factor_li in self.factors.values():
                all_factors.extend(factor_li)
            return set(all_factors)

        eliminated_variables = set()
        working_factors = {node: {factor for factor in self.factors[node]}
                           for node in self.factors}

        # Dealing with evidence. Reducing factors over it before VE is run.
        if evidence:
            for evidence_var in evidence:
                for factor in working_factors[evidence_var]:
                    factor_reduced = factor.reduce([(evidence_var, evidence[evidence_var])], inplace=False)
                    for var in factor_reduced.scope():
                        working_factors[var].remove(factor)
                        working_factors[var].add(factor_reduced)
                del working_factors[evidence_var]

        # TODO: Modify it to find the optimal elimination order
        if not elimination_order:
            elimination_order = list(set(self.variables) -
                                     set(variables) -
                                     set(evidence.keys() if evidence else []))

        elif any(var in elimination_order for var in
                 set(variables).union(set(evidence.keys() if evidence else []))):
            raise ValueError("Elimination order contains variables which are in"
                             " variables or evidence args")

        for var in elimination_order:
            # Removing all the factors containing the variables which are
            # eliminated (as all the factors should be considered only once)
            factors = [factor for factor in working_factors[var]
                       if not set(factor.variables).intersection(eliminated_variables)]
            phi = factor_product(*factors)
            phi = getattr(phi, operation)([var], inplace=False)
            del working_factors[var]
            for variable in phi.variables:
                working_factors[variable].add(phi)
            eliminated_variables.add(var)

        final_distribution = set()
        for node in working_factors:
            factors = working_factors[node]
            for factor in factors:
                if not set(factor.variables).intersection(eliminated_variables):
                    final_distribution.add(factor)

        query_var_factor = {}
        for query_var in variables:
            phi = factor_product(*final_distribution)
            query_var_factor[query_var] = phi.marginalize(list(set(variables) -
                                                               set([query_var])),
                                                          inplace=False).normalize(inplace=False)

        return query_var_factor

    def query(self, variables, evidence=None, elimination_order=None):
        return self._variable_elimination(variables, 'marginalize',
                                          evidence=evidence, elimination_order=elimination_order)