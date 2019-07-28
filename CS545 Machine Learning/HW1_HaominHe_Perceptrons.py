# CS 545 Machine Learning
# Homework 1 Perceptrons
# Haomin He

# References: 
# http://www.hackevolve.com/recognize-handwritten-digits-1/
# http://www.hackevolve.com/recognize-handwritten-digits-2/
# https://github.com/saideeptalari/DigitRecognizer
# https://machinelearningmastery.com/implement-perceptron-algorithm-scratch-python/
# https://github.com/TsebMagi/Machine-Learning-Projects
# https://docs.python.org/3/tutorial/classes.html
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros.html
# https://realpython.com/python-csv/
# https://stackabuse.com/append-vs-extend-in-python-lists/
# https://maviccprp.github.io/a-perceptron-in-just-a-few-lines-of-python-code/
# https://towardsdatascience.com/understanding-learning-rates-and-how-it-improves-performance-in-deep-learning-d0d4059c1c10



import numpy as np
import PerceptronClass

# Each perceptron’s target is one of the 10 digits, 0−9
tenPerceptrons = ()
for each in range(10):
    tenPerceptrons += tuple([PerceptronClass.PerceptronClass(each)])


# load csv dataset, returns numpy array
def load_dataset(fileName):
    csvarray = []
    # lineCount = 0
    with open(fileName, 'r') as csvFile:
        # The resulting list is one containing all of the elements of both lists
        csvarray.extend(load_dataset_setup(x) for x in csvFile)
        #for row in csvFile:
            # lineCount += 1 
            # csvarray.extend(load_dataset_setup(row))
    # print(lineCount)
    return np.array(csvarray, float)


def load_dataset_setup(input_row):
    # split data in a row with commas
    splitLine = input_row.split(',')
    # make each value as a float number
    floatSplitLine = [float(each) for each in splitLine]
    # Scale each data value to be between 0 and 1, divide each value by 255
    for eachVal in range(1, len(floatSplitLine)):
        floatSplitLine[eachVal] /= 255
    # list.insert(index, obj), insert into the second index
    # the very first value is target value
    floatSplitLine.insert(1, 1.0)
    # A tuple is a collection which is ordered and unchangeable. 
    return tuple(floatSplitLine)


def accuracy(fileData):
    # number of right cases divide total 
    right = 0
    total = 0
    # first column is the target number
    # rest of data is pixel values for each digit
    for eachRowData in fileData:
        target = eachRowData[0]
        prediction = accuracyHelper(eachRowData[1:])
        if prediction == target:
            right += 1
        total += 1
    return right / total


def accuracyHelper(inputPixel):
    # The output with the highest value of w ∙ x is the prediction for this training example.
    highestVal = -1000
    prediction = -1000
    # loop through perceptrons and calculate w ∙ x
    for each in range(10):
        mulResult = tenPerceptrons[each].multiplyInput(inputPixel)
        if mulResult > highestVal:
            highestVal = mulResult
            prediction = each
    # return the prediction
    return prediction


def runEpoch(trainData):
    for each in trainData:
        runTest(each[1:], each[0])


def runTest(inputs, target):
    for each in range(10):
        mulResult = tenPerceptrons[each].multiplyInput(inputs)
        # update weights if w ∙ x <= 0
        # output units t − y could be zero, and thus the weights to
        # that output unit would not be updated.
        if mulResult <= 0 and each != target:
            pass
        elif mulResult <= 0 and each == target:
            tenPerceptrons[each].updateWeights(1, 0)
        elif mulResult > 0 and each == target:
            pass
        elif mulResult > 0 and each != target:
            tenPerceptrons[each].updateWeights(0, 1)


def confusionMatrix(testingData):
    # build the confusion matrix 0-9 values
    confusion_matrix = np.zeros((10, 10), 'int64')
    # increase matrix cell value based on the accuracy result
    for eachRowData in testingData:
        target = eachRowData[0]
        prediction = accuracyHelper(eachRowData[1:])
        confusion_matrix[int(target), int(prediction)] += 1
    print("Confusion Matrix: ")
    for row in confusion_matrix:
        print(row)
    print("\n")
    return confusion_matrix





# Train the perceptrons with three different learning rates: η = 0.001, 0.01, and 0.1.
leaRates = (0.1, 0.01, 0.001)

if __name__ == "__main__":
    trainingData = load_dataset("mnist_train.csv")
    testingData = load_dataset("mnist_test.csv")
    # print(trainingData)
    # print(testingData)

    # loop through three different rates
    for rate in leaRates:
        print("Learning rate for the following epochs: ", rate)
        # reset perceptron for each learning rate
        for each in range(10):
            tenPerceptrons[each].setup(rate)

        # Compute the accuracy on the training and test sets for this initial set of weights, to include in
        # your plot. (Call this “epoch 0”.)
        print("Epoch Number\t Testing Accuracy\t Training Accuracy")
        print('0 \t\t', accuracy(testingData), '\t\t', accuracy(trainingData))
        # Repeat for 50 epochs
        # After each epoch, compute accuracy on training and test set
        for epoch in range(1, 50):
            # Randomly shuffle the order of the training data
            np.random.shuffle(trainingData)
            # print(trainingData)
            # cycle through the training data, changing the weights (according to the
            # perceptron learning rule)
            runEpoch(trainingData)
            print(epoch, '\t\t', accuracy(testingData), '\t\t', accuracy(trainingData))
        
        print('\n')       
        # Confusion matrix on the test set, after training has been completed.
        confusionMatrix(testingData)
        print('\n')
    # print("Test if code can reach here")

