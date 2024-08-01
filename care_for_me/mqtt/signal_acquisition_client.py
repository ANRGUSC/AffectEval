import numpy as np
import paho.mqtt.client as mqtt
import pandas as pd
import random

from care_for_me.signal_acquisition.signal_acquisition import SignalAcquisition


# TODO: Define message template containing timestamp, sensor value, signal type, subject ID, and label (if applicable)
class SignalAcquisitionClient():
    """
    MQTT client that subscribes to a topic streaming sensor data in real time.
    Collects data over a user-specified period of time (in seconds) before publishing the data packet 
    for the next client(s) in the system.
    """
    def __init__(
            self, signal_types, packet_duration=10,
            source_folder=None, 
            host="localhost", port=1883, 
            subscribe_topic="/signal_acq", publish_topic="/signal_preprocessor", 
            client_id="Signal Acq", 
            keepalive=60
        ):
        self._mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self._subscribe_topic = subscribe_topic
        self._publish_topic = publish_topic
        self._client_id = client_id
        self._host = host
        self._port = port

        self._mqtt_client.on_connect = self.on_connect
        self._mqtt_client.on_log = self.on_connect
        self._mqtt_client.on_message = self.on_message
        self._mqtt_client.on_publish = self.on_publish

        self.signal_acq = SignalAcquisition(signal_types, source_folder)
        
        # self._mqtt_client.connect(host, port)

    def connect(self):
        self._mqtt_client.connect(self._host, self._port)
        print(f"Signal acquisition node (ID: {self.client_id}) connected to host")

    def on_connect(self, client, userdata, flags, reason_code, properties):
        self._mqtt_client.subscribe(self._subscribe_topic)
        self._mqtt_client.subscribe(self._publish_topic)
        print(f"Connected with result code {reason_code}")

    def on_log(self, client, userdata, level, buf):
        print(buf)

    def on_message(self, client, userdata, msg):
        print(f"{self._client_id} received: {str(msg.payload.decode())}")

    def on_publish(self, client, userdata, mid, reason_code, properties):
        pass

    def disconnect(self):
        print("Disconnecting...")
        self.mqtt_client.disconnect()

    def save_to_file(self):
        pass

    @property
    def mqtt_client(self):
        return self._mqtt_client
    
    @property
    def client_id(self):
        return self._client_id