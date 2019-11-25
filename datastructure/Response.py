# -*- coding: utf-8 -*-
"""
Define the standard response to return to the client
"""

import logging
from datetime import datetime


class Response(object):
	"""
	Response class is delegated to standardize the response in order to better manage the interaction with other
	external tools
	"""

	def __init__(self, status="KO", description=None, error=None, data=None):
		self.status = status
		self.description = description
		self.error = error
		self.data = self.parse_data(data)
		self.date = str(datetime.now())

	def parse_data(self, data):
		"""

		:param data:
		:return:
		"""
		log = logging.getLogger()
		log.debug("parse_data | Parsing {}".format(data))

		t = {}
		if data is not None:
			log.debug("parse_data | Data not None ...")
			if isinstance(data, dict):
				log.debug("parse_data | Data is a dict")
				if "predictions" in data and "scores" in data:
					# if predictions data["predictions"] and data["scores"]:
					log.debug("parse_data | Predictions and scores provided")
					if isinstance(data["predictions"], list) and isinstance(data["scores"], list):
						predictions = data["predictions"]
						scores = data["scores"]
						if len(predictions) == len(scores):
							log.debug("parse_data | Predictions and scores same lenght")
						for i in range(len(predictions)):
							t[predictions[i][0]] = scores[i]
						log.debug("parse_data | Dict initalized -> {}".format(t))
						return t

		self.date = data
