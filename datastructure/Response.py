# -*- coding: utf-8 -*-
"""
Define the standard response to return to the client
"""

from datetime import datetime


class Response(object):
	"""
	Response class is delegated to standardize the response in order to better manage the interaction with other
	external tools
	"""

	def __init__(self):
		self.status = "KO"
		self.description = None
		self.error = None
		self.data = None
		self.date = str(datetime.now())
