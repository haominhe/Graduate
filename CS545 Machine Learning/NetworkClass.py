# CS 545 Machine Learning
# Homework 2 NN
# Haomin He

import numpy as np
import random
import scipy.special
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# Initialize internal state of the random number generator.
random.seed(a=None)
WEIGHT = 0.05
INPUT_SIZE = 785
OUTPUT = 10
BIAS = 1

class NetworkClass(object):
    def __init__(self, learningRate, numHiddenUnits, momentum):
        self.numHiddenUnits = int(numHiddenUnits + 1) # Add one for the bias node
        self.momentum = float(momentum)
        self.learningRate = float(learningRate)

        # Set weights for inputHidden (weights from input to hidden)
        self.inputHiddenWeights = np.random.uniform(-WEIGHT, WEIGHT, (INPUT_SIZE, self.numHiddenUnits))

        # Set weights for hiddenOutput
        self.hiddenOutputWeights = np.random.uniform(-WEIGHT, WEIGHT, (self.numHiddenUnits, OUTPUT))


        # Set deltaWeights
        self.inputHiddenDeltaWeights = np.zeros((INPUT_SIZE, self.numHiddenUnits))
        self.hiddenOutputDeltaWeights = np.zeros((self.numHiddenUnits, OUTPUT))

        # Initialize the table
        self.table = {}


    def test(self, data, updateTable=False):
        if updateTable == True:
            self.__resetTable()
        correct = 0
        testingLength = len(data)

        for i in range(testingLength):
            inst = data[i][0]
            label = data[i][1]

            # Forward propagate
            hiddenActivation = self.calculateActivation(inst, self.inputHiddenWeights)
            hiddenActivation[0,0] = BIAS

            outputActivation = self.calculateActivation(hiddenActivation, self.hiddenOutputWeights)

            # Find the highest value and use it as prediction
            probDistributions = self.softmax(outputActivation)
            prediction =  np.argmax(probDistributions)


            if prediction == label:
                correct += 1
            # set value to True to reset and update the table.
            if updateTable == True:
                self.table[label][prediction] += 1


        acc = float(correct) / testingLength
        return acc



    def train(self, trainingData):
        # Test using the training data and then train the model.
        # Accuracy on the training dataset
        acc = self.test(trainingData)
        self.__trainingEpoch(trainingData)
        return acc




    def __trainingEpoch(self, trainingData):
        trainingLength = len(trainingData)
        for i in range(trainingLength):
            inst = trainingData[i][0]
            label = trainingData[i][1]

            # Forward propagation
            # Forward propagate the input * weights for all the nodes
            # in the hidden layer and then apply the sigmoid function.
            # Forward propagate the activation * weights from the hidden
            # layer to output layer and then apply sigmoid function.
            hiddenActivation = self.calculateActivation(inst, self.inputHiddenWeights)
            hiddenActivation[0,0] = BIAS
            outputActivation = self.calculateActivation(hiddenActivation, self.hiddenOutputWeights)

            # Set the target value t_k for output unit k to 0.9 if 
            # the input class is the kth class. Otherwise, set to 0.1.
            targetValues = [0.1] * OUTPUT
            targetValues[label] = 0.9

            # Determine the error for each output unit.
            # Use back propagation algorithm one layer at a time to
            # update all weights in the network.
            # Back propagration
            errorOutput = np.multiply(np.multiply(outputActivation, (1 - outputActivation)), (targetValues - outputActivation))

            sumWeightTimesErrorOutput = np.dot(self.hiddenOutputWeights, errorOutput.transpose()).transpose()

            errorHidden = np.multiply(np.multiply(hiddenActivation, (1 - hiddenActivation)), sumWeightTimesErrorOutput)

            self.hiddenOutputDeltaWeights = self.calculateDeltaWeights(errorOutput, hiddenActivation, self.hiddenOutputDeltaWeights)
            self.inputHiddenDeltaWeights = self.calculateDeltaWeights(errorHidden, inst, self.inputHiddenDeltaWeights)

            # Update weights
            self.hiddenOutputWeights += self.hiddenOutputDeltaWeights
            self.inputHiddenWeights += self.inputHiddenDeltaWeights




    def calculateActivation(self, layer, weights):
        # Calculate the activation by calculating the dot product of layer and
        # weights and apply the sigmoid function.
        return self.sigmoid(np.dot(layer, weights))



    def calculateDeltaWeights(self, error, layer, deltaWeights):
        # Calculate delta weights using this formula:
        # deltaWeights = learningRate * error * layer + 
        # previousDeltaWeights + momentum
        a = np.multiply(self.learningRate, error).transpose()
        b = np.multiply(a, layer).transpose()
        c = np.multiply(self.momentum, deltaWeights)
        return (b + c)



    def softmax(self, matrix):
        # Converts the output values into a probability distribution.
        top = np.exp(matrix)
        return top / top.sum()


    def sigmoid(self, matrix):
        # Apply sigmoid function for each cell in this matrix
        return 1.0 / (1.0 + np.exp(-matrix))



# print("Test purpose")