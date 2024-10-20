# This script reads and formats APD data following the requirements of CAREforMe
# NOTE: The original file structure of the APD dataset was modified to be as follows:
# /APD
#     /p_4
#         /baseline
#         ...
#     /p_6

import math
import numpy as np
import os
import pandas as pd
import care_for_me.signals as signals

from pathlib import Path


# ROOT_DIR = "C:\\Users\\zhoux\\Desktop\\Projects\\CAREforMe"
# DATA_DIR = os.path.join(ROOT_DIR, "data")
# APD_PATH = os.path.join(DATA_DIR, "APD")
# METRICS = os.path.join(DATA_DIR, "metrics", "APD")


class DataTypes:
    ANKLE_L = "LeftAnkle"
    ANKLE_R = "RightAnkle"
    WRIST_L = "LeftWrist"
    WRIST_R = "RightWrist"
    EDA = "EDA"
    ECG = "Heart"
    POSTURE = "Posture"

    DATA_TYPES = [
        ANKLE_L, ANKLE_R, WRIST_L, WRIST_R, EDA, ECG, POSTURE
    ]


FS_DICT = {
    DataTypes.ANKLE_L: 50.0,
    DataTypes.ANKLE_R: 50.0,
    DataTypes.WRIST_L: 50.0,
    DataTypes.WRIST_R: 50.0,
    DataTypes.EDA: 50.0,
    DataTypes.ECG: 250.0,
    DataTypes.POSTURE: 1.0
}


class Phases:
    BASE_REST = "Baseline_Rest"

    BUG_RELAX = "BugBox_Relax"
    BUG_ANTICIPATE = "BugBox_Anticipate"
    BUG_EXPOSURE = "BugBox_Exposure"
    BUG_BREAK = "BugBox_Break"

    SPEECH_RELAX = "Speech_Relax"
    SPEECH_ANTICIPATE = "Speech_Anticipate"
    SPEECH_EXPOSURE = "Speech_Exposure"
    SPEECH_BREAK = "Speech_Break"

    PHASES_LIST = [
        BASE_REST,
        BUG_RELAX,
        BUG_ANTICIPATE,
        BUG_EXPOSURE,
        BUG_BREAK,
        SPEECH_RELAX,
        SPEECH_ANTICIPATE,
        SPEECH_EXPOSURE,
        SPEECH_BREAK
    ]

    BASELINE_PHASES = [
        BASE_REST
    ]

    BUG_PHASES = [
        BUG_RELAX,
        BUG_ANTICIPATE,
        BUG_EXPOSURE,
        BUG_BREAK
    ]

    SPEECH_PHASES = [
        SPEECH_RELAX,
        SPEECH_ANTICIPATE,
        SPEECH_EXPOSURE,
        SPEECH_BREAK
    ]

    # NOTE: NO SELF-REPORTS AVAILABLE FOR 'BASE SPEECH' AND 'REFLECT' PHASES
    phases = {
        "Baseline": [BASE_REST],
        "Bug baseline": [BUG_RELAX],
        "Speech baseline": [SPEECH_RELAX],
        "Bug all": [BUG_RELAX, BUG_ANTICIPATE, BUG_EXPOSURE, BUG_BREAK],
        "Speech all": [SPEECH_RELAX, SPEECH_ANTICIPATE, SPEECH_EXPOSURE, SPEECH_BREAK],
        "Bug pre-anxiety": [BUG_RELAX, BUG_ANTICIPATE],
        "Speech pre-anxiety": [SPEECH_RELAX, SPEECH_ANTICIPATE],
        "Bug anxiety": [BUG_EXPOSURE],
        "Speech anxiety": [SPEECH_EXPOSURE],
        "Bug post-anxiety": [BUG_BREAK],
        "Speech post-anxiety": [SPEECH_BREAK]
    }


class Tasks:
    ALL = "all"
    BASELINE = "baseline"
    BUGS = "bug_box_task"
    SPEAKING = "speaking_task"
    TASKS = {
        BASELINE: Phases.BASELINE_PHASES,
        BUGS: Phases.BUG_PHASES,
        SPEAKING: Phases.SPEECH_PHASES
    }


class Groups: 
    ALL = "all"
    HA = "high_anxiety_group"
    LA = "low_anxiety_group"

    ha_participant_indices = [
        '4', '6', '7', '8', '10', '12', '15', '16', '18', '22', '26', '27', '29', '31', '32', '33', '35', '42', '45', '47', '48', '49', '54', '55', '66', '69'
    ]

    la_participant_indices = [
        '14', '21', '23', '25', '34', '39', '43', '46', '51', '57', '71', '72', '77', '78', '79', '80', '82', '83', '84', '85', '87', '88', '89', '91', '92', '93'
    ]

SUBJECTS = Groups.ha_participant_indices + Groups.la_participant_indices


class Responses:
    ALL = "all"
    AVOID = "avoidance_response"
    CONFRONT = "confrontation_response"
    ESCAPE = "escape_response"
    SAFETY = "safety_behavior_response"


def reformat_and_save_data(apd_path):
    for subject in SUBJECTS:
        folder = os.path.join(apd_path, "formatted", f"{subject}")
        print(f"Saving data for subject {subject}...")
        for task in Tasks.TASKS.keys():
            for phase in Tasks.TASKS[task]:
                for mode in DataTypes.DATA_TYPES:
                    file_name = os.path.join(apd_path, f"p_{subject}", task, f"{mode}_{phase}.csv")
                    new_file = os.path.join(folder, f"{subject}_{phase}_{mode}.csv")
                    new_file = Path(new_file)
                    new_file.parent.mkdir(parents=True, exist_ok=True)
                    data = pd.read_csv(file_name)
                    # Add artificial timestamp column
                    fs = FS_DICT[mode]
                    timestamp = [1/fs*i for i in range(data.shape[0])]
                    data["timestamp"] = timestamp
                    data.to_csv(new_file)


def get_suds_labels(apd_path, threshold="fixed"):
    suds_cols = [0 for _ in range(len(Phases.PHASES_LIST))]
    label_dict = {
        "Baseline_Rest": "Baseline_SUDS", 
        "BugBox_Relax": "BugBox_Relax_SUDS",
        "BugBox_Anticipate": "BugBox_Preparation_SUDS",
        "BugBox_Exposure": "BugBox_Exposure_SUDS", 
        "BugBox_Break": "BugBox_Break_SUDS", 
        "Speech_Relax": "Speech_Relax_SUDS",
        "Speech_Anticipate": "Speech_SUDS",
        "Speech_Exposure": "Speech_Exposure_SUDS",
        "Speech_Break": "Speech_Break_SUDS"
    }
    for i in range(len(Phases.PHASES_LIST)):
        suds_cols[i] = label_dict[Phases.PHASES_LIST[i]]
    participant_file = os.path.join(apd_path, "participants_details.csv")
    df = pd.read_csv(participant_file)
    participant_ids = df.loc[:, "Participant"]
    # Cast subject ID to the correct data type (int64)
    participant_ids = participant_ids.apply(lambda x: int(x[1:]))

    suds_labels = df.loc[:, suds_cols]
    mean_suds = np.mean(suds_labels.loc[:, suds_cols], axis=1)
    labels = []

    for i in range(suds_labels.shape[0]):
        if threshold == "fixed":
            mean = 50
        else:
            mean = mean_suds.iloc[i, :]

        row = suds_labels[suds_cols].iloc[i]
        zero_idx = row.index[row < mean]
        one_idx = row.index[row >= mean]
        row[zero_idx] = 0
        row[one_idx] = 1

        labels.append(row)

    labels = pd.DataFrame(labels)
    labels.insert(0, "subject", participant_ids)

    # Rename label columns to be consistent with phase names
    mapping = {
        "Baseline_SUDS": "Baseline_Rest",
        "BugBox_Relax_SUDS": "BugBox_Relax",
        "BugBox_Preparation_SUDS": "BugBox_Anticipate",
        "BugBox_Exposure_SUDS": "BugBox_Exposure",
        "BugBox_Break_SUDS": "BugBox_Break",
        "Speech_Relax_SUDS": "Speech_Relax",
        "Speech_SUDS": "Speech_Anticipate",
        "Speech_Exposure_SUDS": "Speech_Exposure",
        "Speech_Break_SUDS": "Speech_Break"
    }
    labels = labels.rename(columns=mapping)

    return labels