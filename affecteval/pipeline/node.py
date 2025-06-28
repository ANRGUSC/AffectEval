class Node:

    def __init__(self, layer):
        self._layer = layer
        self._name = self._layer.name
        self._prev = []
        self._next = []

    def check_inputs(self, data):
        return True

    def run(self, data):
        if self.check_inputs(data):
            return self._layer.run(data)

    def add_next(self, next_layer):
        self._next.append(next_layer)

    def add_prev(self, prev_layer):
        self._next.append(prev_layer)

    @property
    def name(self):
        return self._name

    @property
    def next_layers(self):
        return self._next
    
    @property
    def prev_layers(self):
        return self._prev