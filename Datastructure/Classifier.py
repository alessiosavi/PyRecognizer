"""
Core utils for manage face recognition process
"""

import logging
from math import sqrt
from pprint import pformat

from sklearn.neighbors import KNeighborsClassifier

log = logging.getLogger()


class Classifier(object):
	"""
	Store the knowledge related to the people faces
	"""

	def __init__(self):
		self.trainin_dir = ""
		self.model_path = ""
		self.n_neighbors = ""
		self.knn_algo = ""
		self.classifier = None

	def init_specs(self, knn_algo=None, X_len=None):
		log.debug("init_specs | Init knn algorithm ...")
		if self.knn_algo == "" and knn_algo is None:
			self.knn_algo = 'ball_tree'
		self.init_n_neighbors(X_len)
		self.init_classifier()

	def init_n_neighbors(self, X_len=None):
		if X_len is None:
			X_len = 20
		log.debug("init_n_neighbors | START")
		if self.n_neighbors == "":
			self.n_neighbors = int(round(sqrt(X_len)))
		log.debug("init_n_neighbors | Choosed {0} n_neighbors".format(self.n_neighbors))

	def init_classifier(self):
		if self.classifier is None:
			if self.knn_algo != "" and self.n_neighbors != "":
				log.debug("init_classifier | Initializing a new classifier ... | {0}".format(pformat(self.__dict__)))
				self.classifier = KNeighborsClassifier(
					n_neighbors=self.n_neighbors, algorithm=self.knn_algo, weights='distance')
