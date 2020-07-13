import numpy as np

class NeuralNet(object):
    """
    layers
    nodes per layer
    initialize random values for the weights and biases

    Using a feed forward system with 3 to 5 inputs and possibly 3-4 layers.
    The inputs will be distances recorded at different angles of the car.
    These angles will let the car know how close it is to obstacles
    Genetic algorithm used to train the car

    Need a method for saving the "mind" of the top car at the end.  Have a
    way of starting with a specific brain.
    """

    def __init__(self, genes, inputs):
        self.layers = len(genes[0])
        self.weights = genes[0]
        self.biases = genes[1]
        self.h = self.feed_forward(inputs)

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def feed_forward(self, inputs):
        in_ = inputs
        for layer in range(self.layers):
            a = 0
            h = []
            for nodes in range(len(self.biases[layer])):
                CONST = int(len(self.weights[layer]) / len(self.biases[layer]))
                for i in range(CONST):
                    a += self.weights[layer][nodes * CONST + i] * in_[i]
                h.append(self.sigmoid(a+self.biases[layer][nodes]))
            in_ = h
        # print(h[0] * 2 - 1)
        return h[0] * 2 - 1

def feed_forward(genes, inputs):
    layers = len(genes[0])
    weights = genes[0]
    biases = genes[1]
    in_ = inputs
    for layer in range(layers):
        a = 0
        h = []
        for nodes in range(len(biases[layer])):
            CONST = int(len(weights[layer]) / len(biases[layer]))
            for i in range(CONST):
                a += weights[layer][nodes * CONST + i] * in_[i]
            h.append(sigmoid(a+biases[layer][nodes]))
        in_ = h
    # print(h[0] * 2 - 1)
    return h[0] * 2 - 1

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))
