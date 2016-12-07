import numpy as np
import soundfile as sf
import sounddevice as sd
import os
import time

from nimblenet.activation_functions import sigmoid_function
from nimblenet.cost_functions import cross_entropy_cost
from nimblenet.learning_algorithms import RMSprop
from nimblenet.data_structures import Instance
from nimblenet.neuralnet import NeuralNet

network = NeuralNet.load_network_from_file( "trained.pkl" )
sound_max_size = network.n_inputs
for dirname, dirnames, filenames in os.walk('test'):
    for filename in filenames:
        path = os.path.join(dirname, filename)
        if(path.find('.keep') == -1):
            # test the nn
            sig, fs = sf.read(path)
            if(len(sig.shape) > 1):
                sig.shape = (len(sig.shape) * len(sig)) # from (245196, 2) to (490392,)
            if(sound_max_size > len(sig)):
                sig = np.concatenate((sig, np.zeros((sound_max_size - len(sig)))))
            elif(sound_max_size < len(sig)):
                sig = sig[:sound_max_size]
                print 'warning the sound is cut: '
            print path, network.predict( [ Instance(sig) ] )
            # play the sound
            # sig, fs = sf.read(path)
            # sd.play(sig, fs)
            # time.sleep(5)
