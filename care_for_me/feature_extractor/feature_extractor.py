import numpy as np
import pandas as pd

import biosppy as bp
import heartpy as hp
import neurokit2 as nk
import pyhrv.time_domain as td
import scipy

from care_for_me.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from care_for_me import tools


# Sliding window parameters for feature extraction
WINDOW_SIZE_ECG = 60
OVERLAP_ECG = 30

WINDOW_SIZE_EDA = 60
OVERLAP_EDA = 30
MIN_AMP = 0.3  # Minimum threshold by which to exclude SCRs (peaks) as relative to the largest amplitude in the signal (from neurokit documentation)

WINDOW_SIZE_TEMP = 60
OVERLAP_TEMP = 30


# TODO: Add window sizes for different signals as a parameter
class FeatureExtractor(BaseFeatureExtractor):

    def __init__(self, feature_extraction_methods=None, name=None):
        if name is None:
            name = "Feature Extractor"
        self._name = name
        self._features = {}
        self._input_type = None
        self._output_type = np.ndarray

        if feature_extraction_methods is not None:
                self._feature_extraction_methods = feature_extraction_methods
        else:
            # Default preprocessing methods
            self._feature_extraction_methods = {
                "ECG": {"HR": self.extract_hr, "RMSSD": self.extract_rmssd, "SDNN": self.extract_sdnn},
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
            print(out.shape)
            self._features[key] = out
        return self._features
    
    def extract_ecg_features_pyhrv(self, signal):
        """
        Extracts ECG features (heart rate, RMSSD, SDNN) using pyhrv methods
        """
        fs = tools.get_sampling_rate(signal)
        signal = signal.iloc[:, -1]
        
        n = signal.size
        if n == 0:
            print("ECG signal has length 0, returning None")
            return None
        
        hr = []
        rmssd = []
        sdnn = []

        start = 0
        window_size = int(WINDOW_SIZE_ECG*1/fs)
        overlap = int(OVERLAP_ECG*1/fs)
        stop = start + WINDOW_SIZE_ECG

        if stop >= n:
            t, filtered_signal, rpeaks, _, _, _, bpm = bp.signals.ecg.ecg(signal=signal, sampling_rate=fs, show=False)
            bpm = np.mean(bpm)
            rmssd_segment = td.rmssd(rpeaks=t[rpeaks])["rmssd"]
            sdnn_segment = td.sdnn(rpeaks=t[rpeaks])["sdnn"]

            hr.append(bpm)
            rmssd.append(rmssd_segment)
            sdnn.append(sdnn_segment)
        else:
            while stop < n:
                stop = start + window_size
                segment = signal[start:stop]
                print(segment.shape)
                segment, info = nk.ecg_process(segment, sampling_rate=fs)
                segment = segment["ECG_Clean"]
                t, filtered_signal, rpeaks, _, _, _, bpm = bp.signals.ecg.ecg(signal=segment, sampling_rate=fs, show=False)
                try:
                    segment = signal.iloc[start:stop]
                except AttributeError:
                    segment = signal[start:stop]
                try:
                    bpm = np.mean(bpm)
                    rmssd_segment = td.rmssd(rpeaks=t[rpeaks])["rmssd"]
                    sdnn_segment = td.sdnn(rpeaks=t[rpeaks])["sdnn"]
                except Exception as e:
                    bpm = np.nan
                    rmssd_segment = np.nan
                    sdnn_segment = np.nan

                hr.append(bpm)
                rmssd.append(rmssd_segment)
                sdnn.append(sdnn_segment)
                start = stop - overlap
        return hr, rmssd, sdnn
    
    def extract_hr(self, signal):
        hr, _, _ = self.extract_ecg_features_pyhrv(signal)
        return hr
    
    def extract_rmssd(self, signal):
        _, rmssd, _ = self.extract_ecg_features_pyhrv(signal)
        return rmssd
    
    def extract_sdnn(self, signal):
        _, _, sdnn = self.extract_ecg_features_pyhrv(signal)
        return sdnn
    
    def extract_eda_features_nk(self, signal):
        """
        Extracts EDA features (mean SCL, SCR rate) using neurokit methods
        """
        fs = tools.get_sampling_rate(signal)
        signal = signal.iloc[:, -1]
        
        signal = signal.astype(np.double)
        signal = hp.scale_data(signal)
        signal = scipy.ndimage.median_filter(signal, int(fs))  # Median smoothing to reject outliers
        signals, info = nk.eda_process(signal, sampling_rate=fs)
        phasic = signals["EDA_Phasic"].to_numpy()
        tonic = signals["EDA_Tonic"].to_numpy()

        peak_info = nk.eda_findpeaks(phasic, fs, amplitude_min=MIN_AMP)
        peak_idx = peak_info["SCR_Peaks"].astype(int)
        peak_amps = peak_info["SCR_Height"]
        peaks = np.zeros(phasic.shape)
        np.put(peaks, peak_idx, [1])
        tonic = tonic - peaks

        return tonic, peaks
    
    def extract_mean_scl(self, signal):
        fs = tools.get_sampling_rate(signal)
        window_size = int(WINDOW_SIZE_EDA*1/fs)
        overlap = int(OVERLAP_EDA*1/fs)

        tonic, _ = self.extract_eda_features_nk(signal)

        if tonic is None:
            print("mean SCL is None")
            return None
        
        n = tonic.size
        start = 0
        stop = start + window_size
        out = []
        if stop >= n:
            segment = tonic
            segment_mean = np.mean(segment)
            out.append(segment_mean)
        while stop < n:
            stop = start + window_size
            segment = tonic[start:stop]
            segment_mean = np.mean(segment)
            out.append(segment_mean)
            start = stop - overlap
        mean_scl = np.asarray(out)
        return mean_scl

    def extract_scr_rate(self, signal):
        fs = tools.get_sampling_rate(signal)
        window_size = int(WINDOW_SIZE_EDA*1/fs)
        overlap = int(OVERLAP_EDA*1/fs)

        _, peaks = self.extract_eda_features_nk(signal)

        if peaks is None:
            print("SCR rate is None")
            return None

        n = peaks.size
        start = 0
        stop = start + window_size
        out = []
        if stop >= n:
            segment = peaks
            num_peaks = sum(segment)
            out.append(num_peaks)
        while stop < n:
            stop = start + window_size
            segment = peaks[start:stop]
            num_peaks = sum(segment)
            out.append(num_peaks)
            start = stop - overlap
        scr_rate = np.asarray(out)
        return scr_rate

    @property
    def name(self):
        return self._name
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def output_type(self):
        return self._output_type