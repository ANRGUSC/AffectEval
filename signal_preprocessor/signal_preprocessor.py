import numpy as np
import pandas as pd
import random

import biosppy as bp
import heartpy as hp
import samplerate
import scipy

from signal_preprocessor.base_signal_preprocessor import BaseSignalPreprocessor


class SignalPreprocessor(BaseSignalPreprocessor):
    """
    A class for preprocessing raw signals.
    """
    
    def __init__(self, preprocessing_methods=None, name=None):
        """
        Parameters
        --------------------
        preprocessing_methods: dict
            A dictionary in which keys represent the type of input signal (e.g., BVP, ECG, EDA) and values are 
            the corresponding preprocessing methods. Signal types must be listed in signals.Signals. Defaults to 
            the class methods below.
        name: str
            Name of the instantiated object. Defaults to "Signal Preprocessor"
        """

        if name is None:
            name = "Signal Preprocessor"
        self._name = name
        self._input_type = None
        self._output_type = np.ndarray
        
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
        Parameters
        --------------------
        data: dict of {subject_index: list of pd.DataFrames}
            Keys correspond to subject indices.
            Values are lists of pd.DataFrames, where each DataFrame contains the timestamp and raw data for one signal.

        Returns 
        --------------------
        dict of {subject_index: pd.DataFrame}
            Signal DataFrames in each sublist are resampled, processed separately, and then combined into one DataFrame.
        """
        sampling_rates = []
        # Find lowest sampling rate 
        for key in list(data.keys()):
            data_list = data[key]
            for signal in data_list:
                # Infer sample rate from timestamp
                sampling_rates.append(self._get_sampling_rate(signal))
        min_sampling_rate = min(sampling_rates)
        
        for key in list(data.keys()):
            data_list = data[key]
            processed_df = {}
            for signal in data_list:
                signal_type = signal.columns[1]
                sampling_rate = self._get_sampling_rate(signal)
                resampled_signal = samplerate.resample(signal.iloc[:, -1], min_sampling_rate/sampling_rate) # type: np.ndarray
                try:
                    method = self._preprocessing_methods[signal_type]
                    processed = method(resampled_signal, min_sampling_rate)
                except Exception as e:
                    raise(e)
                    print(f"Error processing {signal_type}. Returning resampled signal.")
                    processed = resampled_signal
                processed_df[signal_type] = processed
            processed_df = pd.DataFrame(processed_df)
            # Add updated timestamp column
            timestamp = [min_sampling_rate*i for i in range(processed_df.shape[0])]
            processed_df.insert(0, "timestamp", timestamp)
            self._processed_data[key] = processed_df
        return self._processed_data
    
    def align_signals(self, data):
        # May refactor run() so that signals are first aligned and combined into one DataFrame before processing.
        """
        Align signals given in data. Infers sampling rates of different signals based on the timestamp column of each signal DataFrame.  
        Downsamples signals if necessary to match the lowest sampling rate present in the collection of signals.
        Parameters
        --------------------
        data: pd.DataFrame of raw signals 
        """
        pass
                
    def preprocess_ecg(self, signal, sampling_rate):
        _, filtered_signal, _, _, _, _, _ = bp.signals.ecg.ecg(signal=signal, sampling_rate=sampling_rate, show=False)
        return filtered_signal

    def preprocess_eda(self, signal, sampling_rate):
        filtered_signal = scipy.ndimage.median_filter(signal, int(sampling_rate))
        # _, filtered_signal, _, _, _ = bp.signals.eda.eda(signal=signal, sampling_rate=fs, show=False, min_amplitude=0.01)
        return filtered_signal
    
    def preprocess_temp(self, signal, sampling_rate):
        return signal

    def add_preprocessing_method(self, signal_type, method):
        self._preprocessing_methods[signal_type] = method

    def _get_sampling_rate(self, signal):
        try:
            if type(signal) is pd.DataFrame:
                timestamp = signal.iloc[:, 0]
            elif type(signal) is np.ndarray:
                timestamp = signal[:, 0]
            delta = timestamp[1] - timestamp[0]
            return 1/delta
        except Exception:
            pass

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