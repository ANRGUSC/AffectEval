import numpy as np
import pandas as pd

import biosppy as bp
import heartpy as hp

from feature_extractor.base_feature_extractor import BaseFeatureExtractor


class FeatureExtractor(BaseFeatureExtractor):

    def __init__(self):
        self._features = pd.DataFrame()

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
                
    def run(self):
        pass