import numpy as np
import pandas as pd

from tqdm import tqdm
from care_for_me.label_generator.base_label_generator import BaseLabelGenerator
from care_for_me import tools


class LabelGenerator(BaseLabelGenerator):

    def __init__(self, label_generation_method, labels_folder=None, drop_subject=False, drop_phase=False, name=None):
        """
        Constructor method for the label generation layer.
        Parameters
        --------------------
        :param label_generation_method: Can be either "subject", "phase", or a callable method for label generation.
            Defaults to the class method provided.
            If a callable is provided, it should return aa pandas DataFrame
        :type feature_extraction_methods: str or callable

        :param name: Name of the instantiated object. Defaults to "Label Generator".
        :type name: str
        """
        if name is None:
            self._name = "Label Generator"
        
        if label_generation_method == "subject":
            self._label_gen = self.generate_subject_labels
        elif label_generation_method == "phase":
            self._label_gen = self.generate_phase_labels
        else:
            self._label_gen = label_generation_method

        self._labels_folder = labels_folder
        self._drop_subject = drop_subject
        self._drop_phase = drop_phase

        self._input_type = None
        self._output_type = np.ndarray

    def run(self, data):
        data = data[0]
        labels, data = self._label_gen(data)

        if self._drop_subject and "subject" in labels.columns:
            data = data.drop("subject", axis=1)
        
        if self._drop_phase and "Phase" in labels.columns:
            data = data.drop("Phase", axis=1)

        col_types = data.dtypes
        if "subject" in data.columns and col_types["subject"] == object:
            data["subject"] = pd.to_numeric(data["subject"])
        
        feature_names = list(data.columns)[2:]
        return [data, labels, feature_names]
    
    def generate_subject_labels(self, data):
        """
        Generates labels according to subject IDs. Removes subject ID from feature set.
        """
        labels = data["subject"]
        data = data.drop("subject", axis=1)
        return labels, data

    def generate_phase_labels(self, data):
        labels = data["Phase"]
        data = data.drop("Phase", axis=1)
        return labels, data

    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type