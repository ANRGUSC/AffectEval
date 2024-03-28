import numpy as np
import pandas as pd
import random

import biosppy as bp
import heartpy as hp

from signal_preprocessor.base_signal_preprocessor import BaseSignalPreprocessor


class SignalPreprocessor(BaseSignalPreprocessor):
    
    def __init__(self, preprocessing_methods=None):
        self._processed_data = pd.DataFrame()
        if preprocessing_methods is not None:
                self._preprocessing_methods = preprocessing_methods
        else:
            # Default preprocessing methods
            self._preprocessing_methods = {
                "ECG": self.preprocess_ecg,
                "EDA": self.preprocess_eda
            }

    def save_to_file(self, file_path):
        pass

    def read_from_file(file_path):
        file_type = file_path[-3:]
        if file_type not in ["csv", "json"]:
            print(f"File type {file_type} is not supported.")

        with open(file_path) as f:
            if file_type == "csv":
                data = pd.read_csv(file_path)
            elif file_type == "json":
                data = pd.read_json(file_path)
        
        # Add data to self._processed_data DataFrame accordingly
                
    def run(self, data):
        """
        data: pd.DataFrame of raw signals 
        """
        signal_types = list(data.columns)
        for signal_type in signal_types:
            method = self._preprocessing_methods[signal_type]
            signal = data.loc[:, signal_type]
            processed = method(signal)
            self._processed_data[signal_type] = processed
                
    def preprocess_ecg(self):
        print("Preprocessing ECG...")

    def preprocess_eda(self):
        print("Preprocessing EDA...")

    @property
    def data(self):
        return self._processed_data