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

	def __init__(self, status="KO", description=None, error=None, data=None):
		self.status = status
		self.description = description
		self.error = error
		self.data = data
		self.date = str(datetime.now())
