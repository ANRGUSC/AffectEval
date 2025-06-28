import os
import sys
file_path = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.abspath(os.path.join(file_path, "../../"))
# module_path = "C:/Users/zhoux/Desktop/Projects/CAREforMe/"
sys.path.append(module_path)

import time

from affecteval.mqtt.signal_acquisition_client import SignalAcquisitionClient
from affecteval.mqtt.signal_preprocessor_client import SignalPreprocessorClient
from affecteval.mqtt.feature_extractor_client import FeatureExtractorClient
from affecteval.mqtt.feature_selector_client import FeatureSelectorClient
from affecteval.signals import Signals


if __name__ == "__main__":
    host = "localhost"
    port = 1883
    signal_acquisition_client = SignalAcquisitionClient(Signals.ECG)
    signal_preprocessor_client = SignalPreprocessorClient(Signals.ECG)
    feature_extractor_client = FeatureExtractorClient(Signals.ECG)
    feature_selector_client = FeatureSelectorClient(Signals.ECG)
    clients = [
        signal_acquisition_client,
        signal_preprocessor_client,
        feature_extractor_client,
        feature_selector_client
    ]

    try:
        print("Press CTRL+c to exit")
        for client in clients: 
            client.connect()
            client.mqtt_client.loop_start()
        while True:
            pass
    except Exception as e:
        print(f"Caught an exception: {e}")
    finally:
        print("Disconnecting from the MQTT broker")
        for client in clients: 
            client.mqtt_client.loop_stop()
            client.disconnect()
