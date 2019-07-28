# CS 545 Machine Learning
# Homework 5: K-Means Clustering
# Haomin He

"""
References: 
Lecture Slides
OptDigits data, originally from the UCI ML repository
https://en.wikipedia.org/wiki/Netpbm_format#PGM_example
https://github.com/paolo215/CS445-ML
https://github.com/asayles
https://github.com/scottfabini/machine-learning-perceptron
https://github.com/abrahamsk/ml_k-means-clustering
"""

import numpy as np
import pandas as pd
import random
import time
import itertools
import sys
from PIL import Image






CHANGE = 1e-01
LENIENT = 1
class Kmeans(object):
    def __init__(self, numOfFeatures, K):
        self.K = K
        self.numOfFeatures = numOfFeatures
        self.centroids = np.random.randint(0, 16, (self.K, self.numOfFeatures))
        self.clusters = []
        self.clustersClass = []

    def resetClusters(self):
        self.clusters = [ [] for f in range(self.K)]

    def train(self, features):
        # train kmeans until the centroid stops moving
        centroids = None
        notCloseEnough = True
        # Keep moving the centroids until the values stops changing
        while notCloseEnough == True:
            centroids = self.cluster(features)
            notCloseEnough = not self.allclose(np.array(self.centroids), np.array(centroids))
            self.centroids = centroids

    def allclose(self, old, new):
        # Check the difference between the previous and current centroids
        closeEnough = []
        for i in range(len(old)):
            close = [f <= CHANGE for f in  np.abs(old[i]- new[i])]
            if sum(close) == int(self.numOfFeatures * LENIENT) :
                closeEnough.append(True)
        if sum(closeEnough) == int(len(old) * LENIENT):
            return True
        return False

    def closestCentroid(self, x, centroids):
        # Determine the closest centroid for this instance using
        # euclidean distance.
        euclideanDists = []
        # Calculate euclidean dist for all centroids
        for centroid in range(len(centroids)):
            euclideanDists.append(self.euclideanDistance(x, centroids[centroid]))

        argMinWinner = min(euclideanDists)
        possibleWinners = []
        for i in range(len(euclideanDists)):
            if np.abs(argMinWinner - euclideanDists[i]) <= CHANGE:
                possibleWinners.append(i)

        # randomly select winner
        return np.random.choice(possibleWinners)

    def cluster(self, training):
        # Creates clusters by iterating through the training set and see
        # which cluster they belong to and then calcualte the new value
        # of the centroids.
        self.resetClusters()

        # Iterate through training set
        for idx in range(len(training)):
            # determine where this training instance belong to which cluster
            winner = self.closestCentroid(training[idx], self.centroids)
            self.clusters[winner].append(idx)

        centroids = []
        # Calculate centroids
        for centroid in range(len(self.centroids)):
            # Calculate the mean if this cluster is not empty
            if len(self.clusters[centroid]) != 0:
                newCentroid = training[self.clusters[centroid]].mean(axis=0)
            else:
                newCentroid = self.centroids[centroid]
            centroids.append(newCentroid)

        return centroids


    def euclideanDistance(self, x, y):
        total = 0
        for a, b in zip(x,y):
            total += (a - b) ** 2
        return np.sqrt(total)

    def meanSquareError(self, x, c):
        top = self.euclideanDistance(x, c.mean(axis=0)) ** 2
        bottom = len(c)
        return top / float(bottom)

    def averageMeanSquareError(self, training):
        total = 0
        nonEmpty = 0
        for i in range(self.K):
            if len(self.clusters[i]) != 0:
                cluster = np.array(training[self.clusters[i]])
                length = len(cluster)
                for i in range(length):
                    mse = self.meanSquareError(cluster[i], cluster)
                    total += mse
                nonEmpty += 1
        return total / nonEmpty

    def meanSquareSeparation(self, training):
        total = 0
        nonEmpty = [f for f in range(len(self.clusters)) if len(self.clusters[f]) > 0]
        nonEmptyLength = len(nonEmpty)
        uniquePairs = itertools.combinations(nonEmpty, 2)
        print(uniquePairs)
        for i, j in uniquePairs:
            dist = self.euclideanDistance(self.centroids[i], self.centroids[j]) ** 2
            total += dist
        return total / (((nonEmptyLength) * (nonEmptyLength - 1)) / 2)


    def determineClass(self, labels):
        # Determine the class of each clusters by counting the number of classes
        # inside the cluster
        length = len(self.clusters)
        self.clustersClass = [None] * length

        for cluster in range(length):
            if len(self.clusters[cluster]) == 0:
                continue
            clusters = labels[self.clusters[cluster]]
            unique, counts = np.unique(clusters, return_counts=True)
            winner = np.argmax(counts)
            possibleWinners = []
            for i in range(len(counts)):
                if counts[i] == counts[winner]:
                    possibleWinners.append(unique[i])

            winner = np.random.choice(possibleWinners)
            self.clustersClass[cluster] = int(winner)
        print(self.clustersClass)

    def predict(self, testing):
        predictions = []
        length = len(testing)
        for idx in range(length):
            winner = self.closestCentroid(testing[idx], self.centroids)
            predictions.append(self.clustersClass[winner])
        return predictions


    def draw(self, path):
        for i in range(len(self.centroids)):
            centroid = self.centroids[i]
            img = Image.new("L", (8,8), "black")
            center8x8 = np.array(centroid).reshape(8,8)
            filename = "k_" + str(self.K) + "_cluster" + str(i) + "_" + str(self.clustersClass[i]) + ".png"
            imgSize = img.size[0]
            # Draw
            for ii in range(imgSize):
                for iii in range(imgSize):
                    img.putpixel((iii,ii), int(center8x8[ii][iii]) * 16)

            # Resize image
            img.resize((32,32))

            # Save file
            img.save(path + filename)



def evaluate(num, testingLabels, predictions):
    conf = {}
    correct = 0
    total = len(testingLabels)
    for i in range(num):
        conf[int(i)] = [0] * num

    for i in range(total):
        actual = int(testingLabels[i])
        predicted = int(predictions[i])
        if actual == predicted:
            correct += 1
        conf[actual][predicted] += 1
    accuracy = correct / total
    return accuracy, conf



def runK_MeansTrial(labelCol, trainingFeatures, trainingLabels, 
        testingFeatures, testingLabels, iteration, K, path=""):
    """
    Specify the number of iteration: Repeat 5 times, with different random number seeds.
    K clusters: K = 10, 10 final cluster centers
    """
    models = []
    for i in range(iteration):
        print("iteration number: ")
        print(i)
        K_Model = Kmeans(labelCol, K)
        K_Model.train(trainingFeatures)
        amse = K_Model.averageMeanSquareError(trainingFeatures)
        print("averageMeanSquareError", amse)
        models.append((K_Model, amse))

    # Determine the winner by looking at the smallest amse
    winner = min(models, key=lambda x: x[1])
    K_Model = winner[0]
    mse = winner[1]
    mss = K_Model.meanSquareSeparation(trainingFeatures)

    K_Model.determineClass(trainingLabels)
    predictions = K_Model.predict(testingFeatures)
    accuracy, conf = (evaluate(10, testingLabels, predictions))
    print("Accuracy: ", accuracy)
    print("Confidence Matrix: ", conf)

    K_Model.draw(path)

    print("Average mean square error", mse)
    print("Mean square separation", mss)



def main(argv):
    # Run your clustering program on the training data (optdigits.train) with K = 10, obtaining
    # 10 or 30 final cluster centers.
    K = 30 
    storage = "./"
    print("Load dataset optdigits data")
    dfTrain = pd.read_csv("optdigits.train", dtype=np.float, header=None)
    dfTest = pd.read_csv("optdigits.test", dtype=np.float, header=None)
    # Split dataset
    labelCol = len(dfTrain.columns) - 1
    trainingLabels = np.array(dfTrain[labelCol])
    trainingFeatures = np.array(dfTrain.drop(labelCol, axis=1))
    testingLabels = np.array(dfTest[labelCol])
    testingFeatures = np.array(dfTest.drop(labelCol, axis=1))
    runK_MeansTrial(labelCol, trainingFeatures, trainingLabels, 
            testingFeatures, testingLabels, 5, K, storage)

if __name__ == "__main__":
    main(sys.argv[1:])
    # print("Test if code can reach here")

