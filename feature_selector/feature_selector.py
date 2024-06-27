import numpy as np
import pandas as pd

from sklearn.feature_selection import SequentialFeatureSelector
from .base_feature_selector import BaseFeatureSelector


class FeatureSelector(BaseFeatureSelector):

    def __init__(self, model, features, labels, feature_selection_method=None, num_features=None, name=None):
        """
        Constructor

        Parameters
        --------------------
        :param model: An unfitted estimator
        :type model: sklearn classifier

        :param features: Features on which to perform feature selection
        :type features: 

        :param labels: Labels 
        """
        if name is None:
            name = "Feature Selector"
        self._name = name
        self._model = model
        self._features = features
        self._labels = labels
        self._input_type = None
        self._output_type = np.ndarray

        if feature_selection_method is not None:
                self._feature_selection_method = feature_selection_method
        else:
            # Default feature selection method
            self._feature_selection_method = SequentialFeatureSelector

        if num_features is None:
            num_features = 3
        self._num_features = num_features
        self._selected_features = {}

    def run(self, features):
        sfs = self._feature_selection_method(self._model, n_features_to_select=self._num_features)
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type