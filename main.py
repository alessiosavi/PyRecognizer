"""
PyRecognizer loader
"""
import base64
import json
import os

import flask_monitoringdashboard as dashboard
from flask import Flask, flash, request, send_from_directory, url_for
from werkzeug.utils import redirect, secure_filename

from api.Api import upload_image_predict
from datastructure.Classifier import Classifier
from utils.util import load_logger, print_prediction_on_image

# ===== LOAD CONFIGURATION FILE =====
CONFIG_FILE = "conf/test.json"

with open(CONFIG_FILE) as f:
	CFG = json.load(f)

log = load_logger(CFG["logging"]["level"], CFG["logging"]["path"], CFG["logging"]["prefix"])

# ===== FLASK CONFIGURATION =====
# $(base64 /dev/urandom  | head -n 1 | md5sum | awk '{print $1}')
SECRET_KEY = str(base64.b64encode(bytes(os.urandom(24)))).encode()
UPLOAD_FOLDER = "/tmp/upload"

app = Flask(__name__, template_folder="api/templates")
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
def upload():
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
	prediction = clf.predict(img_path)
	print_prediction_on_image(img_path, prediction)
	return redirect(url_for('uploaded_file', filename="predict.png"))


# return redirect(url_for('uploaded_file', filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	"""

	:param filename:
	:return:
	"""
	return send_from_directory("/tmp/upload/prediction/", filename)


if __name__ == '__main__':
	app.run(host=CFG["network"]["host"], port=CFG["network"]["port"], threaded=True, debug=True)
