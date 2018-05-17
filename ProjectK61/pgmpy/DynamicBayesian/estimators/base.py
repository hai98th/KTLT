#!/usr/bin/env python
from warnings import warn

import numpy as np
import pandas as pd
from scipy.stats import chisquare


class BaseEstimator(object):
    def __init__(self, data, state_names=None, complete_samples_only=True):
        self.data = data
        self.complete_samples_only = complete_samples_only

        variables = list(data.columns.values)

        if not isinstance(state_names, dict):
            self.state_names = {var: self._collect_state_names(var) for var in variables}
        else:
            self.state_names = dict()
            for var in variables:
                if var in state_names:
                    if not set(self._collect_state_names(var)) <= set(state_names[var]):
                        raise ValueError("Data contains unexpected states for variable '{0}'.".format(str(var)))
                    self.state_names[var] = sorted(state_names[var])
                else:
                    self.state_names[var] = self._collect_state_names(var)

    def _collect_state_names(self, variable):
        "Return a list of states that the variable takes in the data"
        states = sorted(list(self.data.ix[:, [variable]][variable].dropna().unique()))
        return states

    # The function below was written by Thanh Dat
    def state_counts(self, variable, parents=[], complete_samples_only=None):
        # the different from this function with the function above is variable of type tuple
        # example variable = ('D', 0)
        if complete_samples_only is None:
            complete_samples_only = self.complete_samples_only
        # ignores either any row containing NaN, or only those where the variable or its parents is NaN
        data = self.data.dropna() if complete_samples_only else self.data.dropna(subset=[variable] + parents)

        if not parents:
            # count how often each state of 'variable' occured
            state_count_data = data.ix[:, [variable]][variable].value_counts()
            state_counts = state_count_data.reindex(self.state_names[variable]).fillna(0).to_frame()

        else:
            parents_states = [self.state_names[parent] for parent in parents]
            # count how often each state of 'variable' occured, conditional on parents' states
            state_count_data = data.groupby([variable] + parents).size().unstack(parents)

            # reindex rows & columns to sort them and to add missing ones
            # missing row    = some state of 'variable' did not occur in data
            # missing column = some state configuration of current 'variable's parents
            #                  did not occur in data
            row_index = self.state_names[variable]
            column_index = pd.MultiIndex.from_product(parents_states, names=parents)
            state_counts = state_count_data.reindex(index=row_index, columns=column_index).fillna(0)

        return state_counts



class ParameterEstimator(BaseEstimator):
    def __init__(self, model, data, **kwargs):
        if not set(model.get_slice_nodes(0) + model.get_slice_nodes(1)) <= set(data.columns.values):
            raise ValueError("variable names of the model must be identical to column names in data")
        self.model = model

        super(ParameterEstimator, self).__init__(data, **kwargs)

    def state_counts(self, variable, **kwargs):
        parents = sorted(self.model.get_parents(variable))
        return super(ParameterEstimator, self).state_counts(variable, parents=parents, **kwargs)

    def get_parameters(self):
        pass
