import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.svm import SVC
from sklearn.utils.validation import check_is_fitted

from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import f1_score


class Estimator(BaseEstimator):

    def __init__(
            self, mode,
            models=None, cv=None, name="Estimator", 
            run_method=None, verbose=True, random_seed=None
        ):
        """
        Constructor method for the classification layer.
        Parameters
        --------------------
        :param mode: Integer indicating what mode to run the estimator.
            0 - Train only
            1 - Test only
            2 - Train and test
        :type mode: int

        :param model: An unfitted estimator. Defaults to sklearn's SVC
        :type model: sklearn classifier

        :param cv: Cross-validation method to use. Defaults to StratifiedKFold with n_splits = 5.
        :type cv: Any cross-validation method compatible with sklearn's cross_val_score
            - int to specify the number of folds for StratifiedKFold
            - CV splitter
            - iterable that generates(train, test) splits as arrays of indices

        :param name: Name of the instantiated object. Defaults to "SVC"
        :type name: str
        """

        if name is None:
            name = "Estimator"

        self._name = name
        self._mode = mode

        if models is not None:
            self._models = models
        else:
            self._models = {"SVM": SVC()}
        if cv is not None:
            self._cv = cv
        else:
            self._cv = StratifiedKFold(n_splits=5)
        
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
        self._groups = None

        self.set_random_seed(random_seed)

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

        # Drop NaN rows
        nan_rows = self._x[self._x.isna().any(axis=1)].index
        x_selected = self._x.drop(nan_rows)
        self._y = np.delete(self._y, nan_rows, axis=0)

        self._groups = x_selected.loc[:, "subject"]
        self._feature_names = data[2]
        if len(data) == 4:
            self._selected_features = data[3]
        else:
            self._selected_features = data[2]
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
        for model_name in self._models.keys():
            model = self._models[model_name]
            model.fit(x, y)
        return [x, y, self._feature_names, self._selected_features, self._models]

    def test(self, x, y_true):
        """
        Returns 
        --------------------
        Returns [fitted model, y_true, y_pred].
        """
        y_preds = []
        for model_name in self._models.keys():
            model = self._models[model_name]
            try:
                check_is_fitted(model)    # This requires that any model passed in must be compatible with sklearn (define __sklearn_is_fitted__ method returning a boolean)
                y_pred = model.predict(x)
                y_preds.append(y_pred)
            except Exception:
                print("Model has not been fitted. Returning unfitted model and NaN predictions.")
                y_pred = np.full(y_true.shape, np.nan)
                y_preds.append(y_pred)
        return [self._models, y_true, y_preds]

    def train_val_test(self, x, y):
        # TODO: Make test set size a parameter
        """
        Splits the input data into train and test sets. Default test split: 0.2
        Returns 
        --------------------
        Returns [fitted model, y_true, y_pred].
        """
        y_preds = {}
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=self._random_seed
        )
        for model_name in self._models.keys():
            print(f"{model_name} " + "-"*50)
            model = self._models[model_name]
            acc = cross_val_score(model, x_train, y_train, cv=self._cv, scoring="accuracy")
            print(f"Cross-validation acc: {acc}")
            print(f"Cross-validation mean acc: {np.mean(acc)}")
            print(f"Cross-validation std acc: {np.std(acc)}")
            f1 = cross_val_score(model, x_train, y_train, cv=self._cv, scoring="f1_weighted")
            print(f"Cross-validation f1: {f1}")
            print(f"Cross-validation mean f1: {np.mean(f1)}")
            print(f"Cross-validation std f1: {np.std(f1)}")
            # auc = cross_val_score(model, x_train, y_train, cv=self._cv, scoring="roc_auc")
            # print(f"Cross-validation auc: {auc}")
            # print(f"Cross-validation mean auc: {np.mean(auc)}")
            # print(f"Cross-validation std auc: {np.std(auc)}")

            # f1 = []
            # for train_index, test_index in enumerate(self._cv.split(x_train, y_train)):
            #         x_train_cv, x_test_cv = x_train.iloc[train_index], x_train.iloc[test_index]
            #         y_train_cv, y_test_cv = y_train.iloc[train_index], y_train.iloc[test_index]
            #         clf = clf.fit(x_train_cv, y_train_cv)
            #         y_pred = clf.predict(x_test_cv)
            #         f1.append(f1_score(y_test_cv, y_pred, average="micro"))
            
            # print(f"Cross-validation f1: {f1}")
            # print(f"Cross-validation mean f1: {np.mean(f1)}")
            # print(f"Cross-validation std f1: {np.std(f1)}")

            model.fit(x_train, y_train)

            y_pred = model.predict(x_test)
            y_preds[model_name] = y_pred
        
        return [self._models, y_test, y_preds]



    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type