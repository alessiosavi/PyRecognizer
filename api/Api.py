# -*- coding: utf-8 -*-
"""
Custom function that will be wrapped for be HTTP compliant
"""

import time
from datetime import datetime
from logging import getLogger

from datastructure.Response import Response
from utils.util import print_prediction_on_image, random_string, retrieve_dataset

log = getLogger()


def predict_image(img_path, clf, PREDICTION_PATH):
	"""

	:param PREDICTION_PATH: global variable where image recognized are saved
	:param img_path: image that have to be predicted
	:param clf: classifier in charge to predict the image
	:return: Response dictionary jsonizable
	"""
	response = Response()
	if clf is None:
		log.error("predict_image | FATAL | Classifier is None!")
		prediction = None
	else:
		log.debug("predict_image | Predicting {}".format(img_path))
		prediction = clf.predict(img_path)
		log.debug("predict_image | Result: {}".format(prediction))
	# Manage success
	if prediction and isinstance(prediction["predictions"], list):
		img_name = random_string() + ".png"
		log.debug("predict_image | Generated a random name: {}".format(img_name))
		log.debug("predict_image | Visualizing face recognition ...")
		print_prediction_on_image(img_path, prediction["predictions"], PREDICTION_PATH, img_name)
		return Response(status="OK", description=img_name, data=prediction).__dict__

	# Manage error
	elif prediction is None:
		response.error = "CLASSIFIER_NOT_LOADED"
		response.description = "Classifier is None | Training mandatory"
		log.error("predict_image | Seems that the classifier is not loaded :/")

	elif isinstance(prediction, list):
		if len(prediction) == 0:
			response.error = "NO_FACE_FOUND"
			response.description = "Seems that in this images there is no face :/"
			log.error("predict_image | Seems that in this images there is no face :/")

		elif len(prediction) > 1:
			response.error = "TOO_MANY_FACES"
			response.description = "Seems that in this images there are too many faces :/"
			log.error("predict_image | Seems that in this images there are too many faces :/")

	elif prediction == -1:
		# TODO: Add custom algorithm that "try to understand" who has never been recognized
		response.error = "FACE_NOT_RECOGNIZED"
		response.description = "Seems that this face is related to nobody that i've seen before ..."
		log.error("predict_image | Seems that this face is related to nobody that i've seen before ...")

	elif prediction == -2:
		response.error = "FILE_NOT_VALID"
		response.description = "Seems that the file that you have tried to upload is not valid ..."
		log.error("predict_image |Seems that the file that you have tried to upload is not valid ...")

	return response.__dict__


def train_network(folder_uncompress, zip_file, clf):
	"""
	Train a new neural model with the zip file provided
	:param folder_uncompress:
	:param zip_file:
	:param clf:
	:return:
	"""

	log.debug("train_network | Starting training phase ...")
	dataset = retrieve_dataset(folder_uncompress, zip_file, clf)

	if dataset is None:
		return Response(error="ERROR DURING LOADING DAT", description="Seems that the dataset is not valid").__dict__

	else:
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		neural_model_file, elapsed_time = clf.train(dataset["X"], dataset["Y"], timestamp)

		response = Response(status="OK", data=neural_model_file)
		response.description = "Model succesfully trained! | {}".format(
			time.strftime("%H:%M:%S.%f", time.gmtime(elapsed_time)))
		log.debug("train_network | Tuning phase finihsed! | {}".format(response.description))

		return response.__dict__


def tune_network(folder_uncompress, zip_file, clf):
	"""
	Train a new neural model with the zip file provided
	:param folder_uncompress:
	:param zip_file:
	:param clf:
	:return:
	"""
	log.debug("tune_network | Starting tuning phase ...")
	dataset = retrieve_dataset(folder_uncompress, zip_file, clf)

	if dataset is None:
		return Response(error="ERROR DURING LOADING DAT", description="Seems that the dataset is not valid").__dict__

	else:
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		neural_model_file, elapsed_time = clf.tuning(dataset["X"], dataset["Y"], timestamp)

		response = Response(status="OK", data=neural_model_file)
		response.description = "Model succesfully trained! | {}".format(
			time.strftime("%H:%M:%S.%f", time.gmtime(elapsed_time)))
		log.debug("train_network | Tuning phase finihsed! | {}".format(response.description))

		return response.__dict__
