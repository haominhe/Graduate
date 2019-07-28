# CS 545 Machine Learning
# Homework 3 SVMs and Feature Selection
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
"""

import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn import svm
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
import matplotlib
matplotlib.use("Agg")
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
import matplotlib.pyplot as plt
import random




def split(features, labels, test_size=0.5):
    """ split data into 1/2 training, 1/2 test, each should have approximately
    the same proportion of positive and negative examples as in the entire set.
    Use model_selection library to split dataset and scale features.
    test_size (float) : specify the ratio to split the dataset
    """
    # Split dataset into 1/2 training and 1/2 testing
    trainingFeatures, testingFeatures, trainingLabels, testingLabels = model_selection.train_test_split(features, labels, test_size=0.5, stratify=labels)
    """Scale training data using standardization: Compute the mean and standard deviation
    of each feature (i.e., over a column in the training set). Then subtract the mean from
    each value and divide each value by the standard deviation.
    
    If for any feature the standard deviation is zero (i.e., all values are equal) then simply
    set all the values of that feature to zero.
    """
    # Calculate mean and std
    trainingMeanList  = trainingFeatures.mean(axis=0)
    trainingStdList = trainingFeatures.std(axis=0)

    # Scale datasets
    trainingFeatures -= trainingMeanList
    trainingFeatures /= trainingStdList

    """Scale test data: for each feature, subtract mean and divide by standard deviation of
    that feature, where the mean and standard deviation were calculated for the training
    set, not the test set.
    """
    testingFeatures -= trainingMeanList
    testingFeatures /= trainingStdList
    # 2-dimensional labeld data structure that contains set of features
    # assigned label of each features
    return trainingFeatures, testingFeatures, trainingLabels, testingLabels




def savefig(xlabel, ylabel, filename):
    """Add labels, legends, and save figure to png
    """
    # Reposition title
    plt.gca().title.set_position([0.5, 1.05])

    # Add labels
    plt.ylabel(ylabel, fontsize=16)
    plt.xlabel(xlabel, fontsize=16)

    # Add legend
    plt.legend(loc = "lower right")

    # Save to png
    plt.savefig(filename)

    # Clear plot
    plt.clf()




def experiment1(trainingFeatures, testingFeatures, trainingLabels, testingLabels):
    """
    Use linear kernel.
    Use SVM and test the learned SVM model on test data.
    Report accuracy, precision, and recall.
    Create an ROC curve for this SVM on the test data, using 200 or more evenly spaced thresholds.
    """
    # Instantiate SVM with linear kernel
    clf = svm.SVC(kernel="linear")
    # Train model
    clf.fit(trainingFeatures, trainingLabels)
    # Make a prediction for each instance
    predictions = clf.predict(testingFeatures)
    # Calculate recall, precision, and accuracy
    recall = recall_score(testingLabels, predictions)
    precision = precision_score(testingLabels, predictions)
    accuracy = accuracy_score(testingLabels, predictions)
    print("Experiment 1 accuracy", accuracy)
    print("Experiment 1 precision", precision)
    print("Experiment 1 recall", recall)
    # Plot ROC curve
    # Calculate decision score (distance of the instance to the separating hyperplane)
    scores = clf.decision_function(testingFeatures)
    fpr, tpr, threshold = roc_curve(testingLabels, scores)

    # Design chart
    plt.plot(fpr, tpr, color="c", label="ROC Curve on the Test Data")
    plt.plot([0,1], [0,1], color="k", linestyle="--", label="Random Guess")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.title("Experiment 1: ROC Curve")
    savefig("False Positive Rate or 1 - Specificity", "True Positive Rate or Sensitivity", "Experiment1roc.png")

    # Return classifier to use for experiment2
    return clf




def plotSolo(xAxis, exp, basename, label, title):
    """Add labels, legends, and save figure to png
    """
    # Plot data
    plt.plot(xAxis, exp, color="c", label=label)

    # Add title
    plt.title(title)

    # Add labels and save to png
    savefig("m Features", "Accuracy", basename + ".png")





def experiment2(exp1_clf, trainingFeatures, testingFeatures, trainingLabels, testingLabels):
    """
    Use learned SVM model from experiment1 to obtain the weight vector.
    For m = 2 to 57:
    Select the set of m features that have highest weighted value
    Train an SVM using linear kernel on the training data using m features
    Testing new SVM on the test set
    Plot accuracy vs. m
    """
    # Get all the weights from experiment1's classifier
    weights = exp1_clf.coef_[0]
    # Sort weights in descending order and keep track the column index
    weights = [f[0] for f in sorted([(f, weights[f]) for f in range(len(weights))], key=lambda x : x[1], reverse=True)]
    length = len(trainingFeatures.columns)
    testingAccuracies = []
    mRange = list(range(2, length+1))
    #print(weights)
    #print(mRange)

    # For each iteration, select m features, train the model, and calculate accuracy
    for i in mRange:
        newTrainingFeatureSets = trainingFeatures[weights[0:i]]
        newTestingFeatureSets = testingFeatures[weights[0:i]]
        #print(newTrainingFeatureSets)
        #print(newTestingFeatureSets)
        clf = svm.SVC(kernel="linear")
        clf.fit(newTrainingFeatureSets, trainingLabels)

        accuracy = clf.score(newTestingFeatureSets, testingLabels)
        testingAccuracies.append(accuracy)

    print("Experiment 2 accuracy", accuracy)
    # Solo plot experiment 2 results
    plotSolo(mRange, testingAccuracies, "Experiment 2", "accuracy vs. m features",
            "Experiment 2: Feature selection with linear SVM")
    return testingAccuracies
    



def experiment3(trainingFeatures, testingFeatures, trainingLabels, testingLabels):
    """Select m features at random from the complete set.
    Your features for each m value should be selected with uniform probability over the set of 57
    This experiment is to see if using SVM weights for feature selection (Experiment 2) has any
    advantage over random selection of features.
    """
    length = len(trainingFeatures.columns)
    testingAccuracies = []
    featureCols = []
    choices = list(range(length))
    mRange = list(range(2, length+1))

    # For each iteration, select m features, train the model, and calculate accuracy
    for i in mRange:
        # Randomly select feature
        featureCols.append(choices.pop(random.randint(0, len(choices)-1)))

        newTrainingFeatureSets = trainingFeatures[featureCols]
        newTestingFeatureSets = testingFeatures[featureCols]

        clf = svm.SVC(kernel="linear")
        clf.fit(newTrainingFeatureSets, trainingLabels)

        accuracy = clf.score(newTestingFeatureSets, testingLabels)
        testingAccuracies.append(accuracy)

    print("Experiment 3 accuracy", accuracy)
    plotSolo(mRange, testingAccuracies, "Experiment 3", "accuracy vs. m random features",
            "Experiment 3: Random Feature Selection")
    return testingAccuracies





def main():
    print("Load dataset spambase.data")
    df = pd.read_csv("spambase.data", dtype=np.float, header=None)
    # put data into format needed for the SVM package 
    # Remember the label column
    labelCol = len(df.columns) - 1
    # Change all 0 values to -1 in the labelCol column
    df[labelCol][df[labelCol] == 0] = -1
    # Separate label cols (last column is 1 or -1) and features cols (rest of columns)
    labels = np.array(df[labelCol])
    #print(labels)
    dfFeatures = df.drop(labelCol, 1)
    #print(dfFeatures)
    print("finished loading and modifying datasets")

    """ split data into 1/2 training, 1/2 test, each should have approximately
    the same proportion of positive and negative examples as in the entire set.
    """
    trainingFeatures, testingFeatures, trainingLabels, testingLabels = split(dfFeatures, labels)

    print("running Experiment 1:")
    exp1_clf = experiment1(trainingFeatures, testingFeatures, trainingLabels, testingLabels)
    #print(exp1_clf)
    print("finished Experiment 1")   

    print("running Experiment 2")
    exp2_testingAccuracies = experiment2(exp1_clf, trainingFeatures, testingFeatures, trainingLabels, testingLabels)
    print("finished Experiment 2")

    print("running Experiment 3")
    exp3_testingAccuracies = experiment3(trainingFeatures, testingFeatures, trainingLabels, testingLabels)
    print("finished Experiment 3")






if __name__ == "__main__":
    main()
    #print("Test if code can reach here")

