# save a network's first layer weights
# as a wav file

import struct
def toBuffer(list):
    data = []
    for i in range( len(list) ):
        data.append( list[i] )
    return struct.pack('f'*len(data), *data)

import sys
if(len(sys.argv) > 1):
  filename = sys.argv[1]
else: filename = "trained.pkl"
print "loading network file", filename


from nntester import NnTester
nnTester = NnTester(filename)
data = nnTester.getLayerData()


import wave
# file = open(filename + ".wav", "wb")
# w = wave.open(file, 'w')
w = wave.open(filename + ".wav", 'w')
w.setnchannels(1)
w.setsampwidth(1)
w.setframerate(2000)
w.setnframes(len(data))
w.writeframesraw(toBuffer(data))
w.close()
