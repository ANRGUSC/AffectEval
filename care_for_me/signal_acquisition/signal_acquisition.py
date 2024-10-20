import glob
import numpy as np
import os
import pandas as pd

from care_for_me.signal_acquisition.base_signal_acquisition import BaseSignalAcquisition


class SignalAcquisition(BaseSignalAcquisition):

    def __init__(self, signal_types, source_folder, labels=None, name=None):
        """
        Constructor method for the signal acquisition layer.
        Parameters
        --------------------
        :param source_folder: Absolute path to folder containing (possibly) subfolders and .csv and/or .json files of raw signals.
            Must follow the structure described in the ReadME file.
        :type source_folder: str
        :param signal_types: List of signal types to read in. Must match signal types listed in signals.py
        :type signal_type: str
        :param name: Name of the signal acquisition layer.
        :type name: str
        :param labels: Generates labels depending on passed value. Can be 'phase', 'subject', or the absolute path to a .csv file of annotations.
        :type labels: str
        """
        if name is None:
            name = "Signal Acquisition"
        self._name = name

        if source_folder is not None:
            self._database = self.read_from_source_folder(source_folder, signal_types)

        self._input_type = None
        self._output_type = dict

    def save_to_file(self):
        pass

    def read_from_source_folder(self, source_folder, signal_types):
        """
        Reads all .csv and .json files from the source folder recursively. Files in the same folder will 
        be grouped together in one list.

        Parameters
        --------------------
        :param source_folder: Absolute path to folder containing (possibly) subfolders and .csv and/or .json files of raw signals.
            Must follow the structure described in the ReadME file.
        :type source_folder: str
        :param signal_types: List of signal types to read in. Must be a valid type listed in signals.py
        :type signal_type: str
        :return: A dictionary of lists of pd.DataFrames
        """
        data_files = self._get_data_files(source_folder, signal_types)
        # Need to distinguish between different participants
        data = {}
        for subject in list(data_files.keys()):
            data[subject] = []
            phases = set(["_".join(f.split("_")[1:-1]) for f in data_files[subject]])
            for phase in phases:
                sublist = [f for f in data_files[subject] if phase in f]
                for f in sublist:
                    df = self.read_from_file(f)
                    df.insert(1, "Phase", phase)
                    data[subject].append(df)
        return data
    
    def _get_data_files(self, source_folder, signal_types):
        files_dict = {}
        dir_list = [os.path.join(source_folder, f) for f in os.listdir(source_folder)]  # Lists all files and subdirectories
        for p in dir_list:
            if os.path.isdir(p):
                files_p = os.listdir(p)
                s = files_p[0].split("_")[0]  # Get subject index from file
                files_p = [os.path.join(p, f) for f in files_p if any(signal in f for signal in signal_types)]
                files_dict[s] = files_p  # Add list of all files in subdirectory p
            else:
                print(f"Path {p} corresponds to a file, expecting a subdirectory.")
        return files_dict

    def read_from_file(self, file_path):
        """
        Reads signals from a CSV or JSON file into a pandas DataFrame. 
        Parameters
        --------------------
        file_path: str
            Absolute path to data file
        Returns
        --------------------
        pd.DataFrame
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
                
    def run(self, data):
        """
        Returns
        --------------------
        dict of {subject_index: list of pd.DataFrames}
            Keys correspond to subject indices.
            Values are lists of pd.DataFrames, where each DataFrame contains the 
            timestamp, data, and label (if applicable) for one signal.
        """
        return [self._database]
    
    def add_to_database(self, data):
        self._database.append(data)

    @property
    def database(self):
        return self._database

    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type