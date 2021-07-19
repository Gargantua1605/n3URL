import numpy as np
import tensorflow as tf
import keras
from keras.models import model_from_json

class EEGClassifier:
	actions = ['right', 'left']

	def __init__(self, model_json_file, model_h5_file):
		# load model from the JSON file
		json_file = open(model_json_file, 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.model = model_from_json(loaded_model_json)

		# load model weights
		self.model.load_weights(model_h5_file)
		print("Loaded model from disk")

		# self.model._make_predict_function()

	def classify_thought(self, epoched_data):
		self.prediction = self.model.predict(epoched_data)
		return EEGClassifier.actions[np.argmax(self.prediction)]
