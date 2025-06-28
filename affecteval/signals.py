class Signals:
    ACC = "ACC"
    BVP = "BVP"
    ECG = "ECG"
    EDA = "EDA"
    EMG = "EMG"
    RESP = "RESP"
    TEMP = "TEMP"

class Features:
    # Statistical ECG features
    ECG_MEAN = "ECG mean"
    ECG_MEDIAN = "ECG median"
    ECG_STD = "ECG std"
    ECG_VAR = "ECG var"
    # Temporal ECG features
    HR = "heart rate"
    HR_MEAN = "mean heart rate"
    RMSSD = "RMSSD"
    RMSSD_MEAN = "mean RMSSD"   # RMS of HRV
    SDNN = "SDNN"
    NN50 = "NN50"
    TINN = "TINN"   # Triangular interpolation index
    # Frequency-based ECG features
    ULF = "ULF"
    LF = "LF"
    LF_NORM = "norm LF"
    HF = "HF"
    HF_NORM = "norm HF"
    UHF = "UHF"
    LF_HF = "LF/HF"

    # Stastistical EDA features
    EDA_MEAN = "EDA mean"
    EDA_MEDIAN = "EDA median"
    EDA_STD = "EDA std"
    EDA_VAR = "EDA var"
    EDA_SLOPE = "EDA slope"
    EDA_RANGE = "EDA range"
    # High-level EDA features
    MEAN_SCL = "mean SCL"
    SCR_RATE = "SCR rate"

    # Statistical EMG features
    EMG_MEAN = "EMG mean"
    EMG_MEDIAN = "EMG median"
    EMG_STD = "EMG std"
    EMG_VAR = "EMG var"
    EMG_RANGE = "EMG range"
    EMG_10 = "EMG 10th percentile"
    EMG_90 = "EMG 90th percentile"
    EMG_NUM_PEAKS = "EMG peaks"
    EMG_PEAK_MEAN = "EMG mean peak"
    EMG_PEAK_STD = "EMG std peak"
    EMG_PEAK_AMP = "EMG peak amp sum"
    # Frequency-based EMG features
    EMG_F_MEAN = "EMG mean freq"
    EMG_F_MED = "EMG med freq"
    EMG_F_PEAK = "EMG peak freq"
    EMG_PSD_1 = "EMG PSD 1" # 0-50 Hz
    EMG_PSD_2 = "EMG PSD 2" # 50-100 Hz
    EMG_PSD_3 = "EMG PSD 3" # 100-150 Hz
    EMG_PSD_4 = "EMG PSD 4" # 150-200 Hz
    EMG_PSD_5 = "EMG PSD 5" # 200-250 Hz
    EMG_PSD_6 = "EMG PSD 6" # 250-300 Hz
    EMG_PSD_7 = "EMG PSD 7" # 300-350 Hz

    # Statistical RESP features
    RESP_MEAN_INH = "RESP mean inhale duration"
    RESP_MEAN_EXH = "RESP mean exhale duration"
    RESP_STD_INH = "RESP std inhale duration"
    RESP_STD_EXH = "RESP std exhale duration"
    RESP_INH_EXH = "RESP inh/exh"
    RESP_RANGE = "RESP range"
    RESP_VOL = "RESP volume"
    RESP_RATE = "RESP rate"
    RESP_DURATION = "RESP duration"

    # Statistical TEMP features
    TEMP_MEAN = "TEMP mean"
    TEMP_STD = "TEMP std"
    TEMP_MIN = "TEMP min"
    TEMP_MAX = "TEMP max"
    TEMP_SLOPE = "TEMP slope"
    TEMP_RANGE = "TEMP range"
