# CS 545 Machine Learning
# Homework 4: Naive Bayes Classification and Logistic Regression
# Haomin He

"""
References: 
Lecture Slides
https://archive.ics.uci.edu/ml/datasets/Spambase
http://scikit-learn.org/stable/modules/preprocessing.html
https://github.com/paolo215/CS445-ML
https://github.com/asayles
https://github.com/ZPdesu/Spam-Message-Classifier-sklearn
https://github.com/scottfabini/machine-learning-perceptron
https://github.com/sushmithashridhar/Naive-Bayes-Classifier
https://github.com/shikhashah2627/Naive_Bayes_Regression_Classification
http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8
http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import random
import sys
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB

import matplotlib.cm as cm
import sklearn.preprocessing
import sklearn.model_selection
import sklearn.linear_model


def split(df):
    # Split data into training and test set where set should have
    # about 40% spam and 60% not spam to reflect the statistics
    # of the full data set.
    # Keep track of the column number of the label
    labelCol = len(df.columns) - 1
    # Keep track the total number of the dataset
    total = len(df[labelCol])
    # Shuffle dataset
    df = shuffle(df)
    # Count the total number of positives and negatives
    totalNumOfPositives = len(df[labelCol][df[labelCol] == 1])
    totalNumOfNegatives = total - totalNumOfPositives
    # Divide by 2
    numOfPositives = int(totalNumOfPositives / 2)
    numOfNegatives = int(totalNumOfNegatives / 2)

    # Use first half as training and rest for testing
    trainingPositives = df[df[labelCol] == 1][numOfPositives:]
    testingPositives = df[df[labelCol] == 1][:numOfPositives+1]
    trainingNegatives = df[df[labelCol] == 0][numOfNegatives:]
    testingNegatives = df[df[labelCol] == 0][:numOfNegatives+1]
    # concatenate all training and testing together
    training = pd.concat([trainingPositives, trainingNegatives])
    testing = pd.concat([testingPositives, testingNegatives])
    # training, testing dataframes
    return training, testing


class Bayes(object):
    def __init__(self):
        self.prior = {}
        self.mean = {}
        self.std = {}

    def train(self, df):
        total = float(len(df))
        labelCol = len(df.columns) - 1
        # Calculate prior by counting the total number of positives
        # and negatives
        positives = df[df[labelCol] == 1]
        negatives = df[df[labelCol] == 0]
        positives = positives.drop(labelCol, axis=1)
        negatives = negatives.drop(labelCol, axis=1)
        # Train the model by creating probabilistic model
        # Compute the prior probability for each class
        self.prior["pos"] = len(positives) / total
        self.prior["neg"] = 1 - self.prior["pos"]
        # Calculate mean and std for each feature
        self.mean["pos"] = positives.mean(axis=0)
        self.mean["neg"] = negatives.mean(axis=0)
        self.std["pos"] = positives.std(axis=0)
        self.std["neg"] = negatives.std(axis=0)


    def predict(self, features):
        # predictions (list) : list of predictions
        predictions = []
        # features (pandas.DataFrame) : dataframe that contains testing features (does not include label)
        # Iterate through test set
        for idx, row in features.iterrows():
            # Use the Gaussian Naive Bayes to classify each instances in test set
            # Calculate P(x_i | class)
            # P(x_i | c_j) = N(x_i; u_i,cj, sigma_i,cj)
            guassianPositives = self.calculateGaussian(row, "pos")
            guassianNegatives = self.calculateGaussian(row, "neg")
            # Use log for all results
            logPositives = np.log(guassianPositives)
            logNegatives = np.log(guassianNegatives)
            # Replace all NaN to 0.0001
            # add a small value epsilon = 0.0001
            logPositives[np.isnan(logPositives) == True] = 0.0001
            logNegatives[np.isnan(logNegatives) == True] = 0.0001
            # Calculate score
            probPositive = np.log(self.prior["pos"]) + logPositives.sum()
            probNegative = np.log(self.prior["neg"]) + logNegatives.sum()
            # Use argmax to make a prediction
            predictions.append(np.argmax([probNegative, probPositive]))
        return predictions


    def calculateGaussian(self, x, key):
        # x (np.array) : numpy array of features
        # key (str) : Key (pos/neg)
        eTop = - ((x - self.mean[key]) ** 2)
        eBottom = 2 * (self.std[key] ** 2)
        e = np.exp(eTop  / eBottom)
        top = float(1)
        bottom = np.sqrt(2 * np.pi) * self.std[key]
        # guassian (np.array)
        return (top/bottom) * e



def evaluate(testingLabels, predictions):
    # Evalute results by calculating accuracy, precision, recall, and confusion matrix table
    conf = {}
    # initialize
    # true positive, true negative, false positive, false negative
    conf["TP"] = 0.0
    conf["TN"] = 0.0
    conf["FP"] = 0.0
    conf["FN"] = 0.0
    total = len(testingLabels)
    for i in range(total):
        actual = testingLabels[i]
        predicted = predictions[i]
        if actual == 0:
            if predicted == 0:
                conf["TN"] += 1
            else:
                conf["FP"] += 1
        else:
            if predicted == 0:
                conf["FN"] += 1
            else:
                conf["TP"] += 1
    accuracy = (conf["TP"] + conf["TN"]) / total
    precision = conf["TP"] / (conf["TP"] + conf["FP"])
    recall = conf["TP"] / (conf["TP"] + conf["FN"])
    return accuracy, precision, recall, conf


def main():
    print("Load dataset spambase.data")
    df = pd.read_csv("spambase.data", dtype=np.float, header=None)
    # Split dataset
    training, testing = split(df)
    print("\n\n Classification with Naive Bayes Classification  \n")
    # Instantiate Naive Bayes Classification
    bayes = Bayes()
    labelCol = len(df.columns) - 1
    testingLabels = np.array(testing[labelCol])
    testingFeatures = testing.drop(labelCol, axis=1)
    # Train the model
    bayes.train(training)
    # Make a prediction for each testingFeatures
    predictions = bayes.predict(testingFeatures)
    # Evaluate by calculating accuracy, precision, recall and
    # confusion matrix
    accuracy, precision, recall, conf = evaluate(testingLabels, predictions)
    # Print out
    print("accuracy", accuracy)
    print("recall", recall)
    print("precision", precision)
    print("conf", conf)


    print("\n\n Classification with Logistic Regression \n")
    ddf = pd.read_csv("spambase.data", dtype=np.float, header=None, index_col=57)
    data = sklearn.utils.shuffle(ddf)
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(data, data.index.values, test_size=0.5)
    # Normalize the data by scaling to the training data
    scaler = sklearn.preprocessing.StandardScaler().fit(X_train)
    X_train_norm = scaler.fit_transform(X_train)
    X_test_norm = scaler.transform(X_test)
    # Initialize Logistic Regression classifier
    clf = sklearn.linear_model.LogisticRegression()
    # Train Logistic Regression using training data
    clf.fit(X_train_norm, y_train)
    # Classify the test data using the Logistic Regression.
    # Score is a weighted classification. Predict is 0/1 classification.
    y_score = clf.decision_function(X_test_norm)
    y_predict = clf.predict(X_test_norm)
    # Print results
    print("Test Set Accuracy Score:")
    print(sklearn.metrics.accuracy_score(y_test, y_predict))
    print("Test Set Precision Score:")
    print(sklearn.metrics.precision_score(y_test, y_predict))
    print("Test Set Recall Score:")
    print(sklearn.metrics.recall_score(y_test, y_predict))
    print("\n")
    print("Test Set Confusion Matrix:")
    print(sklearn.metrics.confusion_matrix(y_test, y_predict))
    print("\n")



if __name__ == "__main__":
    main()
    # print("Test if code can reach here")

