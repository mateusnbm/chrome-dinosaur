#
# network.py
#
# Based on https://github.com/miloharper/multi-layer-neural-network
#


import random
from numpy import exp, array, random, dot
import numpy as np


'''
Class representing a network layer (MLP layer).
'''

class NeuronLayer():

    '''
    Instantiates a network layer with 'K' neurons and 'W' inputs per neuron. The
    attribute 'synaptic_weights' is a (W x K) matrix representing the weight of
    each neuron input, it is initialized with random numbers between -1 and 1.
    '''

    def __init__(self, number_of_neurons, number_of_inputs_per_neuron, output_layer):

        i = number_of_inputs_per_neuron
        j = number_of_neurons

        self.output_layer = output_layer
        self.bias = random.uniform(-1, 1)
        self.number_of_neurons = j
        self.number_of_inputs_per_neuron = i
        self.synaptic_weights = 2 * np.random.random((i, j)) - 1


'''
Class representing the network itself (MLP).
'''

class NeuralNetwork():

    '''
    '''

    def __init__(self, layers):

        self.layers = layers

    '''
    Maps a genome genes into the network weights.
    '''

    def load_weights_from_genome(self, genome):

        starting_index = 0

        for layer in self.layers:

            for i in range(layer.number_of_inputs_per_neuron):

                for j in range(layer.number_of_neurons):

                    index = starting_index + (i * layer.number_of_neurons) + j
                    layer.synaptic_weights[i, j] = genome.genes[index]

            length = layer.number_of_neurons * layer.number_of_inputs_per_neuron
            starting_index += length

            if layer.output_layer == False:

                index = starting_index
                layer.bias = genome.genes[index]
                starting_index += 1

    '''
    Print network weights.
    '''

    def print_weights(self):

        for layer in self.layers:

            print('weights:' + str(layer.synaptic_weights))
            print('bias:' + str(layer.bias))
            print('')

    '''
    The Sigmoid function, which describes an S shaped curve.
    We pass the weighted sum of the inputs through this function to
    normalise them between 0 and 1.
    '''

    def __sigmoid(self, x):

        return 1 / (1 + exp(-x))

    '''
    The derivative of the Sigmoid function.
    This is the gradient of the Sigmoid curve.
    It indicates how confident we are about the existing weight.
    '''

    def __sigmoid_derivative(self, x):

        return x * (1 - x)

    '''
    Compute neural network output for a given input.
    '''

    def think(self, inputs):

        inputs = np.array(inputs, dtype=float)

        output = self.__sigmoid(dot(inputs, self.layers[0].synaptic_weights))
        output = output + self.layers[0].bias

        for i in range(len(self.layers)-1):

            output = self.__sigmoid(dot(output, self.layers[i+1].synaptic_weights))

            if self.layers[i+1].output_layer == False:

                output = output + self.layers[i+1].bias

        return output
