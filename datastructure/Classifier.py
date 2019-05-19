# -*- coding: utf-8 -*-
"""
Core utils for manage face recognition process
"""
import json
import logging
import os
import pickle
from datetime import datetime
from math import sqrt
from multiprocessing.pool import ThreadPool
from pprint import pformat

import face_recognition
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, \
	precision_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier

from datastructure.Person import Person
from utils.util import dump_dataset

log = logging.getLogger()


class Classifier(object):
	"""
	Store the knowledge related to the people faces
	"""

	def __init__(self):
		self.training_dir = None
		self.model_path = None
		self.n_neighbors = None
		self.knn_algo = None
		self.peoples_list = []
		self.classifier = None

	def init_knn_algo(self, knn_algo):
		"""
		Initialize the knn_algorithm for the neural network. If not provided the 'ball_tree' will
		be used as default
		:param knn_algo: 'ball_tree' as default
		"""
		log.debug("init_knn_algo | Initializing knn algorithm ...")
		if self.knn_algo is None:
			self.knn_algo = knn_algo

	def init_n_neighbors(self, X_len=10):
		"""
		Initalize the n_neighbors parameter

		:param X_len:
		"""
		log.debug("init_n_neighbors | Initializing neighbors number ...")
		if self.n_neighbors is None:
			self.n_neighbors = int(round(sqrt(X_len)))
		log.debug("init_n_neighbors | Choosed {0} n_neighbors".format(self.n_neighbors))

	def init_classifier(self):
		"""
		Initialize a new classifier after be sure that necessary data are initalized
		"""
		if self.classifier is None:
			log.debug("init_classifier | START!")
			if self.knn_algo is not None and self.n_neighbors is not None:
				log.debug("init_classifier | Initializing a new classifier ... | {0}".format(pformat(self.__dict__)))
				self.classifier = KNeighborsClassifier(
					n_neighbors=self.n_neighbors, algorithm=self.knn_algo, weights='distance')
			else:
				log.error("init_classifier | Mandatory parameter not provided :/")
				self.classifier = None

	def init_specs(self, X_len, knn_algo='ball_tree'):
		"""
		Initalize the classifier
		:param knn_algo:
		:param X_len:
		"""
		log.debug("init_specs | Init knn algorithm ...")
		self.init_knn_algo(knn_algo)
		self.init_n_neighbors(X_len)
		self.init_classifier()

	def load_classifier_from_file(self, classifier_file):
		"""
		Initalize the classifier from file
		:param classifier_file:
		:return:
		"""
		log.debug("load_classifier_from_file | Loading classifier from file ... | File: {}".format(classifier_file))

		# Load a trained KNN model (if one was passed in)
		err = None
		if self.classifier is None:
			if self.model_path is None or not os.path.isdir(self.model_path):
				raise Exception("Model folder not provided!")
			log.debug("load_classifier_from_file | Loading classifier from file ...")
			log.debug("load_classifier_from_file | Path {} exist ...".format(self.model_path))
			filename = os.path.join(self.model_path, classifier_file)
			if os.path.isfile(filename):
				log.debug("load_classifier_from_file | File {} exist ...".format(filename))
				with open(filename, 'rb') as f:
					self.classifier = pickle.load(f)
			else:
				err = "load_classifier_from_file | FATAL | File {} DOES NOT EXIST ...".format(filename)
		else:
			err = "load_classifier_from_file | FATAL | Path {} DOES NOT EXIST ...".format(self.model_path)
		if err is not None:
			log.error(err)
			log.error("load_classifier_from_file | Seems that the model is gone :/ | Loading an empty classifier for "
			          "training purpouse ...")
			self.classifier = None
		return

	def train(self, X, Y):
		"""
		Train a new model by the given data [X] related to the given target [Y]
		:param X:
		:param Y:
		"""
		log.debug("train | START")
		if self.classifier is not None:
			log.debug("train | Training ...")
			X_train, x_test, Y_train, y_test = train_test_split(X, Y, test_size=0.25)
			self.classifier.fit(X_train, Y_train)
			log.debug("train | Model Trained!")
			log.debug("train | Checking performance ...")
			y_pred = self.classifier.predict(x_test)
			# Static method
			self.verify_performance(y_test, y_pred)
			return self.dump_model(self.model_path, "model")

	def tuning(self, X, Y):
		"""
		Tune the hyperparameter of a new model by the given data [X] related to the given target [Y]

		:param X:
		:param Y:
		:return:
		"""
		X_train, x_test, Y_train, y_test = train_test_split(X, Y, test_size=0.25)
		self.classifier = KNeighborsClassifier()
		# Hyperparameter of the neural network (KKN)

		# n_neighbors_range = list(range(1, round(sqrt(len(X_train)))))  # n_neighbors <= n_samples
		weights_range = ['uniform', 'distance']
		metrics_range = ['minkowski', 'euclidean', 'manhattan']
		# 'auto' will automagically choose an algorithm by the given value
		algorithm_range = ['ball_tree', 'kd_tree', 'brute']
		power_range = [1, 2]
		nn_root = int(round(sqrt(len(X_train))))
		parameter_space = {
			# 'n_neighbors': list(range(1,nn_root)),
			'n_neighbors': [nn_root],
			'metric': metrics_range,
			'weights': weights_range,
			'algorithm': algorithm_range,
			'p': power_range,
		}
		log.debug("tuning | Parameter -> {}".format(pformat(parameter_space)))
		grid = GridSearchCV(self.classifier, parameter_space, cv=3, scoring='accuracy', verbose=10, n_jobs=3)
		grid.fit(X_train, Y_train)
		log.info("TUNING COMPLETE | DUMPING DATA!")
		# log.info("tuning | Grid Scores: {}".format(pformat(grid.grid_scores_)))
		log.info('Best parameters found: {}'.format(grid.best_params_))

		y_pred = grid.predict(x_test)

		log.info('Results on the test set: {}'.format(pformat(grid.score(x_test, y_test))))

		self.verify_performance(y_test, y_pred)

		return self.dump_model(params=grid.best_params_)

	@staticmethod
	def verify_performance(y_test, y_pred):
		"""
		Verify the performance of the result analyzing the known-predict result
		:param y_test:
		:param y_pred:
		:return:
		"""

		log.debug("verify_performance | Analyzing performance ...")
		# log.info("Computing classifier score --> {}".format(pformat(clf.score(y_test,y_pred))))
		log.info("Classification Report: {}".format(pformat(classification_report(y_test, y_pred))))
		log.info("balanced_accuracy_score: {}".format(pformat(balanced_accuracy_score(y_test, y_pred))))
		log.info("accuracy_score: {}".format(pformat(accuracy_score(y_test, y_pred))))
		log.info("precision_score: {}".format(pformat(precision_score(y_test, y_pred, average='weighted'))))

	def dump_model(self, params, path=None, file=None):
		"""
		Dump the model to the given path, file
		:param params:
		:param path:
		:param file:
		"""
		if path is None:
			if self.model_path is not None:
				if os.path.exists(self.model_path) and os.path.isdir(self.model_path):
					path = self.model_path
		if file is None:
			file = "model"

		if os.path.isdir(path):
			time_parsed = datetime.now().strftime('%Y%m%d_%H%M%S')
			classifier_file = os.path.join(path, "{}-{}".format(file, time_parsed))
			config = {'classifier_file': classifier_file,
			          'params': params
			          }

			log.debug("dump_model | Dumping model ... | Path: {} | File: {}".format(path, classifier_file))
			# TODO: Save every model in a different folder
			with open(classifier_file + ".clf", 'wb') as f:
				pickle.dump(self.classifier, f)
			with open(classifier_file + ".json", 'w') as f:
				json.dump(config, f)
				log.info('dump_model | Configuration saved to {0}'.format(classifier_file))

			return config

	def init_peoples_list(self, peoples_path=None):
		"""
		This method is delegated to iterate among the folder that contains the peoples's face in order to
		initalize the array of peoples
		:return:
		"""

		log.debug("init_peoples_list | Initalizing people ...")
		if peoples_path is not None and os.path.isdir(peoples_path):
			self.training_dir = peoples_path
		# freq_list = pool.map(partial(get_frequency, nlp=nlp_en, client=mongo_client), fileList)
		pool = ThreadPool(3)
		self.peoples_list = pool.map(self.init_peoples_list_core, os.listdir(self.training_dir))
		self.peoples_list = list(filter(None.__ne__, self.peoples_list))  # Remove None

	# TODO: Add method for dump datastructure in order to don't wait to load same data for test

	def init_peoples_list_core(self, people_name):
		"""
		Delegated core method for parallelize operation
		:param people_name:
		:return:
		"""
		if os.path.isdir(os.path.join(self.training_dir, people_name)):
			log.debug("Initalizing people {0}".format(os.path.join(self.training_dir, people_name)))
			person = Person()
			person.name = people_name
			person.path = os.path.join(self.training_dir, people_name)
			person.init_dataset()
			return person
		else:
			log.debug("People {0} invalid folder!".format(os.path.join(self.training_dir, people_name)))
			return None

	def init_dataset(self):
		"""
		Initialize a new dataset joining all the data related to the peoples list
		:return:
		"""
		DATASET = {
			# Image data (numpy array)
			"X": [],
			# Person name
			"Y": []
		}

		for people in self.peoples_list:
			log.debug(people.name)
			for item in people.dataset["X"]:
				DATASET["X"].append(item)
			for item in people.dataset["Y"]:
				DATASET["Y"].append(item)
		dump_dataset(DATASET, self.model_path)
		return DATASET

	# TODO: Add configuration parameter for choose the distance_threshold
	def predict(self, X_img_path, distance_threshold=0.45):
		"""
		Recognizes faces in given image using a trained KNN classifier

		:param X_img_path: path to image to be recognized
		:param distance_threshold: (optional) distance threshold for face classification. the larger it is,
		the more chance of mis-classifying an unknown person as a known one.
		:return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
			For faces of unrecognized persons, the name 'unknown' will be returned.
		"""

		if self.classifier is None:
			log.error("predict | Be sure that you have loaded/trained a nerual model")
			return None

		# Load image file and find face locations
		try:
			# TODO: Necessary cause at this point we are not sure what file type is this ...
			X_img = face_recognition.load_image_file(X_img_path)
		except OSError:
			log.error("predict | What have you uploaded ???")
			return -2
		X_face_locations = face_recognition.face_locations(X_img)

		# If no faces are found in the image, or more than one face are found, return an empty result.
		if len(X_face_locations) != 1:
			return []

		# Find encodings for faces in the test iamge
		faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

		# Use the KNN model to find the best matches for the test face
		closest_distances = self.classifier.kneighbors(faces_encodings, n_neighbors=1)
		log.debug("predict | Closest distances: {}".format(closest_distances))
		are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
		log.debug("predict | are_matches: {}".format(are_matches))

		prediction = []
		for pred, loc, rec in zip(self.classifier.predict(faces_encodings), X_face_locations, are_matches):
			log.debug("predict_folder | Pred: {} | Loc: {} | Rec: {}".format(pred, loc, rec))
			if rec:  # Face recognized !
				prediction.append((pred, loc))
			else:
				log.debug("predict | Face {} not recognized :/".format(pred))
				prediction = -1
		log.debug("predict_folder | Prediction: {}".format(prediction))

		return prediction
