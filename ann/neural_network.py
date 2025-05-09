#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################################################################################
#                                        ANN CORE MODULE                                         #
#                                                                                                #
# This module implements a basic artificial neural network (ANN) from scratch in Python.         #
# It includes data preprocessing, training (via backpropagation), and prediction logic.          #
# Designed to support the NeuroGoalkeeper system for training handball goalkeepers.              #
#                                                                                                #
# Key Features:                                                                                  #
# - Reads and normalizes CSV datasets                                                            #
# - Initializes a multilayer ANN with one hidden layer                                           #
# - Implements forward/backward propagation and weight updates                                   #
# - Logs outputs and predictions to a training results file                                      #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from random import seed, random
from math import exp
from utils.paths import resource_path
import csv
import copy

##################################################################################################
#                                       DATASET LOADING UTILS                                    #
##################################################################################################

def load_csv(filename):
    dataset = []
    try:
        with open(filename, newline='') as archivo:
            reader = csv.reader(archivo, delimiter=',')
            for row in reader:
                if row:
                    dataset.append(row)
    except Exception as e:
        print(f"[ERROR] Could not load CSV file: {filename}")
        print(f"Details: {e}")
    return dataset


def str_column_to_float(dataset, column):
    for row in dataset:
        row[column]=float(row[column].strip())

def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
    for row in dataset:
        row[column] = lookup[row[column]]
        #print(row)
    return lookup

# Find the min and max values for each column
def dataset_minmax(dataset, opf):
    stats = [[min(column), max(column)] for column in zip(*dataset)]
    
    opf.write('Min and Max values for each input feature:\n')
    for values in stats:    
        opf.write(str(values[:]))

    return stats
 
# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)-1):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])  

##################################################################################################
#                                        NEURAL NETWORK LOGIC                                    #
##################################################################################################

##################################################################################################
# 1.INITIALIZE A NETWORK                                                                         #
#                                                                                                #
# Creates a new neural network ready for training. It accepts three parameters:                  #
# 1. The number of inputs                                                                        #
# 2. The number of neurons to have in the hidden layer                                           #
# 3. The number of outputs                                                                       #
#                                                                                                #
# For the hidden layer we create n_hidden neurons and each neuron in the hidden layer has        #
# n_inputs + 1 weights, one for each input column in a data-set and an additional one for        #
# the bias.                                                                                      #
# The output layer that connects to the hidden layer has n_outputs neurons, each with            #
# n_hidden + 1 weights. This means that each neuron in the output layer connects to (has a       #
# weight for) each neuron in the hidden layer.                                                   #
##################################################################################################

def initialize_network(n_inputs, n_hidden, n_outputs, opf):
    network = list()
    hidden_layer = [{'weights':[random() for i in range(n_inputs)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights':[random() for i in range(n_hidden)]} for i in range(n_outputs)]
    network.append(output_layer)  

    # WRITE IN FILE THE INITIAL WEIGHTS (RANDOM) INSIDE THE ANN
    opf.write('INITIAL WEIGHTS HIDDEN LAYER(Wij) - OUTPUT LAYER (Wjk):\n')
    for layer in network:    
        opf.write(str(layer[:])+'\n')
    
    return network

##################################################################################################
# 2.FORWARD PROPAGATE                                                                            #
#                                                                                                #
# 2.1 CALCULATE NEURON ACTIVATION FOR AN INPUT                                                   #
##################################################################################################

def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]    # Neuron activation is calculated as the weighted sum of the inputs. Where: 
                                                # - weight is a network weight
                                                # - input is an input
                                                # - i is the index of a weight or an input
                                                # The function assumes that the bias is the last weight in the list of weights.
    return activation

##################################################################################################
# 2.2 TRANSFER NEURON ACTIVATION                                                                 #
# transfer() function implements sigmoid function.                                               #
# The sigmoid activation function looks like an S shape, it's also called the logistic function. #
# It can take any input value and produce a number between 0 and 1 on an S-curve. It is also a   #
# function of which we can easily calculate the derivative (slope) that we will need later when  #
# backpropagating error.                                                                         #
##################################################################################################

def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))

##################################################################################################
# 2.3 FORWARD PROPAGATE INPUT TO A NETWORK OUTPUT                                                #
# Function forward_propagate() implements the forward propagation for a row of data from our     #
# dataset with our neural network.                                                               #
# Neuron's output value is stored in the neuron with the name 'output'. We collect the outputs   #
# for a layer in an array named new_inputs that becomes the array inputs and is used as inputs   #
# for the following layer.                                                                       #
##################################################################################################

def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

##################################################################################################
# 3.BACK PROPAGATE ERROR                                                                         #
#                                                                                                #
# 3.1 CALCULATE THE DERIVATIVE OF AN NEURON OUTPUT                                               #
##################################################################################################

def transfer_derivative(output):
    return output * (1.0 - output)  # Error calculation for a given neuron.

##################################################################################################
# 3.2 ERROR BACKPROPAGATION                                                                      #
# Backpropagate error and store in neurons. Error signal calculated for each neuron is stored    #
# with the name 'delta'                                                                          #
##################################################################################################

def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

##################################################################################################
# 4.TRAIN NETWORK                                                                                #
#                                                                                                #
# 4.1 UPDATE NETWORK WEIGHTS WITH ERROR                                                          #
# Function update_weights() updates the weights for a network given an input row of data, a      #
# learning rate and assume that a forward and backward propagation have already been performed.  #
##################################################################################################

def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]               
            neuron['weights'][-1] += l_rate * neuron['delta']

##################################################################################################
# 4.2 TRAIN A NETWORK FOR A FIXED NUMBER OF EPOCHS                                               #
# train_network() function implements the training of an already initialized neural network with #
# a given training dataset, learning rate, fixed number of epochs and an expected number of      #
# output values.                                                                                 #
##################################################################################################

def train_network(network, dataset, l_rate, n_epoch, n_outputs, opf):
    for epoch in range(n_epoch):
        sum_error = 0
        for row in dataset:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        opf.write('>>epoch=%d, error=%.3f\n' % (epoch, sum_error))

##################################################################################################
# 5.PREDICT                                                                                      #
#                                                                                                #
# Make a prediction with a network                                                               #
# Forward-propagate an input pattern to get an output is all we need to do to make a prediction. #
# Function named predict() implements this procedure. It returns the index in the network output #
# that has the largest probability.                                                              #
##################################################################################################

def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))

##################################################################################################
#                                     MAIN TRAINING FUNCTION                                     #
#                                                                                                #
# Function ann_MAIN() where the COMPLETE TRAINING is performed by calling the helper functions   #
# previously defined in this module. It executes the training process, logs the ANN evolution,   #
# and stores predictions and metrics into a structured output file.                              #
##################################################################################################

def complete_training(n_hidden,l_rate,n_epoch,dataset_selected):
    # Seed for reproducibility of weight initialization
    seed(1)

    dataset=list(dataset_selected)                  # Dataset to be normalized and trained

    # Explanation:
    # dataset_init holds the original input dataset (unnormalized) which is later used
    # to display predictions including real (x, y, speed, distance) values.
    # We use deepcopy because lists are mutable and normalizing dataset would affect dataset_init otherwise.
    dataset_init=copy.deepcopy(dataset_selected)    # Original dataset to display unnormalized prediction data

    outputfile = resource_path("outputs/training_summary.txt")
    with open(outputfile, 'w+') as opf:

        opf.write('\n' + '-' * 160 + '\n')
        opf.write('ARTIFICIAL NEURAL NETWORK FOR HANDBALL GOALKEEPER TRAINING\n')
        opf.write('Author: Íñigo Rodríguez Sánchez\n')
        opf.write('-' * 160 + '\n\n')

        opf.write('RAW INPUT PATTERNS TO THE NEURAL NETWORK [DISTANCE(m), SPEED(km/h), x(m), y(m), DESIRED OUTPUT (0 or 1)]:\n')

        for row in dataset:
            opf.write('[%s,%s,%s,%s,%s]\n' % (row[0], row[1], row[2], row[3], row[4]))
        opf.write('\n' + '-' * 160 + '\n\n')

        # DATA PREPROCESSING: Convert strings to float/int
        for k in range(len(dataset[0])-1):
            str_column_to_float(dataset, k)
        str_column_to_int(dataset, len(dataset[0])-1)

        # NORMALIZATION: normalize input variables
        minmax = dataset_minmax(dataset, opf)
        normalize_dataset(dataset, minmax)

        opf.write('\n\n' + '-' * 160 + '\n\n')
        opf.write('NORMALIZED INPUT PATTERNS TO THE NEURAL NETWORK [DISTANCE, SPEED, x, y, DESIRED OUTPUT]:\n')

        for row in dataset:
            opf.write('[%s,%s,%s,%s,%s]' % (row[0],row[1],row[2],row[3],row[4]))

        opf.write('\n\n' + '-' * 160 + '\n\n')
        opf.write('SPECIFIED PARAMETERS:\n')

        # INPUTS
        n_inputs = len(dataset[0])
        opf.write(' - Number of neurons in input layer: %d\n' % n_inputs)

        # NEURONS OF THE HIDDEN LAYER
        # n_hidden: number of hidden layer neurons (provided as parameter)
        opf.write(' - Number of neurons in hidden layer: %d\n' % n_hidden)

        # OUTPUTS
        # For this binary classification task, we use 2 output neurons
        n_outputs = 2
        opf.write(' - Number of neurons in output layer: %d\n' % n_outputs)

        # LEARNING RATE
        opf.write(' - Learning rate: %s\n' % l_rate)

        # NUM OF EPOCHS
        #n_epoch = len(dataset)
        opf.write(' - Number of epochs: %d\n' % n_epoch)

        opf.write('\n' + '-' * 160 + '\n\n')

        # NETWORK INITIALIZATION
        network = initialize_network(n_inputs, n_hidden, n_outputs, opf)

        opf.write('\n' + '-' * 160 + '\n')

        opf.write('\nERROR EVOLUTION PER EPOCH:\n')

        train_network(network, dataset, l_rate, n_epoch, n_outputs, opf)

        opf.write('\n' + '-' * 160 + '\n')

        # LOG FINAL WEIGHTS
        opf.write('\nFINAL WEIGHTS - HIDDEN LAYER (Wij) & OUTPUT LAYER (Wjk):\n')
        for layer in network:
            opf.write(str(layer[:])+'\n')


        # LOG PREDICTIONS
        opf.write('\n' + '-' * 160 + '\n')
        opf.write('\nPREDICTIONS MADE BY THE NETWORK:\n')

        k=0                     # Index counter to match dataset and dataset_init positions
        total_shots = 1
        total_errors = 0        # number of wrong predictions
        total_distance = 0.00   # sum of distances and that we will later use to calculate the average distance
        total_speed = 0.00      # sum of velocities and that we will later use to calculate the average velocity

        for row in dataset:
            prediction = predict(network, row)
            if row[-1]!=prediction:
                opf.write('(%d)--[x,y]: %f,%f  |  Distance: %f  |  Speed: %f  |  Expected: %d  |  Predicted: %d  <-- WRONG\n' %
                          (total_shots, float(dataset_init[k][2]), float(dataset_init[k][3]), float(dataset_init[k][0]), float(dataset_init[k][1]), row[-1], prediction))
                total_errors += 1

            else:
                opf.write('(%d)--[x,y]: %f,%f  |  Distance: %f  |  Speed: %f  |  Expected: %d  |  Predicted: %d\n' %
                          (total_shots, float(dataset_init[k][2]), float(dataset_init[k][3]), float(dataset_init[k][0]), float(dataset_init[k][1]), row[-1], prediction))
                #opf.write('Expected=%d, Got=%d\n' % (row[-1], prediction))

            total_shots = total_shots+1
            total_distance = total_distance + float(dataset_init[k][0])
            total_speed = total_speed + float(dataset_init[k][1])
            k=k+1

        total_shots -= 1  # Adjust because we incremented once too many in final loop iteration

        opf.write('\n' + '-' * 160 + '\n')

        opf.write('\nFINAL RESULTS:\n')
        opf.write(' ~ TOTAL SHOTS: %d\n' % total_shots)

        mean_distance = total_distance / total_shots
        mean_speed = total_speed / total_shots
        opf.write('    ~ MEAN DISTANCE: ' + str(round(mean_distance, 2)) + ' meters\n')
        opf.write('    ~ MEAN SPEED: ' + str(round(mean_speed, 2)) + ' km/h\n\n')

        opf.write(' ~ TOTAL PREDICTIONS: %d\n' % total_shots)
        correct_predictions = total_shots - total_errors
        opf.write('    ~ CORRECT: %d\n' % correct_predictions)
        opf.write('    ~ INCORRECT: %d\n' % total_errors)

        accuracy_percentage = round((100 - ((total_errors / total_shots) * 100)), 2)
        error_percentage = round(((total_errors / total_shots) * 100), 2)

        opf.write(' ~ ACCURACY: ' + str(accuracy_percentage) + '%\n')
        opf.write(' ~ ERROR RATE: ' + str(error_percentage) + '%\n\n')

        opf.write('\n' + '-' * 160 + '\n')
        opf.write('-' * 160 + '\n\n')

    return outputfile