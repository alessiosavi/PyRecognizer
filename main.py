# -*- coding: utf-8 -*-
"""
PyRecognizer loader
"""
import base64
import json
import os

import flask_monitoringdashboard as dashboard
from flask import Flask, flash, jsonify, request, send_from_directory
from werkzeug.utils import redirect, secure_filename

from api.Api import predict_image, upload_image_predict
from datastructure.Classifier import Classifier
from utils.util import load_logger

# ===== LOAD CONFIGURATION FILE =====
# TODO: Add argument parser for manage configuration file
CONFIG_FILE = "conf/test.json"

PREDICTION_PATH = "/tmp/upload/predictions/"

with open(CONFIG_FILE) as f:
	CFG = json.load(f)

log = load_logger(CFG["logging"]["level"], CFG["logging"]["path"], CFG["logging"]["prefix"])

# $(base64 /dev/urandom  | head -n 1 | md5sum | awk '{print $1}')
SECRET_KEY = str(base64.b64encode(bytes(os.urandom(24)))).encode()
UPLOAD_FOLDER = "/tmp/upload"

# ===== FLASK CONFIGURATION =====

app = Flask(__name__, template_folder=CFG["network"]["templates"])
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =====FLASK DASHBOARD CONFIGURATION =====

dashboard.config.init_from(file=CFG["dashboard"]["config_file"])
dashboard.bind(app, SECRET_KEY)

# ===== CLASSIFIER CONFIGURATION =====

log.debug("Init classifier ...")
clf = Classifier()
# Loading mandatory data ...
clf.trainin_dir = CFG["classifier"]["trainin_dir"]
clf.model_path = CFG["classifier"]["model_path"]
clf.load_classifier_from_file(CFG["classifier"]["model"])

allowed_ext = ["jpg", "jpeg", "png"]


@app.route('/', methods=['GET'])
def home():
	"""
	Show the html template for upload the image
	"""
	return upload_image_predict("upload.html")


@app.route('/', methods=["POST"])
def predict():
	"""

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
	return jsonify(response=predict_image(img_path, clf, PREDICTION_PATH))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	"""

	:param filename:
	:return:
	"""
	return send_from_directory(PREDICTION_PATH, filename)


if __name__ == '__main__':
	app.run(host=CFG["network"]["host"], port=CFG["network"]["port"], threaded=True, debug=True)
