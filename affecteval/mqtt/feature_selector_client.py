import numpy as np
import paho.mqtt.client as mqtt
import pandas as pd
import random

from affecteval.feature_selector.feature_selector import FeatureSelector


class FeatureSelectorClient():
    # TODO: change signature to specify feature names
    def __init__(self, signal_types, source_folder=None, host="localhost", port=1883, subscribe_topic="/feature_selector", publish_topic="/estimator", client_id="Feature Selector", keepalive=60):
        self._mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self._subscribe_topic = subscribe_topic
        self._publish_topic = publish_topic
        self._client_id = client_id
        self._host = host
        self._port = port

        self._mqtt_client.on_connect = self.on_connect
        self._mqtt_client.on_message = self.on_message
        self._mqtt_client.on_publish = self.on_publish

        self._feat_selector = FeatureSelector(None, None, None)    # Replace with actual values later
        
        # self._mqtt_client.connect(host, port)

    def connect(self):
        self._mqtt_client.connect(self._host, self._port)
        print(f"Feature Selector node (ID: {self.client_id}) connected to host")

    def on_connect(self, client, userdata, flags, reason_code, properties):
        self._mqtt_client.subscribe(self._subscribe_topic)
        self._mqtt_client.subscribe(self._publish_topic)
        print(f"Connected with result code {reason_code}")

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