import math
import numpy as np
import os
import pandas as pd
import signals

from feature_extractor.feature_extractor import FeatureExtractor
from signal_acquisition.signal_acquisition import SignalAcquisition
from signal_preprocessor.signal_preprocessor import SignalPreprocessor
from pipeline.pipeline import Pipeline


ROOT_DIR = "C:\\Users\\zhoux\\Desktop\\Projects\\CAREforMe"
DATA_DIR = os.path.join(ROOT_DIR, "data")
WESAD_PATH = os.path.join(DATA_DIR, "WESAD")
METRICS = os.path.join(DATA_DIR, "metrics", "WESAD")

subject_indices = list(range(2, 12)) + list(range(13, 18))
SUBJECTS = [str(i) for i in subject_indices]

FS_DICT = {
    "chest": {
        "ACC": 700,
        "ECG": 700,
        "EDA": 700,
        "EMG": 700,
        "RESP": 700,
        "TEMP": 700
    },
    "wrist": {
        "ACC": 32,
        "BVP": 64,
        "EDA": 4,
        "TEMP": 4,
    }
}

class Phases:
    BASE = "Base"
    TSST = "TSST"
    MEDI_1 = "Medi_1"
    FUN = "Fun"
    MEDI_2 = "Medi_2"
    PHASES_ORDERED = [BASE, TSST, MEDI_1, FUN, MEDI_2]

    def get_phase_index(phase):
        return Phases.PHASES_ORDERED.index(phase)
    

WESAD_chest_modalities = [
    signals.Signals.ACC,
    signals.Signals.ECG,
    signals.Signals.EDA,
    signals.Signals.TEMP
]


def get_participant_data(participant_idx):
    file = os.path.join(WESAD_PATH, f"S{participant_idx}", f"S{participant_idx}.pkl")
    data = pd.read_pickle(file)
    return data


def get_modality(participant_idx, location, modality):
    data = get_participant_data(participant_idx)
    # Capitalize all columns of DataFrame
    data = data["signal"][location]
    for key in list(data.keys()):
        data[key.upper()] = data.pop(key)
    return data[modality]


def get_time_intervals(participant_idx, phase):
    file = os.path.join(WESAD_PATH, f"S{participant_idx}", f"S{participant_idx}_quest.csv")
    df = pd.read_csv(file, sep=";", header=None, index_col=0).dropna(how="all")
    start = df.loc["# START", :].iloc[Phases.get_phase_index(phase)]
    end = df.loc["# END", :].iloc[Phases.get_phase_index(phase)]
    return [float(start), float(end)]


def get_data_for_phase(participant_idx, phase, location, modalities=None):
    """
    Returns a pd.DataFrame of specified modalities for the given phase and participant.
    If a modality has multiple columns (e.g., ACC), they will be combined into one DataFrame.
    """
    if modalities is None:
        modalities = WESAD_chest_modalities
    if type(modalities) is not list:
        modalities = [modalities]
    out = []
    for m in modalities:
        data_col = get_modality(participant_idx, location, m)
        start, end = get_time_intervals(participant_idx, phase)
        fs = FS_DICT[location][m]
        start_index = math.floor(start*fs)
        end_index = math.ceil(end*fs)
        data_col = data_col[start_index:end_index, :]

        num_cols = data_col.shape[1]
        # Probably don't need to do this again
        if num_cols > 1:
            columns = [f"{m}_{i+1}" for i in range(num_cols)]
        else:
            columns = [m]
        data_col = pd.DataFrame(data_col, columns=columns)

        out.append(data_col)
    out = pd.concat(out, axis=1)
    return out


def get_participant_signals(participant_idx):
    """
    Returns a pd.DataFrame of all chest modalities across all phases for a given participant
    """
    data = []
    for phase in Phases.PHASES_ORDERED:
        phase_data = get_data_for_phase(participant_idx, phase, "chest")
        data.append(phase_data)
    data = pd.concat(data, axis=0)
    return data


def reformat_and_save_data():
    for subject in SUBJECTS:
        folder = os.path.join(WESAD_PATH, "formatted", f"{subject}")
        print(f"Saving data for subject {subject}...")
        for phase in Phases.PHASES_ORDERED:
            print(f"Phase {phase}")
            for mode in WESAD_chest_modalities:
                file_name = os.path.join(folder, f"{subject}_{phase}_{mode}.csv")
                # data = get_participant_signals(subject)
                data = get_data_for_phase(subject, phase, "chest", mode)
                # Add artificial timestamp column
                timestamp = [1/700*i for i in range(data.shape[0])]
                data.insert(0, "timestamp", timestamp)
                data.to_csv(file_name)
