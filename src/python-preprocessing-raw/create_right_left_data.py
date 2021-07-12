import os
import numpy as np
import matplotlib.pyplot as plt
import mne

event_id = dict(rest=1, left=2, right=3)
runs = [4, 8, 12] # motor imagery: rest vs left hand vs right hand

eeg_data_rest = []
eeg_data_right = []
eeg_data_left = []

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

		events, _ = mne.events_from_annotations(raw, event_id=dict(T0=1, T1=2, T2=3))
		picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude='bads')

		epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks, baseline=None, preload=True)

		rest_epochs = epochs['rest']
		right_epochs = epochs['right']
		left_epochs = epochs['left']

		subject_eeg_data_rest = rest_epochs.get_data(picks=['FC3', 'FC4'])
		subject_eeg_data_right = right_epochs.get_data(picks=['FC3', 'FC4'])
		subject_eeg_data_left = left_epochs.get_data(picks=['FC3', 'FC4'])

		for data in subject_eeg_data_rest:
			if data.shape[1] == 640:
				eeg_data_rest.append(data)

		for data in subject_eeg_data_right:
			if data.shape[1] == 640:
				eeg_data_right.append(data)

		for data in subject_eeg_data_left:
			if data.shape[1] == 640:
				eeg_data_left.append(data)

rest_data = np.stack(eeg_data_rest)
right_data = np.stack(eeg_data_right)
left_data = np.stack(eeg_data_left)

print(rest_data.shape)
print(right_data.shape)
print(left_data.shape)

rest = np.reshape(rest_data, (rest_data.shape[0], rest_data.shape[2], rest_data.shape[1]))
right = np.reshape(right_data, (right_data.shape[0], right_data.shape[2], right_data.shape[1]))
left = np.reshape(left_data, (left_data.shape[0], left_data.shape[2], left_data.shape[1]))

print(rest.shape)
print(right.shape)
print(left.shape)

print(rest[0, :, :])
print(right[0, :, :])
print(left[0, :, :])

reshaped_rest = rest.reshape(rest.shape[0], -1)
np.savetxt("rest_data.txt", reshaped_rest)

reshaped_right = right.reshape(right.shape[0], -1)
np.savetxt("right_data.txt", reshaped_right)

reshaped_left = left.reshape(left.shape[0], -1)
np.savetxt("left_data.txt", reshaped_left)

# load_rest = np.loadtxt("rest_data.txt")
# load_right = np.loadtxt("right_data.txt")
# load_left = np.loadtxt("left_data.txt")

# load_rest_reshaped = np.reshape(load_rest, (load_rest.shape[0], load_rest.shape[1] // rest.shape[2], rest.shape[2]))
# if (load_rest_reshaped == rest).all():
	# print("YES")
# else:
	# print("NO")

# load_right_reshaped = np.reshape(load_right, (load_right.shape[0], load_right.shape[1] // right.shape[2], right.shape[2]))
# if (load_right_reshaped == right).all():
	# print("YES")
# else:
	# print("NO")

# load_left_reshaped = np.reshape(load_left, (load_left.shape[0], load_left.shape[1] // left.shape[2], left.shape[2]))
# if (load_left_reshaped == left).all():
	# print("YES")
# else:
	# print("NO")