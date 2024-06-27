class Node:

    def __init__(self, layer):
        self._layer = layer
        self._prev = []
        self._next = []

    def check_inputs(self, **input_data):
        pass

    def run_layer(self, input_data):
        if self.check_inputs(input_data):
            self._layer.run(input_data)

    def add_next(self, next_layer):
        self._next.apped(next_layer)

    def add_prev(self, prev_layer):
        self._next.apped(prev_layer)

    @property
    def next_layers(self):
        return self._next
    
    @property
    def prev_layers(self):
        return self._prev