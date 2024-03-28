import numpy as np
import paho.mqtt.client as mqtt
import pandas as pd
import random

from signal_acquisition.signal_acquisition import SignalAcquisition


class SignalAcquisitionClient():

    def __init__(self, host="localhost", port=1883, subscribe_topic="/signal_acq/sub", publish_topic="/signal_acq/pub", keepalive=60):
        self._mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._subscribe_topic = subscribe_topic
        self._publish_topic = publish_topic
        self._client_id = random.randint(1, 10)

        self._mqtt_client.on_connect = self.on_connect
        self._mqtt_client.on_message = self.on_message
        self._mqtt_client.on_publish = self.on_publish
        self._mqtt_client.subscribe(self._subscribe_topic)
        self._mqtt_client.connect(host, port)
        print(f"Signal acquisition node (ID: {self.client_id}) connected to host")

        self.signal_acq = SignalAcquisition()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")

    def on_message(client, userdata, msg):
        print(f"{msg.topic}/ {str(msg.payload)}")

    def on_publish(self):
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