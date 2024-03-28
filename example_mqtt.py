import paho.mqtt.client as mqtt

from signal_acquisition.signal_acquisition_client import SignalAcquisitionClient


if __name__ == "__main__":
    signal_acquisition = SignalAcquisitionClient()
    try:
        print("Press CTRL+c to exit...")
        signal_acquisition.mqtt_client.loop_forever()
    except Exception:
        print("Caught an exception, something went wrong...")
    finally:
        print("Disconnecting from the MQTT broker")
        signal_acquisition.disconnect()
