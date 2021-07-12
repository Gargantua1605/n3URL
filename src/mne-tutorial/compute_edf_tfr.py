import os
import numpy as np
import matplotlib.pyplot as plt
import mne

tmin, tmax = -1., 4.
event_id = dict(rest=1, left=2, right=3)
runs = [4, 8, 12] # motor imagery: rest vs left hand vs right hand

eeg_tfr_rest = []
eeg_tfr_right = []
eeg_tfr_left = []

subjects = [i for i in range(1, 3, 1)]
for run in runs:
	for subject in subjects:
		raw_fnames = mne.datasets.eegbci.load_data(subject, run)
		raw = mne.io.read_raw_edf(raw_fnames[0], preload=True)
		mne.datasets.eegbci.standardize(raw)

		montage = mne.channels.make_standard_montage('standard_1005')
		raw.set_montage(montage)

		raw.filter(8., 30., fir_design='firwin', skip_by_annotation='edge')
		# raw.plot_psd(fmax=50)

		events, _ = mne.events_from_annotations(raw, event_id=dict(T0=1, T1=2, T2=3))
		picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude='bads')

		sfreq = raw.info['sfreq']
		epochs = mne.Epochs(raw, events, event_id, tmin, tmax - 1 / sfreq, proj=True, picks=picks, baseline=None, preload=True)

		rest_epochs = epochs['rest']
		right_epochs = epochs['right']
		left_epochs = epochs['left']

		frequencies = np.arange(8, 30, 0.50)
		time = np.arange(tmin, tmax, 1 / sfreq)

		rest_power = mne.time_frequency.tfr_array_morlet(rest_epochs, sfreq=sfreq, freqs=frequencies, n_cycles=7.0, output='power')
		right_power = mne.time_frequency.tfr_array_morlet(right_epochs, sfreq=sfreq, freqs=frequencies, n_cycles=7.0, output='power')
		left_power = mne.time_frequency.tfr_array_morlet(left_epochs, sfreq=sfreq, freqs=frequencies, n_cycles=7.0, output='power')
		# print(power.shape)

		for power in rest_power:
			if power.shape[2] == 800:
				eeg_tfr_rest.append(power)
			# eeg_tfr_rest.append(power)

		for power in right_power:
			if power.shape[2] == 800:
				eeg_tfr_right.append(power)
			# eeg_tfr_right.append(power)

		for power in left_power:
			if power.shape[2] == 800:
				eeg_tfr_left.append(power)
			# eeg_tfr_left.append(power)

		# power_epoch = power[0, :, :, :]
		# TFR_epoch = mne.time_frequency.AverageTFR(raw.info, power_epoch, times=time, freqs=frequencies, nave=1)
		# TFR_epoch.plot(picks=['FC3'], title='FC3')

		# print(power_epoch)

		# plt.show()

tfr_rest = np.stack(eeg_tfr_rest)
tfr_right = np.stack(eeg_tfr_right)
tfr_left = np.stack(eeg_tfr_left)

print(tfr_rest.shape)
print(tfr_right.shape)
print(tfr_left.shape)

np.save('tfr_rest_01', tfr_rest)
np.save('tfr_right_01', tfr_right)
np.save('tfr_left_01', tfr_left)