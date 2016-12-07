

Requirements
* `sudo pip install nimblenet soundfile sounddevice`
* on fedora you will want `sudo dnf install pyaudio`


Test the beast:

* record .ogg audio files of yourself saying many words, and several times hello
* call them with "bonjour" in the name if they have "bonjour" in it
* put them in train or test folder

```
$ python train-bonjour.py
```

example output
```
$ python train-bonjour.py
16 sounds of size 718830
[training] Finished:
[training]   Converged to error bound (1e-20) with error 0.2189.
[training]   Measured quality: 0.9861
[training]   Trained for 500 epochs.
test/audio1.ogg [[ 0.99923126]]

```

this means:

> 16 sounds of size 718830

16 sounds in input

> [training] Finished:
> [training]   Converged to error bound (1e-20) with error 0.2189.
> [training]   Measured quality: 0.9861
> [training]   Trained for 500 epochs.

trained the neural net

> test/audio1.ogg [[ 0.99923126]]

I have put only 1 file in test and it has 99% chances of having hello in it

For now I have achieved a good accuracy if each file has only one word
