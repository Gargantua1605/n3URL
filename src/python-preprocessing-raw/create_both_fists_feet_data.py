import os
import numpy as np
import matplotlib.pyplot as plt
import mne

event_id = dict(both_fists=1, both_feet=2)
runs = [6, 10, 14] 

eeg_data_both_fists = []
eeg_data_both_feet = []

subjects = [i for i in range(1, 110, 1)]
for run in runs:
	for subject in subjects:
		raw_fnames = mne.datasets.eegbci.load_data(subject, run)
		raw = mne.io.read_raw_edf(raw_fnames[0], preload=True)
		mne.datasets.eegbci.standardize(raw)

		montage = mne.channels.make_standard_montage('standard_1005')
		raw.set_montage(montage)

		raw.filter(8., 30., fir_design='firwin', skip_by_annotation='edge')

		sfreq = raw.info['sfreq']
		tmin, tmax = 0. + 1 / sfreq, 4.

		events, _ = mne.events_from_annotations(raw, event_id=dict(T1=1, T2=2))
		picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude='bads')

		epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks, baseline=None, preload=True)

		both_fists = epochs['both_fists']
		both_feet = epochs['both_feet']

		subject_eeg_data_both_fists = both_fists.get_data(picks=['FC3', 'FC4'])
		subject_eeg_data_both_feet = both_feet.get_data(picks=['FC3', 'FC4'])

		for data in subject_eeg_data_both_fists:
			if data.shape[1] == 640:
				eeg_data_both_fists.append(data)

		for data in subject_eeg_data_both_feet:
			if data.shape[1] == 640:
				eeg_data_both_feet.append(data)

both_fists_data = np.stack(eeg_data_both_fists)
both_feet_data = np.stack(eeg_data_both_feet)

print(both_fists_data.shape)
print(both_feet_data.shape)

both_fists = np.reshape(both_fists_data, (both_fists_data.shape[0], both_fists_data.shape[2], both_fists_data.shape[1]))
both_feet = np.reshape(both_feet_data, (both_feet_data.shape[0], both_feet_data.shape[2], both_feet_data.shape[1]))

print(both_fists.shape)
print(both_feet.shape)

print(both_fists[0, :, :])
print(both_feet[0, :, :])

reshaped_both_fists = both_fists.reshape(both_fists.shape[0], -1)
np.savetxt("both_fists_data.txt", reshaped_both_fists)

reshaped_both_feet = both_feet.reshape(both_feet.shape[0], -1)
np.savetxt("both_feet_data.txt", reshaped_both_feet)