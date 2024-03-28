import numpy as np
import pandas as pd

from base_signal_acquisition import BaseSignalAcquisition


class SignalAcquisition(BaseSignalAcquisition):
    
    def __init__(self):
        self._data = pd.DataFrame()

    def save_to_file(self):
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
        
        # Add data to self._data DataFrame accordingly
                
    def run(self):
        pass

    @property
    def data(self):
        return self._data