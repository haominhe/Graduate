# CS 545 Machine Learning
# Homework 1 Perceptrons
# Haomin He

import numpy as np
import random
# Initialize internal state of the random number generator.
random.seed(a=None)

class PerceptronClass:
    def __init__(self, targetvalue = 0):
        self.target = targetvalue
        # each perceptron has weight, learningrate
        self.weights = None
        self.learningrate = 0
        self.inputs = None

    def setup(self, learnrate):
        # initialize weights with zeros
        # Each perceptron will have 785 inputs and one output
        self.weights = np.zeros((1, 785))
        self.learningrate = learnrate
        # reset inputs value
        self.inputs = None
        # Choose small random initial weights, w ∈ [−.05, .05]
        for each in range(785):
            # random.randrange(start, stop[, step])
            self.weights[0, each] += (random.randrange(-5,5,1) / 10)

    def multiplyInput(self, inputVector):
        # multiply input vector with its weight
        self.inputs = np.array(inputVector)
        # dot product of two arrays
        mulResult = np.dot(self.inputs, self.weights[0])
        return mulResult

    def updateWeights(self, targetVal, outputVal):
        # Update all weights in each perceptron
        for each in range(len(self.inputs)):
            self.weights[0, each] += self.learningrate * (targetVal - outputVal) * self.inputs[each]



# print("Test purpose")