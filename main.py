# -*- coding: utf-8 -*-
"""
PyRecognizer loader
"""
import base64
import os

import flask_monitoringdashboard as dashboard
from flask import Flask, flash, jsonify, render_template, request, send_from_directory, session
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename

from api.Api import predict_image, train_network, tune_network
from datastructure.Classifier import Classifier
from utils.util import init_main_data, random_string, secure_request

# ===== LOAD CONFIGURATION FILE =====
# TODO: Add argument/environment var parser for manage configuration file
CONFIG_FILE = "conf/test.json"

CFG, log, TMP_UPLOAD_PREDICTION, TMP_UPLOAD_TRAINING, TMP_UPLOAD = init_main_data(CONFIG_FILE)

SSL_ENABLED = CFG["network"]["SSL"]["enabled"]
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

PUB_KEY = CFG["network"]["SSL"]["cert.pub"]
PRIV_KEY = CFG["network"]["SSL"]["cert.priv"]

clf = Classifier()
clf.model_path = CFG["classifier"]["model_path"]
clf.load_classifier_from_file(CFG["classifier"]["timestamp"])


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


@app.route('/tune', methods=['GET'])
def tune():
	"""
	Show the html template for training the neural network
	"""
	return render_template("train.html")


@app.route('/tune', methods=['POST'])
def tune_http():
	"""

	:return:
	"""
	# check if the post request has the file part
	if 'file' not in request.files or request.files['file'].filename == '':
		flash('No file choosed :/', category="error")
		return redirect(request.url)  # Return to HTML page [GET]
	file = request.files['file']
	return jsonify(tune_network(TMP_UPLOAD_TRAINING, file, clf))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	"""
	Expose images only to the one that know the image name in a secure method
	:param filename:
	:return:
	"""
	return send_from_directory(TMP_UPLOAD_PREDICTION, filename)


@app.before_request
def csrf_protect():
	"""
	Validate csrf token against the one in session
	:return:
	"""
	if "dashboard" not in str(request.url_rule):
		if request.method == "POST":
			token = session.pop('_csrf_token', None)
			if not token or token != request.form.get('_csrf_token'):
				abort(403)


@app.after_request
def secure_headers(response):
	"""
	Apply securiy headers to the response call
	:return:
	"""
	return secure_request(response,SSL_ENABLED)


def generate_csrf_token():
	"""
	Generate a randome string and set the data into session
	:return:
	"""
	if '_csrf_token' not in session:
		session['_csrf_token'] = random_string()
	return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':
	app.jinja_env.autoescape = True
	if SSL_ENABLED:
		log.debug("main | RUNNING OVER SSL")
		app.run(host=CFG["network"]["host"], port=CFG["network"]["port"], threaded=False, debug=True,use_reloader=False, ssl_context=(
			PUB_KEY, PRIV_KEY))
	else:
		log.debug("main | HTTPS DISABLED | RUNNING OVER HTTP")
		app.run(host=CFG["network"]["host"], port=CFG["network"]["port"], threaded=False, debug=True)
