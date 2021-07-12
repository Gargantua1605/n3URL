import numpy as np
import mne

file = "../data/S001/S001R01.edf"
data = mne.io.read_raw_edf(file)
raw_data = data.get_data()

# you can get the metadata included in the file and a list of all channels:
info = data.info
channels = data.ch_names

print(info)
print(len(channels))
print(channels)
raw_data_array = np.array(raw_data)
print(raw_data_array)
print(np.shape(raw_data_array))
