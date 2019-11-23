# -*- coding: utf-8 -*-
"""
Common structure for define how to manage a person
"""
from logging import getLogger
from os.path import isdir

from face_recognition import face_encodings, face_locations, load_image_file
from face_recognition.face_recognition_cli import image_files_in_folder

log = getLogger()


class Person(object):
	"""
	Rappresent the necessary information for classify a person's face
	"""

	def __init__(self):
		# Name of the user
		self.name = ""
		# Filesystem folder where images are stored
		self.path = ""
		# Image list used for train the model
		self.dataset = {
			# Image data (numpy array)
			"X": [],
			# Person name
			"Y": []
		}

	def init_dataset(self):
		"""
		This method is delegated to load the images related to a person and verify if the ones
		are suitable for training the neural network.

		The image will be discarded if: More than one face if found | No face is found
		:return:
		"""

		if self.path != "" and isdir(self.path):
			log.debug("initDataset | Paramater provided, iterating images ..")
			# Iterating the images in parallel
			# pool = ThreadPool(2)
			# self.dataset["X"] = pool.map(self.init_dataset_core, image_files_in_folder(self.path))
			for image_path in image_files_in_folder(self.path):
				self.dataset["X"].append(self.init_dataset_core(image_path))
			self.dataset["X"] = list(filter(None.__ne__, self.dataset["X"]))  # Remove None
			# Loading the Y [target]
			for i in range(len(self.dataset["X"])):
				self.dataset["Y"].append(self.name)
			log.debug("Adding {} entries for {}".format(len(self.dataset["X"]), self.name))
		return

	@staticmethod
	def init_dataset_core(img_path=None):
		"""
		Delegated core method for parallelize work
		:param img_path:
		:return:
		"""
		try:
			image = load_image_file(img_path)
		except OSError:
			log.error("init_dataset | === FATAL === | Image {} is corrupted!!".format(img_path))
			return None
		# log.debug("initDataset | Image loaded! | Searching for face ...")
		# Array of w,x,y,z coordinates
		face_bounding_boxes = face_locations(image, model="cnn")
		face_data = None
		if len(face_bounding_boxes) == 1:
			log.info("initDataset | Image {0} have only 1 face, loading for future training ...".format(img_path))
			# Loading the X [data] using 300 times distortion
			face_data = face_encodings(image, known_face_locations=face_bounding_boxes, num_jitters=300)[0]
		else:
			log.error("initDataset | Image {0} not suitable for training!".format(img_path))
			if len(face_bounding_boxes) == 0:
				log.error("initDataset | I've not found any face :/ ")
			else:
				log.error("initDataset | Found more than one face, too much for me Sir :&")
		return face_data
