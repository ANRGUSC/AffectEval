import numpy as np
import pandas as pd
import time

from pipeline.node import Node


class Pipeline:

    def __init__(self):
        self._nodes = []

    def add_node(self, node):
        self._nodes.append(node)

    def generate_nodes_from_layers(self, layers_list):
        """
        Generates an acyclic graph of nodes from the input layers.
        Parameters
        --------------------
        :param layers_list: List of layers to the pipeline, in order.
        :type layers_list: list of pipeline layers
        """
        for layer in layers_list:
            self._nodes.append(Node(layer))
        for i in range(len(self._nodes)-1):
            self._nodes[i].add_next(self._nodes[i+1])
        for i in range(1, len(self._nodes)-1):
            self._nodes[i].add_prev(self._nodes[i+1])

    def run(self):
        data = None
        while self._nodes:
            node = self._nodes.pop(0)
            print(f"Running node {node.name}...")
            start = time.time()
            data = node.run(data)
            end = time.time()
            print(f"Elapsed time for {node.name}: {end-start}")