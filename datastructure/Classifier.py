# -*- coding: utf-8 -*-
"""
Core utils for manage face recognition process
"""
import json
import logging
import os
import pickle
import time
from math import sqrt
from pprint import pformat

import face_recognition
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, \
	precision_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from tqdm import tqdm

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
		self.algorithm = None
		self.metric = None
		self.p = None
		self.weights = None
		self.peoples_list = []
		self.classifier = None

	def init_algorithm(self, algorithm):
		"""
		Initialize the algorithmrithm for the neural network. If not provided the 'ball_tree' will
		be used as default
		:param algorithm: 'ball_tree' as default
		"""
		log.debug("init_algorithm | Initializing knn algorithm ...")
		if self.algorithm is None:
			self.algorithm = algorithm

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
			if self.algorithm is not None and self.n_neighbors is not None:
				log.debug("init_classifier | Initializing a new classifier ... | {0}".format(pformat(self.__dict__)))
				self.classifier = KNeighborsClassifier(
					n_neighbors=self.n_neighbors, algorithm=self.algorithm, weights='distance')
			else:
				log.error("init_classifier | Mandatory parameter not provided | Init a new KNN Classifier")
				self.classifier = KNeighborsClassifier()

	def load_classifier_from_file(self, timestamp):
		"""
		Initalize the classifier from file.
		The classifier file rappresent the name of the directory related to the classifier that we want to load.

		The tree structure of the the model folder will be something like this

		 Structure:
		model/
		├── <20190520_095119>/  --> Timestamp in which the model was created
		│   ├── model.dat       -->  Dataset generated by encoding the faces and pickelizing them
		│   ├── model.clf       -->  Classifier delegated to recognize a given face
		│   ├── model.json      -->  Hyperparameters related to the current classifier
		├── <20190519_210950>/
		│   ├── model.dat
		│   ├── model.clf
		│   ├── model.json
		└── ...

		:param timestamp:
		:return:
		"""
		log.debug("load_classifier_from_file | Loading classifier from file ... | File: {}".format(timestamp))

		# Load a trained KNN model (if one was passed in)
		err = None
		if self.classifier is None:
			if self.model_path is None or not os.path.isdir(self.model_path):
				raise Exception("Model folder not provided!")
			# Adding the conventional name used for the classifier -> 'model.clf'
			filename = os.path.join(self.model_path, timestamp, "model.clf")
			log.debug("load_classifier_from_file | Loading classifier from file: {}".format(filename))
			if os.path.isfile(filename):
				log.debug("load_classifier_from_file | File {} exist!".format(filename))
				with open(filename, 'rb') as f:
					self.classifier = pickle.load(f)
				log.debug("load_classifier_from_file | Classifier loaded!")
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

	def train(self, X, Y, timestamp):
		"""
		Train a new model by the given data [X] related to the given target [Y]
		:param X:
		:param Y:
		:param timestamp:
		"""
		log.debug("train | START")
		if self.classifier is None:
			self.init_classifier()

		dump_dataset(X, Y, os.path.join(self.model_path, timestamp))

		start_time = time.time()

		X_train, x_test, Y_train, y_test = train_test_split(X, Y, test_size=0.25)
		log.debug("train | Training ...")
		self.classifier.fit(X_train, Y_train)
		log.debug("train | Model Trained!")
		log.debug("train | Checking performance ...")
		y_pred = self.classifier.predict(x_test)
		# Static method
		self.verify_performance(y_test, y_pred)

		return self.dump_model(timestamp=timestamp, classifier=self.classifier), time.time() - start_time

	def tuning(self, X, Y, timestamp):
		"""
		Tune the hyperparameter of a new model by the given data [X] related to the given target [Y]

		:param X:
		:param Y:
		:param timestamp:
		:return:
		"""
		start_time = time.time()
		dump_dataset(X, Y, os.path.join(self.model_path, timestamp))

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
			'n_neighbors': [nn_root],
			'metric': metrics_range,
			'weights': weights_range,
			'algorithm': algorithm_range,
			'p': power_range,
		}
		log.debug("tuning | Parameter -> {}".format(pformat(parameter_space)))
		grid = GridSearchCV(self.classifier, parameter_space, cv=3, scoring='accuracy', verbose=20, n_jobs=2)
		grid.fit(X_train, Y_train)
		log.info("TUNING COMPLETE | DUMPING DATA!")
		# log.info("tuning | Grid Scores: {}".format(pformat(grid.grid_scores_)))
		log.info('Best parameters found: {}'.format(grid.best_params_))

		y_pred = grid.predict(x_test)

		log.info('Results on the test set: {}'.format(pformat(grid.score(x_test, y_test))))

		self.verify_performance(y_test, y_pred)

		return self.dump_model(timestamp=timestamp, params=grid.best_params_,
		                       classifier=grid.best_estimator_), time.time() - start_time

	@staticmethod
	def verify_performance(y_test, y_pred):
		"""
		Verify the performance of the result analyzing the known-predict result
		:param y_test:
		:param y_pred:
		:return:
		"""

		log.debug("verify_performance | Analyzing performance ...")
		log.info("Classification Report: {}".format(pformat(classification_report(y_test, y_pred))))
		log.info("balanced_accuracy_score: {}".format(pformat(balanced_accuracy_score(y_test, y_pred))))
		log.info("accuracy_score: {}".format(pformat(accuracy_score(y_test, y_pred))))
		log.info("precision_score: {}".format(pformat(precision_score(y_test, y_pred, average='weighted'))))

	def dump_model(self, timestamp, classifier, params=None, path=None):
		"""
		Dump the model to the given path, file
		:param params:
		:param timestamp:
		:param classifier:
		:param path:

		"""
		log.debug("dump_model | Dumping model ...")
		if path is None:
			if self.model_path is not None:
				if os.path.exists(self.model_path) and os.path.isdir(self.model_path):
					path = self.model_path
		config = {'classifier_file': os.path.join(timestamp, "model.clf"),
		          'params': params
		          }
		if not os.path.isdir(path):
			os.makedirs(timestamp)
		classifier_folder = os.path.join(path, timestamp)
		classifier_file = os.path.join(classifier_folder, "model")

		log.debug("dump_model | Dumping model ... | Path: {} | Model folder: {}".format(path, timestamp))
		if not os.path.exists(classifier_folder):
			os.makedirs(classifier_folder)

		with open(classifier_file + ".clf", 'wb') as f:
			pickle.dump(classifier, f)
			log.info('dump_model | Model saved to {0}.clf'.format(classifier_file))

		with open(classifier_file + ".json", 'w') as f:
			json.dump(config, f)
			log.info('dump_model | Configuration saved to {0}.json'.format(classifier_file))

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
		# pool = ThreadPool(3)
		# self.peoples_list = pool.map(self.init_peoples_list_core, os.listdir(self.training_dir))

		for people_name in tqdm(os.listdir(self.training_dir),
		                        total=len(os.listdir(self.training_dir)), desc="Init people list ..."):
			self.peoples_list.append(self.init_peoples_list_core(people_name))

		self.peoples_list = list(filter(None.__ne__, self.peoples_list))  # Remove None

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
		return DATASET

	# TODO: Add configuration parameter for choose the distance_threshold
	def predict(self, X_img_path, distance_threshold=0.56):
		"""
		Recognizes faces in given image using a trained KNN classifier

		:param X_img_path: path to image to be recognized
		:param distance_threshold: (optional) distance threshold for face classification. the larger it is,
		the more chance of mis-classifying an unknown person as a known one.
		:return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
			For faces of unrecognized persons, the name 'unknown' will be returned.
		"""

		if self.classifier is None:
			log.error("predict | Be sure that you have loaded/trained the nerual network model")
			return None

		# Load image data in a numpy array
		try:
			log.debug("predict | Loading image {}".format(X_img_path))
			# TODO: Necessary cause at this point we are not sure what file type is this ...
			X_img = face_recognition.load_image_file(X_img_path)
		except OSError:
			log.error("predict | What have you uploaded ???")
			return -2
		# TODO: Manage multiple faces
		log.debug("predict | Extracting faces locations ...")
		X_face_locations = face_recognition.face_locations(X_img)
		log.debug("predict | Found {} face(s) for the given image".format(len(X_face_locations)))

		# If no faces are found in the image, or more than one face are found, return an empty result.
		if len(X_face_locations) == 0:
			log.warning("predict | Seems that no faces was found :( ")
			return []

		# Find encodings for faces in the test iamge
		log.debug("predict | Encoding faces ...")
		faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations, num_jitters=2)
		log.debug("predict | Face encoded! | Let's ask to the neural network ...")
		# Use the KNN model to find the best matches for the test face
		closest_distances = self.classifier.kneighbors(faces_encodings)
		log.debug("predict | Closest distances: [{}]".format(len(closest_distances)))
		# At least we need to recognize 1 face
		scores = []
		for i in range(len(closest_distances[0])):
			scores.append(min(closest_distances[0][i]))
			log.debug("predict | *****MIN****| {}".format(min(closest_distances[0][i])))


		predictions = []
		if len(scores) > 0:
			for pred, loc, score in zip(self.classifier.predict(faces_encodings), X_face_locations, scores):
				if distance_threshold > score :
					log.warning("predict | Person {} does not outbounds treshold {}>{}".format(pred,score,distance_threshold))
					predictions = []
				else:
					log.debug("predict | Pred: {} | Loc: {} | Score: {}".format(pred, loc, score))
					predictions.append((pred, loc))
			log.debug("predict | Prediction: {}".format(predictions))
		else:
			log.debug("predict | Face not recognized :/")
			predictions = -1

		return {"predictions": predictions, "scores": scores}
