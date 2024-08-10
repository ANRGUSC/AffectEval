import numpy as np
import pandas as pd

from sklearn.feature_selection import SequentialFeatureSelector
from care_for_me.feature_selector.base_feature_selector import BaseFeatureSelector


class FeatureSelector(BaseFeatureSelector):

    def __init__(self, model, features, labels, name=None, feature_selector=None, num_features=None, mask_subject=True):
        """
        Constructor

        Parameters
        --------------------
        :param model: An unfitted estimator
        :type model: sklearn classifier

        :param features: Features on which to perform feature selection
        :type features: 

        :param labels: Data labels

        :param name: Name of the instantiated object. Defaults to "Feature Selector"
        :type name: str

        :param feature_selector: Feature selection method to use. 
        :type feature_selector: 
        """
        if name is None:
            name = "Feature Selector"

        self._name = name
        self._model = model
        self._features = features
        self._labels = labels
        self._mask_subject = mask_subject
        self._input_type = None
        self._output_type = np.ndarray

        if num_features is None:
            num_features = 3
        self._num_features = num_features

        if feature_selector is not None:
                self._feature_selector = feature_selector
        else:
            # Default feature selection method
            self._feature_selector = SequentialFeatureSelector(self._model, n_features_to_select=self._num_features)

        self._selected_features = {}

    def run(self, features):
        sfs = self._feature_selector.fit(features, self._labels)
        print(sfs.get_feature_names_out())
    
    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type