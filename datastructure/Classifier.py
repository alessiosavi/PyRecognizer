# -*- coding: utf-8 -*-
"""
Core utils for manage face recognition process
"""

import logging
import os
import pickle
from datetime import datetime
from math import sqrt
from pprint import pformat

import face_recognition
from sklearn.neighbors import KNeighborsClassifier

from datastructure.Person import Person

log = logging.getLogger()


class Classifier(object):
	"""
	Store the knowledge related to the people faces
	"""

	def __init__(self):
		self.trainin_dir = None
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
		if self.classifier is None and self.model_path is None:
			log.error("load_classifier_from_file | Classifier path not set :/")
			raise Exception("load_classifier_from_file | Classifier path not set :/")

		if classifier_file is None:
			log.info("load_classifier_from_file | Skipping classifier loading ... | "
			         "Are you going to start a new training?")
			return

		# Load a trained KNN model (if one was passed in)
		err = None
		if self.classifier is None:
			log.debug("load_classifier_from_file | Loading classifier from file ...")
			if os.path.isdir(self.model_path):
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
			raise Exception(err)
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
			self.classifier.fit(X, Y)
			log.debug("train | Model Trained!")
			self.dump_model(self.model_path, "model")

	def dump_model(self, path, file):
		"""
		Dump the model to the given path, file
		:param path:
		:param file:
		"""
		log.debug("dump_model | Dumping model ... | Path: {} | File: {}".format(path, file))
		if os.path.isdir(path):
			time_parsed = datetime.now().strftime('%Y%m%d_%H%M%S')
			with open(os.path.join(path, "{}-{}.clf".format(file, time_parsed)), 'wb') as f:
				pickle.dump(self.classifier, f)

	def init_peoples_list(self):
		"""
		This method is delegated to iterate among the folder that contains the peoples's face in order to
		initalize the array of peoples
		:return:
		"""

		for people_name in os.listdir(self.trainin_dir):
			# Filter only folder
			if os.path.isdir(os.path.join(self.trainin_dir, people_name)):
				log.debug("{0}".format(os.path.join(self.trainin_dir, people_name)))
				person = Person()
				person.name = people_name
				person.path = os.path.join(self.trainin_dir, people_name)
				person.init_dataset()
				self.peoples_list.append(person)

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

	def predict(self, X_img_path, distance_threshold=0.6):
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
		X_img = face_recognition.load_image_file(X_img_path)
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
