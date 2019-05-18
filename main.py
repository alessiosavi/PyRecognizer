# -*- coding: utf-8 -*-
"""
PyRecognizer loader
"""
import base64
import json
import os

import flask_monitoringdashboard as dashboard
from flask import Flask, flash, jsonify, render_template, request, send_from_directory
from werkzeug.utils import redirect, secure_filename

from api.Api import predict_image, train_network
from datastructure.Classifier import Classifier
from utils.util import load_logger

# ===== LOAD CONFIGURATION FILE =====
# TODO: Add argument parser for manage configuration file
CONFIG_FILE = "conf/test.json"

with open(CONFIG_FILE) as f:
	CFG = json.load(f)

log = load_logger(CFG["logging"]["level"], CFG["logging"]["path"], CFG["logging"]["prefix"])

# TODO: Verify the presence -> create directory
# NOTE: create a directory every time that you need to use this folder
TMP_UPLOAD_PREDICTION = CFG["PyRecognizer"]["temp_upload_predict"]
TMP_UPLOAD_TRAINING = CFG["PyRecognizer"]["temp_upload_training"]
TMP_UPLOAD = CFG["PyRecognizer"]["temp_upload"]

# $(base64 /dev/urandom  | head -n 1 | md5sum | awk '{print $1}')
SECRET_KEY = str(base64.b64encode(bytes(os.urandom(24)))).encode()

# ===== FLASK CONFIGURATION =====

app = Flask(__name__, template_folder=CFG["network"]["templates"])
app.secret_key = SECRET_KEY
# Used by flask when a upload is made
app.config['UPLOAD_FOLDER'] = TMP_UPLOAD

# =====FLASK DASHBOARD CONFIGURATION =====

dashboard.config.init_from(file=CFG["dashboard"]["config_file"])
dashboard.bind(app, SECRET_KEY)

# ===== CLASSIFIER CONFIGURATION =====

log.debug("Init classifier ...")
clf = Classifier()
clf.model_path = CFG["classifier"]["model_path"]
clf.load_classifier_from_file(CFG["classifier"]["model"])

allowed_ext = ["jpg", "jpeg", "png"]


@app.route('/', methods=['GET'])
def home():
	"""
	Show the html template for upload the image
	"""
	return render_template("upload.html")


@app.route('/', methods=["POST"])
def predict():
	"""
	Load the image using the HTML page and predict who is
	:return:
	"""
	# check if the post request has the file part
	if 'file' not in request.files or request.files['file'].filename == '':
		flash('No file choosed :/', category="error")
		return redirect(request.url)  # Return to HTML page [GET]
	file = request.files['file']
	# TODO: Add check on extension
	filename = secure_filename(file.filename)
	img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	file.save(img_path)
	return jsonify(response=predict_image(img_path, clf, TMP_UPLOAD_PREDICTION))


@app.route('/train', methods=['GET'])
def train():
	"""
	Show the html template for training the neural network
	"""
	return render_template("train.html")


@app.route('/train', methods=['POST'])
def train_http():
	"""

	:return:
	"""
	# check if the post request has the file part
	if 'file' not in request.files or request.files['file'].filename == '':
		flash('No file choosed :/', category="error")
		return redirect(request.url)  # Return to HTML page [GET]
	file = request.files['file']
	return jsonify(train_network(TMP_UPLOAD_TRAINING, file, clf))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	"""
	Expose images only to the one that know the image name
	:param filename:
	:return:
	"""
	return send_from_directory(TMP_UPLOAD_PREDICTION, filename)


if __name__ == '__main__':
	app.run(host=CFG["network"]["host"], port=CFG["network"]["port"], threaded=True, debug=True)
