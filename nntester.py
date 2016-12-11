from nimblenet.data_structures import Instance
from nimblenet.neuralnet import NeuralNet

class NnTester:
    def __init__(self, filename):
        self.network = NeuralNet.load_network_from_file( filename )
        self.sound_max_size = self.network.n_inputs

    def getScore(self, data):
        if len(data) != self.sound_max_size:
            print 'Error, data buffer must be the same size as the network'
            return -1
        return self.network.predict( [ Instance(data) ] )[0][0]
    def getLayerData(self):
      return self.network.get_weights()
