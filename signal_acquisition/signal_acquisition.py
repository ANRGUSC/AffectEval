import glob
import numpy as np
import os
import pandas as pd

from .base_signal_acquisition import BaseSignalAcquisition


class SignalAcquisition(BaseSignalAcquisition):
    """
    
    """
    
    def __init__(self, source_folder, signal_types, name=None):
        if name is None:
            name = "Signal Acquisition"
        self._name = name
        self._database = self.read_from_source_folder(source_folder, signal_types)

    def save_to_file(self):
        pass

    def read_from_source_folder(self, source_folder, signal_types):
        """
        Reads all .csv and .json files from the source folder recursively. Files in the same folder will 
        be grouped together in one list.

        Parameters
        --------------------
        source_folder: str
            Absolute path to folder containing (possibly) subfolders and .csv aand/or .json files of raw signals.
        """
        data_files = self._get_data_files(source_folder, signal_types)
        # Need to distinguish between different participants
        data = {}
        for key in list(data_files.keys()):
            data[key] = [self.read_from_file(f) for f in data_files[key]]
        return data
    
    def _get_data_files(self, source_folder, signal_types):
        files_dict = {}
        dir_list = [os.path.join(source_folder, f) for f in os.listdir(source_folder)]  # Lists all files and subdirectories
        for p in dir_list:
            if os.path.isdir(p):
                files_p = os.listdir(p)
                key = files_p[0].split("_")[0]  # Get subject index from file
                files_p = [os.path.join(p, f) for f in files_p if any(signal in f for signal in signal_types)]
                files_dict[key] = files_p  # Add list of all files in subdirectory p
            else:
                print(f"Path {p} corresponds to a file, not a subdirectory.")
        return files_dict

    def read_from_file(self, file_path):
        """
        Parameters
        --------------------
        file_path: str
            Absolute path to data file
        """
        file_type = file_path[-3:]
        if file_type not in ["csv", "json"]:
            print(f"File type {file_type} is not supported.")

        with open(file_path) as f:
            if file_type == "csv":
                data = pd.read_csv(file_path, index_col=0)
            elif file_type == "json":
                data = pd.read_json(file_path)
        return data
                
    def run(self, **kwargs):
        """
        Returns
        --------------------
        dict of {subject_index: list of pd.DataFrames}
            Keys correspond to subject indices.
            Values are lists of pd.DataFrames, where each DataFrame contains the timestamp and data for one signal.
        """
        return self._database
    
    def add_to_database(self, data):
        self._database.append(data)

    @property
    def data(self):
        return self._database

    @property
    def name(self):
        return self._name