# CS 545 Machine Learning
# Homework 2 NN
# Haomin He

# References: 
# http://www.hackevolve.com/recognize-handwritten-digits-1/
# http://www.hackevolve.com/recognize-handwritten-digits-2/
# https://github.com/saideeptalari/DigitRecognizer
# https://machinelearningmastery.com/implement-perceptron-algorithm-scratch-python/
# https://github.com/TsebMagi/Machine-Learning-Projects
# https://github.com/paolo215/CS445-ML
# https://docs.python.org/3/tutorial/classes.html
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros.html
# https://realpython.com/python-csv/
# https://stackabuse.com/append-vs-extend-in-python-lists/
# https://maviccprp.github.io/a-perceptron-in-just-a-few-lines-of-python-code/
# https://towardsdatascience.com/understanding-learning-rates-and-how-it-improves-performance-in-deep-learning-d0d4059c1c10
# https://www.youtube.com/watch?v=aircAruvnKk
# https://matplotlib.org/faq/howto_faq.html
# https://github.com/karan6181/RecogHandwrittenDigitsUsingNN
# https://github.com/hlatourette/nn-handwriting
# https://www.python-course.eu/neural_network_mnist.php




import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from NetworkClass import NetworkClass
import datetime



results = None
hiddenUnitsList = [100] # Use n hidden units
EPOCH = 51
momentumList = [0, 0.25, 0.5] # Set momentum to m
momentumName = "Momentum  "
BIAS = 1
NORMALIZER = 255
hiddenUnitsName = "hiddenUnits_"




def loadDataset(dataFilePathStr):
    # Extract data
    dataFile = open(dataFilePathStr, "r")

    # Read and split
    dataStrs = dataFile.read().split("\n")
    dataFile.close()

    data = []

    # Iterate through dataset
    for line in dataStrs:
        if not line: continue
        inst = line.split(",")
        label = int(inst[0])
        inst = [BIAS] + [float(f) / NORMALIZER for f in inst[1:len(inst)]]
        data.append((np.matrix(inst), label))

    return data


def runExperiment1(trainingData, testingData):
    global results
    print("experiment1")
    for n in hiddenUnitsList:
        basename = hiddenUnitsName + str(n)
        if basename in results["training"]:
            continue

        print("hiddenUnits", n)
        log = open(basename + ".txt", "w")

        # Run the network
        trainingAccuracies, testingAccuracies, table = runNetwork(trainingData, testingData, log, 0.1, n, 0.9, basename)

        print("done hiddenUnits", n)
        log.close()





def runNetwork(trainingData, testingData, log, learningRate, hiddenUnits, momentum, basename):
    # Instantiate the 2 layer Neural Network. Train and test the model for EPOCH times
    network = NetworkClass(learningRate, hiddenUnits, momentum)
    table = None
    trainingAccuracies = []
    testingAccuracies = []

    # use for logging accuracy values
    log.write("epoch, training, testing\n")
    limit = EPOCH - 1
    for i in range(EPOCH):
        start = datetime.datetime.now()
        testingAccuracy = None
        # Test the model using test data
        # If limit == 1: update the confusiom matrix table
        if limit == i:
            testingAccuracy = network.test(testingData, True)
        else:
            testingAccuracy = network.test(testingData)

        # Test the model using training data and then train
        trainingAccuracy = network.train(trainingData)

        # Record values
        log.write(",".join(list(map(str, [i, trainingAccuracy, testingAccuracy]))) + "\n")

        # Store values
        trainingAccuracies.append(trainingAccuracy)
        testingAccuracies.append(testingAccuracy)


        end = datetime.datetime.now()
        totalSec = (end - start).total_seconds()
        # print training and test accuracy
        print("epoch", i, trainingAccuracy, testingAccuracy)


    # Store values in a dictionary
    if len(trainingAccuracies) == EPOCH and len(testingAccuracies) == EPOCH and table != None:
        # use the value as a key and store it in a dictionary
        results["training"][basename] = trainingAccuracies
        results["testing"][basename] = testingAccuracies
        results["table"][basename] = table


    return trainingAccuracies, testingAccuracies, table




def runExperiment2(trainingData, testingData):
    global results
    print("experiment2")
    for n in momentumList:
        basename = momentumName + str(n)
        if basename in results["training"]:
            continue

        print("momentum", n)
        log = open(basename + ".txt", "w")
        trainingAccuracies, testingAccuracies, table = runNetwork(trainingData, testingData, log, 0.1, 100, n, basename)
        print("done momentum", n)
        log.close()




def main():
    global results
    trainingData = loadDataset("mnist_train - one half.csv")
    testingData = loadDataset("mnist_test.csv")
    print("Epoch      Training Accuracy     Testing Accuracy")

    # Initialize results dictionary
    results = {}
    results["training"] = {}
    results["testing"] = {}
    results["table"] = {}

    runExperiment1(trainingData, testingData)
    runExperiment2(trainingData, testingData)


if __name__ == "__main__":
    main()
    # print("Test if code can reach here")

