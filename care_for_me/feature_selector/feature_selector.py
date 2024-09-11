import numpy as np
import pandas as pd

from sklearn.feature_selection import SequentialFeatureSelector
from care_for_me.feature_selector.base_feature_selector import BaseFeatureSelector


# TODO: Add parameter to control whether or not to use subject ID as a feature.
class FeatureSelector(BaseFeatureSelector):

    def __init__(self, model, feature_names, labels, name=None, feature_selector=None, num_features=None, mask_subject=True, verbose=True):
        """
        Constructor method for the feature selection layer.
        Parameters
        --------------------
        :param model: An unfitted estimator
        :type model: sklearn classifier

        :param features: Features on which to perform feature selection
        :type features: pandas.DataFrame

        :param labels: Data labels

        :param name: Name of the instantiated object. Defaults to "Feature Selector"
        :type name: str

        :param feature_selector: Feature selection object to use; must have fit() and get_feature_names_out() defined. 
            Defaults to sklearn's SequentialFeatureSelector
        :type feature_selector: Feature selection object
        """
        if name is None:
            name = "Feature Selector"

        self._name = name
        self._model = model
        self._feature_names = feature_names
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
        self._verbose = verbose

        self._selected_features = {}

    def run(self, data):
        """
        Parameters
        --------------------
        Returns 
        --------------------
        A list containing a DataFrame of features (training samples), feature names, training data labels, and names of selected features
        One-hot encoding is performed on categorical features.
        """
        features = data[0]
        # One-hot encoding if necessary
        # *Q*: Subject IDs are currently treated as numerical features -- change to categorical features?
        col_types = features.dtypes
        print(features)
        if col_types["subject"] == object:
            features["subject"] = pd.to_numeric(features["subject"])
        features = pd.get_dummies(features)
        print(features)
        sfs = self._feature_selector.fit(features, self._labels)
        selected = sfs.get_feature_names_out()
        return [features, self._labels, self._feature_names, selected]
    
    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type