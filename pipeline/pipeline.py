import numpy as np
import pandas as pd


class Pipeline:

    def __init__(self):
        self._layers = []

    def add_layer(self, layer):
        self._layers.append(layer)

    def run_pipeline(self):
        while self._layers:
            layer = self._layers.pop()
            layer.run()