import os
import sys
file_path = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.abspath(os.path.join(file_path, "../../"))
# module_path = "C:/Users/zhoux/Desktop/Projects/CAREforMe/"
sys.path.append(module_path)

import paho.mqtt.client as mqtt
import random
import time

from care_for_me.mqtt.signal_acquisition_client import SignalAcquisitionClient
from care_for_me.signals import Signals


def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")


def on_publish(client, userdata, mid, reason_code, properties):
    print("Message published")    


if __name__ == "__main__":
    signal_acq_publisher = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Signal Acq publisher")
    host = "localhost"
    port = 1883
    signal_acq_publisher.on_connect = on_connect
    signal_acq_publisher.on_publish = on_publish

    if signal_acq_publisher.connect(host, port, 60) != 0:
        print("Couldn't connect to the mqtt broker")
        sys.exit(1)

    while True:
        message = str(random.randint(0, 10))
        res = signal_acq_publisher.publish(
            topic="/signal_acq",
            payload=message.encode("utf-8"),
            qos=0
        )

        res.wait_for_publish()
        time.sleep(1)
