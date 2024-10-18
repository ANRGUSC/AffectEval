import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_score, ShuffleSplit, train_test_split
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.svm import SVC
from sklearn.utils.validation import check_is_fitted


class Estimator(BaseEstimator):

    def __init__(
            self, mode,
            model=None, cv=None, name="Estimator", 
            run_method=None, verbose=True
        ):
        """
        Constructor method for the classification layer.
        Parameters
        --------------------
        :param model: An unfitted estimator. Defaults to sklearn's SVC
        :type model: sklearn classifier

        :param labels: Labels OR path to file containing labels.
        :type labels: pandas.DataFrame OR string (file path)

        :param label_generator_method: Specifier for the type of label to generate. 

        :type label_generator_method: str (for default methods, can be "subject", "phase")
            callable (for custom label generation from a file specified by the labels parameter)

        :param mode: Integer indicating what mode to run the estimator.
            0 - Train only
            1 - Test only
            2 - Train and test
        :type mode: int

        :param name: Name of the instantiated object. Defaults to "SVC"
        :type name: str
        """

        if name is None:
            name = "Estimator"

        self._name = name
        self._mode = mode

        if model is not None:
            self._model = model
        else:
            self._model = SVC()
        if cv is not None:
            self._cv = cv
        else:
            self._cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
        
        self._input_type = None
        self._output_type = None

        self._x = None
        self._y = None
        self._feature_names = None
        self._selected_features = None

        if run_method is None:
            if self._mode == 0:
                run_method = self.train
            elif self._mode == 1:
                run_method = self.test
            else:
                run_method = self.train_val_test
        self._run_method = run_method

        self._random_seed = None

    def read_labels(self, labels):
        pass

    def run(self, data):
        """
        Parameters
        --------------------
        :param data: List of [x, y, feature names, selected features] passed from the feature selection layer.
        :type data: list
        Returns 
        --------------------
        If mode=0, returns: [x, y, feature names, selected features, fitted model]
        If mode=1, returns: [fitted model, y_true, y_pred]
        If mode=2, returns: [fitted model, y_true, y_pred]
        """
        self._x = data[0]
        self._y = data[1]
        self._feature_names = data[2]
        self._selected_features = data[3]
        x_selected = self._x[self._selected_features]

        return self._run_method(x_selected, self._y)

    def set_random_seed(self, random_seed):
        self._random_seed = random_seed

    def train(self, x, y):
        """
        Returns 
        --------------------
        Returns [x, y, feature names, selected features, fitted model].
        """
        self._model.fit(x, y)
        return [x, y, self._feature_names, self._selected_features, self._model]

    def test(self, x, y_true):
        """
        Returns 
        --------------------
        Returns [fitted model, y_true, y_pred].
        """
        try:
            check_is_fitted(self._model)    # This requires that any model passed in must be compatible with sklearn (define __sklearn_is_fitted__ method returning a boolean)
            y_pred = self._model.predict(x)
        except Exception:
            print("Model has not been fitted. Returning unfitted model and NaN predictions.")
            y_pred = np.full(y_true.shape, np.nan)
        return [self._model, y_true, y_pred]

    def train_val_test(self, x, y):
        # TODO: Make test set size a parameter
        """
        Splits 
        Returns 
        --------------------
        Returns [fitted model, y_true, y_pred].
        """
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2
        )
        scores = cross_val_score(self._model, x_train, y_train, cv=self._cv)
        print(f"Cross-validation scores: {scores}")
        self._model.fit(x_train, y_train)

        y_pred = self._model.predict(x_test)
        return [self._model, y_test, y_pred]



    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type