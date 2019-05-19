# -*- coding: utf-8 -*-
"""
Common method for reuse code
"""
import json
import logging
import os
import random
import shutil
import string
from logging.handlers import TimedRotatingFileHandler

from PIL import Image, ImageDraw

levels = {
	'debug': logging.DEBUG,
	'info': logging.INFO,
	'warning': logging.WARNING,
	'error': logging.ERROR,
	'critical': logging.CRITICAL
}


def print_prediction_on_image(img_path, predictions, path_to_save, file_to_save):
	"""
	Shows the face recognition results visually.

	:param path_to_save:
	:param file_to_save:
	:param img_path: path to image to be recognized
	:param predictions: results of the predict function
	:return:
	"""
	pil_image = Image.open(img_path).convert("RGB")
	draw = ImageDraw.Draw(pil_image)

	for name, (top, right, bottom, left) in predictions:
		# Draw a box around the face using the Pillow module
		draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

		# There's a bug in Pillow where it blows up with non-UTF-8 text
		# when using the default bitmap font
		name = name.encode("UTF-8")

		# Draw a label with a name below the face
		text_width, text_height = draw.textsize(name)
		draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
		draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
	# Remove the drawing library from memory as per the Pillow docs
	del draw

	# Display the resulting image
	# pil_image.show()
	pil_image.save(os.path.join(path_to_save, file_to_save), "PNG")


def init_main_data(config_file):
	"""
	Parse the configuration file and return the necessary data for initalize the tool
	:param config_file:
	:return:
	"""
	with open(config_file) as f:
		CFG = json.load(f)

	log = load_logger(CFG["logging"]["level"], CFG["logging"]["path"], CFG["logging"]["prefix"])

	# TODO: Verify the presence -> create directory
	# NOTE: create a directory every time that you need to use this folder
	TMP_UPLOAD_PREDICTION = CFG["PyRecognizer"]["temp_upload_predict"]
	TMP_UPLOAD_TRAINING = CFG["PyRecognizer"]["temp_upload_training"]
	TMP_UPLOAD = CFG["PyRecognizer"]["temp_upload"]

	if not os.path.exists(TMP_UPLOAD_PREDICTION):
		os.makedirs(TMP_UPLOAD_PREDICTION)
	if not os.path.exists(TMP_UPLOAD_TRAINING):
		os.makedirs(TMP_UPLOAD_TRAINING)
	if not os.path.exists(TMP_UPLOAD):
		os.makedirs(TMP_UPLOAD)

	return CFG, log, TMP_UPLOAD_PREDICTION, TMP_UPLOAD_TRAINING, TMP_UPLOAD


def load_logger(level, path, name):
	"""

	:param level:
	:param path:
	:param name:
	"""
	logger = logging.getLogger()  # set up root logger
	filename = '{0}{1}'.format(path, name)
	handler = TimedRotatingFileHandler(filename, when='H')
	handler.suffix = "%Y-%m-%d.log"
	handler.extMatch = r"^\d{4}-\d{2}-\d{2}\.log$"

	level = levels[level]
	handler.setLevel(level)  # set level for handler
	formatter = '%(asctime)s - %(name)s - %(levelname)s | [%(filename)s:%(lineno)d] | %(message)s'
	handler.setFormatter(logging.Formatter(formatter))
	logger.addHandler(handler)
	logger.setLevel(level)
	return logger


def random_string(string_length=10):
	"""
	Generate a random string of fixed length
	:param string_length:
	:return:
	"""
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(string_length))


def zip_data(file_to_zip, path):
	"""

	:param file_to_zip:
	:param path:
	:return:
	"""

	shutil.make_archive(file_to_zip, 'zip', path)


def remove_dir(dir):
	if os.path.isdir(dir):
		shutil.rmtree(dir)
