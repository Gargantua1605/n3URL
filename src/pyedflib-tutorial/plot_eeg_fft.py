import pyedflib
import numpy as np
from scipy.fft import fft, fftfreq
import pywt
import matplotlib.pyplot as plt

file_name = "../data/S001/S001R01.edf"
file = pyedflib.EdfReader(file_name)

n = file.signals_in_file # Stores the number of EEG channels
# print("Number of EEG channels", n)

signal_labels = file.getSignalLabels() # List of the n EEG electrodes  
# print("This is the list of n channels: ")
# print(signal_labels)

sigbufs = np.zeros((n, file.getNSamples()[0])) # file.getNSamples()[0] returns the length of each recording	
for i in np.arange(n):
	sigbufs[i, :] = file.readSignal(i)

# print("Find below the actual EEG data stored in the form of a numpy array")
# print(sigbufs)

# print("The length of each channel recording is", file.getNSamples()[0]) # the square brackets are to index into the n channels

sampling_frequency = file.getSampleFrequency(chn=0) # Returns a list containing the sampling frequency of each track
# print("The signals have been sampled at", sampling_frequency)

N = file.getNSamples()[0] # Number of data samples
# print("The number of samples is", N)

fig, axs = plt.subplots(3)
fig.tight_layout()
for i in np.arange(3):
	axs[i].plot(sigbufs[i, :])
	axs[i].set_title(signal_labels[i])

# fig.savefig('../data/S001/S001R01_time.png')

xf = fftfreq(N, 1 / sampling_frequency) # Generate the frequency bins for the FFT plot
fig, axs = plt.subplots(3)
fig.tight_layout()
for i in np.arange(3):
	yf = fft(sigbufs[i, :]) # Compute the FFT
	axs[i].plot(xf, np.abs(yf))
	axs[i].set_title(signal_labels[i])

# fig.savefig('../data/S001/S001R01_fft.png')

plt.show()