#!/usr/bin/env python3

import numpy as np

from nimblenet.activation_functions import sigmoid_function
from nimblenet.cost_functions import cross_entropy_cost
from nimblenet.learning_algorithms import RMSprop
from nimblenet.data_structures import Instance
from nimblenet.neuralnet import NeuralNet

import soundfile as sf
import os

class AudioData:
    fileRawData = []
    expectedNetworkResponse = True
    def __init__(self, fileRawData, expectedNetworkResponse):
        self.fileRawData = fileRawData
        self.expectedNetworkResponse = expectedNetworkResponse

audiodata = []
sound_max_size = 0
for dirname, dirnames, filenames in os.walk('train'):
    for filename in filenames:
        path = os.path.join(dirname, filename)
        if(path.find('.keep') == -1):
            sig, fs = sf.read(path)
            if(len(sig.shape) > 1):
                sig.shape = (len(sig.shape) * len(sig)) # from (245196, 2) to (490392,)
            sound_max_size = max(sound_max_size, len(sig))
            audiodata.append(AudioData(sig, path.find('bonjour') != -1))

dataset = []
for idx in range(len(audiodata)):
    fileRawData = audiodata[idx].fileRawData
    expectedNetworkResponse = audiodata[idx].expectedNetworkResponse
    if(sound_max_size != len(fileRawData)):
        fileRawData = np.concatenate((fileRawData, np.zeros((sound_max_size - len(fileRawData)))))
    dataset.append(Instance(fileRawData, [expectedNetworkResponse]))


print len(dataset), 'sounds of size', sound_max_size

# dataset        = [
#     Instance( [0,0], [0,0] ), Instance( [1,0], [1,0] ), Instance( [0,1], [0,1] ), Instance( [1,1], [1,1] )
# ]

settings       = {
    "n_inputs" : sound_max_size,
    "layers"   : [  (200, sigmoid_function), (1, sigmoid_function) ]
}

network        = NeuralNet( settings )
training_set   = dataset
test_set       = dataset
cost_function  = cross_entropy_cost


RMSprop(
        network,                            # the network to train
        training_set,                      # specify the training set
        test_set,                          # specify the test set
        cost_function,                      # specify the cost function to calculate error

        ERROR_LIMIT             = .1,     # define an acceptable error limit
        max_iterations         = 10,      # continues until the error limit is reach if this argument is skipped
        # save_trained_network = True,
    )

import sys
if(len(sys.argv) > 1):
  filename = sys.argv[1]
else: filename = "trained.pkl"
print "saving network to file", filename
network.save_network_to_file( filename )

# a = [0, 1]
# b = [1, 0]
# prediction_set = [ Instance(a), Instance([1,0]) ]
# print a, b
# print network.predict( prediction_set )

print 'Now test the network with the test scripts"'
