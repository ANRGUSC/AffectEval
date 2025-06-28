import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


colors = ['#D62728', '#2C9F2C', '#FD7F23', '#1F77B4', '#9467BD',
          '#8C564A', '#7F7F7F', '#1FBECF', '#E377C2', '#BCBD27']


def get_sampling_rate(signal):
    try:
        if type(signal) is pd.DataFrame:
            timestamp = signal.iloc[:, 0]
        elif type(signal) is np.ndarray:
            timestamp = signal[:, 0]
        delta = timestamp[1] - timestamp[0]
        return 1/delta
        # return delta
    except Exception as e:
        return None


def display_signal(signal, data_type=None, title=None, labels=None, start=0, stop=None):
    if type(signal) is pd.DataFrame:
        signal = signal.iloc[:, -1]

    # plt.figure(figsize=(17, 7))
    plt.figure(figsize=(13, 7))

    if stop is None:
        stop = signal.size

    x = np.arange(start, stop, 1)
    if type(signal) == pd.Series:
        signal = signal.to_numpy()
    y = signal[start:stop].flatten()

    # print(f"Min amplitude: {np.min(y)}")
    # print(f"Max amplitude: {np.max(y)}")

    plt.plot(x, y, label=labels, color=colors[0], linewidth=3)
    plt.xlabel("Timestep")
    if data_type and labels is not None:
        plt.ylabel(f"{data_type}, {labels}")
    if labels is not None:
        plt.legend(loc="upper right")
    plt.title(title)

    y_min = np.min(y)
    y_max = np.max(y)
    y_med = np.median([y_min, y_max])
    plt.ylim(y_min - (y_med - y_min) / 5, y_max + (y_max - y_med) / 5)
    matplotlib.rcParams.update({'font.size': 18})
    # plt.tight_layout()