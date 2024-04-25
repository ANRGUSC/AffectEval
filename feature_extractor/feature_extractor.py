import numpy as np
import pandas as pd

import biosppy as bp
import heartpy as hp

from feature_extractor.base_feature_extractor import BaseFeatureExtractor


class FeatureExtractor(BaseFeatureExtractor):

    def __init__(self, feature_extraction_methods=None, name=None):
        if name is None:
            name = "Feature Extractor"
        self._name = name
        self._features = {}

        if feature_extraction_methods is not None:
                self._feature_extraction_methods = feature_extraction_methods
        else:
            # Default preprocessing methods
            self._feature_extraction_methods = {
                "ECG": {"HR": self.extract_hr, "SDNN": self.extract_sdnn},
                "EDA": {"mean_SCL": self.extract_mean_scl, "SCR_rate": self.extract_scr_rate}
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
        
        # Add data to self._features DataFrame accordingly
                
    def run(self, data):
        """
        Parameters
        --------------------
        data: dict of {subject_index: pd.DataFrame}
            Keys correspond to subject indices.
            Values are pd.DataFrames, where each DataFrame contains columns of the timestamp and processed signals for each subject.

        Returns 
        --------------------
        dict of {subject_index: pd.DataFrame}
            Signal DataFrames in each sublist are resampled, processed separately, and then combined into one DataFrame.
        """
        for key in list(data.keys()):
            df = data[key]
            signal_types = df.columns[1:]
            out = {}
            for signal_type in signal_types:
                signal = df.loc[:, ["timestamp", signal_type]]
                features = list(self._feature_extraction_methods[signal_type].keys())
                for feature in features:
                    method = self._feature_extraction_methods[signal_type][feature]
                    extracted = method(signal)
                    out[feature] = extracted
            out = pd.DataFrame(out)
            self._features[key] = out
        return self._features
    
    def extract_hr(self, signal):
        print("Extracting HR")
        return signal.iloc[:, -1]
    
    def extract_sdnn(self, signal):
        print("Extracting SDNN")
        return signal.iloc[:, -1]

    def extract_mean_scl(self, signal):
        print("Extracting mean SCL")
        return signal.iloc[:, -1]

    def extract_scr_rate(self, signal):
        print("Extracting SCR rate")
        return signal.iloc[:, -1]

    @property
    def name(self):
        return self._name