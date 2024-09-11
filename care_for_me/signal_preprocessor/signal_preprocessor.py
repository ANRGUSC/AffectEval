import numpy as np
import pandas as pd
import random

import biosppy as bp
import heartpy as hp
import neurokit2 as nk
import samplerate
import scipy

from care_for_me.signal_preprocessor.base_signal_preprocessor import BaseSignalPreprocessor
from care_for_me import tools


class SignalPreprocessor(BaseSignalPreprocessor):
    """
    A class for preprocessing raw signals. Handles signal alignment, resampling, and cleaning. 
    """
    
    def __init__(self, preprocessing_methods=None, name=None, skip=True, resample_rate=None):
        """
        Constructor method for the signal preprocessing layer.
        Parameters
        --------------------
        :param preprocessing_methods: A dictionary in which keys represent the type of input signal (e.g., BVP, ECG, EDA) and values are 
            the corresponding preprocessing methods. Signal types must be listed in signals.Signals. 
            Defaults to the class methods provided.
        :type preprocessing_methods: dict

        :param name: Name of the instantiated object. Defaults to "Signal Preprocessor"
        :type name: str

        :param skip: Flag to skip the default signal preprocessing. Defaults to True (default feature extractor methods also perform the same preprocessing steps)
            If preprocessing is skipped, signals are still downsampled if necessary to match the lowest sampling rate 
            present in the collection of signals 
        :type skip: bool

        :param resample_rate: New sampling rate to resample all signals to. Defaults to the lowest sampling rate present in the collection of signals. 
            If the passed value for resample_rate is higher than the lowest sampling rate, the lowest sampling rate will be used instead.
        :type resample_rate: int
        """

        if name is None:
            name = "Signal Preprocessor"
        self._name = name
        self._input_type = None
        self._output_type = np.ndarray
        self._skip = skip
        self._resample_rate = resample_rate
        
        self._processed_data = {}
        if preprocessing_methods is not None:
                self._preprocessing_methods = preprocessing_methods
        else:
            # Default preprocessing methods
            self._preprocessing_methods = {
                "ECG": self.preprocess_ecg,
                "EDA": self.preprocess_eda,
                "TEMP": self.preprocess_temp
            }

    def save_to_file(self, file_path):
        pass

    def read_from_file(file_path):
        file_type = file_path[-3:]
        if file_type not in ["csv", "json"]:
            print(f"File type {file_type} is not supported.")

        with open(file_path) as f:
            if file_type == "csv":
                data = pd.read_csv(file_path, index_col=0)
            elif file_type == "json":
                data = pd.read_json(file_path)
        
        # Add data to self._processed_data DataFrame accordingly
                
    def run(self, data):
        """
        Infers sampling rates of different signals based on the timestamp column of each signal DataFrame.
        Performs preprocessing steps, then downsamples signals if necessary to match the lowest sampling rate 
        present in the collection of signals.

        Parameters
        --------------------
        :param data: dict of {subject_index: list of pd.DataFrames}
            Keys correspond to subject indices.
            Values are lists of pd.DataFrames, where each DataFrame contains the timestamp and raw data for one signal.
        :type data: dict
            
        Returns 
        --------------------
        dict of {subject_index: [pd.DataFrame]}
            Signal DataFrames in each sublist are resampled and processed separately.
        """
        data = data[0]
        sampling_rates = []
        # Find lowest sampling rate 
        for subject in list(data.keys()):
            data_list = data[subject]
            for signal in data_list:
                # Infer sample rate from timestamp
                sampling_rates.append(tools.get_sampling_rate(signal))
        sampling_rates.append(self._resample_rate)
        min_sampling_rate = min(sampling_rates)
        
        for subject in list(data.keys()):
            data_list = data[subject]
            self._processed_data[subject] = []
            for signal in data_list:
                phase = signal["Phase"].iloc[0]
                signal_type = signal.columns[2]
                sampling_rate = tools.get_sampling_rate(signal)
                temp = samplerate.resample(signal.iloc[:, -1], min_sampling_rate/sampling_rate)  # type: np.ndarray
                temp = pd.DataFrame(data=temp, columns=[signal_type])
                if not self.skip:
                    try:
                        method = self._preprocessing_methods[signal_type]
                        temp = method(temp, min_sampling_rate)
                        if type(temp) is pd.Series:    # Necessary because some preprocessing methods convert the np.ndarray to pd.Series
                            temp = temp.to_frame()
                            temp.columns = [signal_type]
                        else:
                            temp = pd.DataFrame(data=temp, columns=[signal_type])
                    except Exception as e:
                        print(f"Error processing {signal_type}. Returning resampled signal.")
                # Add updated timestamp column
                # TODO: Fix timestamp generation. This sets the timestamp of the first sample to 0, which isn't necessarily what we want. 
                timestamp = [1/min_sampling_rate*i for i in range(temp.shape[0])]    
                temp.insert(0, "timestamp", timestamp)
                temp.insert(1, "Phase", phase)
                self._processed_data[subject].append(temp)
        
        # Merge dataframes for each subject
        for subject in self._processed_data.keys():
            dfs = self._processed_data[subject]
            

        return [self._processed_data]
    
    def align_signal_start(self, data):
        # May refactor run() so that signals are first aligned and combined into one DataFrame before processing.
        """
        Align signals given in data based on starting timestamps. 

        Parameters
        --------------------
        data: pd.DataFrame of raw signals 
        """
        pass
                
    def preprocess_ecg(self, signal, sampling_rate):
        signal = hp.scale_data(signal)
        signal = hp.filtering.remove_baseline_wander(signal, sampling_rate)
        signal, info = nk.ecg_process(signal, sampling_rate=int(sampling_rate))
        filtered_signal = signal["ECG_Clean"]

        return filtered_signal

    def preprocess_eda(self, signal, sampling_rate):
        filtered_signal = scipy.ndimage.median_filter(signal, int(sampling_rate))
        # _, filtered_signal, _, _, _ = bp.signals.eda.eda(signal=signal, sampling_rate=fs, show=False, min_amplitude=0.01)
        return filtered_signal
    
    def preprocess_temp(self, signal, sampling_rate):
        return signal

    def add_preprocessing_method(self, signal_type, method):
        self._preprocessing_methods[signal_type] = method

    @property
    def data(self):
        return self._processed_data
    
    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type
    
    @property
    def skip(self):
        return self._skip