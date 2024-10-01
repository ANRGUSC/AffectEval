import numpy as np
import pandas as pd

from tqdm import tqdm
from care_for_me.label_generator.base_label_generator import BaseLabelGenerator
from care_for_me import tools


class LabelGenerator(BaseLabelGenerator):

    def __init__(self, label_generation_method, name=None):
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
            name = "Label Generator"
            
        self._input_type = None
        self._output_type = np.ndarray

    def run(self, data):
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