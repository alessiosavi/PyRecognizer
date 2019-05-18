"""
Custom function that will be wrapped for be HTTP compliant
"""

from flask import render_template


def upload_image_predict(html_file):
	"""
	Parse the HTML file
	:param html_file:
	:return:
	"""
	return render_template(html_file)
