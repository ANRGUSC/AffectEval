import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.svm import SVC


class Estimator(BaseEstimator):

    def __init__(self, labels, mode, model=None, name="Estimator", run_method=None, scoring_method=None):
        """

        Parameters
        --------------------
        :param model: An unfitted estimator. Defaults to sklearn's SVC
        :type model: sklearn classifier

        :param x: Features on which to perform feature selection
        :type x: pandas.DataFrame

        :param y: Data labels
        :type y: pandas.DataFrame

        :param mode: Integer indicating what mode to run the estimator.
            0 - Train only
            1 - Test only
        :type mode: int

        :param name: Name of the instantiated object. Defaults to "SVC"
        :type name: str
        """

        if name is None:
            name = "Estimator"

        self._name = name
        self._labels = labels
        self._mode = mode
        if model is not None:
            self._model = model
        else:
            self._model = SVC()
        
        self._input_type = None
        self._output_type = None

        if run_method is None:
            if self._mode == 0:
                run_method = self.train
            else:
                run_method = self.test
        self._run_method = run_method

        if scoring_method is None:
            scoring_method = accuracy_score
        self._scoring_method = scoring_method

        self._random_seed = None

    def run(self, data):
        """
        Parameters
        --------------------
        :param data: List of [x, y, feature names, selected features] passed from the feature selection layer.
        :type data: list
        Returns 
        --------------------
        Fitted estimator if mode=0, predicted labels if mode=1.
        """
        x = data[0]
        y = data[1]
        feature_names = data[2]
        selected_features = data[3]
        x_selected = x[selected_features]

        return self._run_method(x_selected, y)

    def set_random_seed(self, random_seed):
        self._random_seed = random_seed

    def train(self, x, y):
        """
        Returns a fitted model
        """
        self._model.fit(x, y)

    def test(self, x, y):
        y_pred = self._model.predict(x)
        score = self._scoring_method(y, y_pred)
        return [y_pred, score]

    def train_val_test(self, x, y):
        pass

    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type