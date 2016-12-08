#!/usr/bin/env python3

import numpy as np
import soundfile as sf
import sounddevice as sd
import os
import time
import sys


if(len(sys.argv) > 1):
  filename = sys.argv[1]
else: filename = "trained.pkl"
print "loading network to file", filename
success = 0
total = 0

from nntester import NnTester
nnTester = NnTester(filename)

for dirname, dirnames, filenames in os.walk('test'):
    for filename in filenames:
        path = os.path.join(dirname, filename)
        if(path.find('.keep') == -1):
            # test the nn
            sig, fs = sf.read(path)
            if(len(sig.shape) > 1):
                sig.shape = (len(sig.shape) * len(sig)) # from (245196, 2) to (490392,)
            if(nnTester.sound_max_size > len(sig)):
                sig = np.concatenate((sig, np.zeros((nnTester.sound_max_size - len(sig)))))
            elif(nnTester.sound_max_size < len(sig)):
                sig = sig[:nnTester.sound_max_size]
                print '<warning the sound is cut>'
            prediction = nnTester.getScore(sig)
            # print path, ' => ', prediction
            total += 1
            if(prediction > .6):
                if(path.find('bonjour') != -1):
                    print path, '\t\t\t', round(prediction, 2), '\t\t\t', u'\u2713'
                    success += 1
                else: print path, '\t\t\t', round(prediction, 2), '\t\t\tx'
            elif(prediction < .4):
                if(path.find('bonjour') == -1):
                    print path, '\t\t\t', round(prediction, 2), '\t\t\t', u'\u2713'
                    success += 1
                else: print path, '\t\t\t', round(prediction, 2), '\t\t\tx'
            else:
                print path, '\t\t\t', round(prediction, 2), '\t\t\t?'
            # play the sound
            sig, fs = sf.read(path)
            sd.play(sig, fs, blocking=True)

print '**********************'
print 'score:', success, ' / ', total



