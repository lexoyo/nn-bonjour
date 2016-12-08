#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!

WARNING: This works only in Python 3.x!

"""
import argparse
import time
import tempfile
from multiprocessing import Queue
from Queue import Empty


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()

try:
    import sounddevice as sd
    import soundfile as sf
    from random import randint

    if args.list_devices:
        print(sd.query_devices())
        parser.exit()
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])
    print("#" * 80)
    if args.filename is None:
        if(randint(0,100)>50):
            print "Say something WITH bonjour"
            prefix = 'bonjour_'
        else:
            print "Say something WITHOUT bonjour"
            prefix = 'rec_'
        if(randint(0,100)>50):
            print "This will be used as training data"
            dir = 'train/'
        else:
            print "This will be used as test data"
            dir = 'test/'
        args.filename = tempfile.mktemp(prefix=prefix, suffix='.wav', dir=dir)
    queue = Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status)
        queue.put(indata.copy())

    startTime = time.time()
    lastPrompt = 0
    maxTime = 5
    with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype=args.subtype) as file:
        with sd.InputStream(samplerate=args.samplerate, device=args.device,
                            channels=args.channels, callback=callback):
            print("recording now for %is"%maxTime)
            print("#" * 80)
            while True:
                curTime = time.time()
                if(curTime - lastPrompt > 1):
                    print maxTime - round(curTime - startTime, 0)
                    lastPrompt = curTime
                if(curTime - startTime > maxTime):
                    raise ValueError("Time's up!")
                file.write(queue.get())



except ValueError:
    parser.exit('\nRecording finished: ' + repr(args.filename))
except KeyboardInterrupt:
    parser.exit('\nRecording finished: ' + repr(args.filename))
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
