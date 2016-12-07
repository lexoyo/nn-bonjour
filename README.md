

Requirements
* `sudo pip install nimblenet soundfile sounddevice`
* on fedora you will want `sudo dnf install pyaudio`


Test the beast:

* record .ogg audio files of yourself saying many words, and several times hello
* call them with "bonjour" in the name if they have "bonjour" in it
* put them in `train/` or `test/` folder

train the network with the ogg files in `train/` (this may take a long time)

```
$ python train-bonjour.py
16 sounds of size 718830
[training] Finished:
[training]   Converged to error bound (1e-20) with error 0.2189.
[training]   Measured quality: 0.9861
[training]   Trained for 500 epochs.
```

> 16 sounds of size 718830

this means that 16 sounds are used as input for training and the longest sample is 718830 bytes long so this is also the number of neurons in the input layer


and then test the network on the ogg files in `test/`

```
$ python test-ogg.py
test/audio1.ogg [[ 0.99923126]]
```


> test/audio1.ogg [[ 0.99923126]]

this means that I have put only 1 file in test and it has 99% chances of having "bonjour" in it


```
$ python test-mic.py
stream config: device= None  - channels= 1  - samplerate= 44100.0
>     0.09
>     0.04
>     0.56
```

this will display the microphone input wave and test it with the displayed data as input of the network

>     0.09
>     0.04
>     0.56

these are the percentage of chance that "bonjour" is in the data, displayed in "real time"
