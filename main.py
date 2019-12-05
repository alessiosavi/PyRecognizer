# -*- coding: utf-8 -*-
"""
PyRecognizer loader
"""
import base64
import os
import signal
import sys

import flask_monitoringdashboard as dashboard
from flask import Flask, flash, jsonify, render_template, request, send_from_directory, session
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename

from api.Api import predict_image, train_network, tune_network
from datastructure.Classifier import Classifier
from datastructure.Administrator import Administrator
from datastructure.Response import Response
from utils.util import init_main_data, random_string, secure_request, find_duplicates

# ===== LOAD CONFIGURATION FILE =====
# TODO: Add argument/environment var parser for manage configuration file
CONFIG_FILE = "conf/test.json"

CFG, log, TMP_UPLOAD_PREDICTION, TMP_UPLOAD_TRAINING, TMP_UPLOAD, TMP_UNKNOWN = init_main_data(
    CONFIG_FILE)

SSL_ENABLED = CFG["network"]["SSL"]["enabled"]
# Disable CSRF protection for if you need to use as REST server instead of use the GUI
ENABLE_CSRF = CFG["network"]["csrf_protection"]
# $(base64 /dev/urandom  | head -n 1 | md5sum | awk '{print $1}')
SECRET_KEY = str(base64.b64encode(bytes(os.urandom(24)))).encode()

login_manager = LoginManager()

# ===== FLASK CONFIGURATION =====
app = Flask(__name__, template_folder=CFG["network"]["templates"])
app.secret_key = SECRET_KEY
# Used by flask when a upload is made
app.config['UPLOAD_FOLDER'] = TMP_UPLOAD
PUB_KEY = CFG["network"]["SSL"]["cert.pub"]
PRIV_KEY = CFG["network"]["SSL"]["cert.priv"]

if not os.path.isfile(PUB_KEY) or not os.path.isfile(PRIV_KEY):
    log.error(
        "Unable to find certs file, be sure that the following certs exists, disabling SSL")
    log.warning("Public key: {}".format(PUB_KEY))
    log.warning("Private key: {}".format(PRIV_KEY))
    SSL_ENABLED = False

# =====FLASK DASHBOARD CONFIGURATION =====
dashboard.config.init_from(file=CFG["dashboard"]["config_file"])
dashboard.bind(app, SECRET_KEY)

# flask-login
login_manager.init_app(app)
login_manager.login_view = "login"

# ===== CLASSIFIER CONFIGURATION =====

log.debug("Init classifier ...")

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
        log.warning("predict_api | No file choosed!")
        return redirect(request.url)  # Return to HTML page [GET]
    file = request.files['file']
    treshold = request.form.get('treshold')
    log.debug("Recived file [{}] and treshold [{}]".format(file, treshold))
    if treshold is None or len(treshold) == 0:
        log.warning("Treshold not provided, using 45 as default")
        treshold = 45
    else:
        try:
            treshold = int(treshold)
        except ValueError:
            log.error("Unable to convert treshold")
            response = Response()
            response.error = "UNABLE_CAST_I  NT"
            response.description = "Treshold is not an integer!"
            response.status = "KO"
            return jsonify(response=response.__dict__)
    if not 0 <= treshold <= 100:
        log.error("Treshold wrong value")
        response = Response()
        response.error = "TRESHOLD_ERROR_VALUE"
        response.description = "Treshold have to be greater than 0 and lesser than 100!"
        response.status = "KO"
        return jsonify(response=response.__dict__)

    treshold /= 100

    log.debug("Recived file {} and treshold {}".format(file, treshold))
    filename = secure_filename(file.filename)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(img_path)
    return jsonify(response=predict_image(img_path, clf, TMP_UPLOAD_PREDICTION, TMP_UNKNOWN, treshold))


@app.route('/train', methods=['GET'])
@login_required
def train():
    """
    Show the html template for training the neural network
    """
    return render_template("train.html")


@app.route('/train', methods=['POST'])
@login_required
def train_http():
    """

    :return:
    """
    # check if the post request has the file part
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file choosed :/', category="error")
        return redirect(request.url)  # Return to HTML page [GET]
    file = request.files['file']
    file.save(os.path.join(TMP_UPLOAD_TRAINING, file.filename))
    return jsonify(train_network(TMP_UPLOAD_TRAINING, file, clf))


@app.route('/tune', methods=['GET'])
@login_required
def tune():
    """
    Show the html template for training the neural network
    """
    return render_template("train.html")


@app.route('/tune', methods=['POST'])
@login_required
def tune_http():
    """

    :return:
    """
    # check if the post request has the file part
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file choosed :/', category="error")
        return redirect(request.url)  # Return to HTML page [GET]
    file = request.files['file']
    file.save(os.path.join(TMP_UPLOAD_TRAINING, file.filename))
    return jsonify(tune_network(TMP_UPLOAD_TRAINING, file, clf))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Expose images only to the one that know the image name in a secure method
    :param filename:
    :return:
    """
    if os.path.exists(os.path.join(TMP_UPLOAD_PREDICTION, filename)):
        return send_from_directory(TMP_UPLOAD_PREDICTION, filename)
    return "PHOTOS_NOT_FOUND"


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    user = Administrator("administrator", email, "dummypassword")
    user.init_redis_connection()
    user_exists = user.verify_user_exist()
    user.redis_client.close()
    if not user_exists:
        return

    user = User()
    user.id = email
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    password = request.form['password']
    log.debug("Password in input -> {}".format(password))
    # name (administrator) is not managed
    admin = Administrator("administrator", email, password)
    if not admin.init_redis_connection():
        return "UNABLE_CONNECT_REDIS_DB"
    authenticated = admin.verify_login(password)
    admin.redis_client.close()
    if not authenticated:
        log.debug("Password is not valid!")
        return "PASSWORD_NOT_VALID"
    user = User()
    user.id = email
    login_user(user)
    log.debug("Logged in!")
    return redirect('/train')


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id


@app.before_request
def csrf_protect():
    """
    Validate csrf token against the one in session
    :return:
    """
    if ENABLE_CSRF:
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
    return secure_request(response, SSL_ENABLED)


def generate_csrf_token():
    """
    Generate a randome string and set the data into session
    :return:
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = random_string()
    return session['_csrf_token']


def signal_handler(signal, frame):
    find_duplicates(TMP_UPLOAD)
    find_duplicates(TMP_UPLOAD_PREDICTION)
    find_duplicates(TMP_UNKNOWN)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


app.jinja_env.globals['csrf_token'] = generate_csrf_token
app.jinja_env.autoescape = True


if __name__ == '__main__':
    if SSL_ENABLED:
        log.debug("main | RUNNING OVER SSL")
        app.run(host=CFG["network"]["host"], port=CFG["network"]["port"], threaded=False, debug=False, use_reloader=False, ssl_context=(
                PUB_KEY, PRIV_KEY))
    else:
        log.debug("main | HTTPS DISABLED | RUNNING OVER HTTP")
        app.run(host=CFG["network"]["host"], port=CFG["network"]
                ["port"], threaded=False, debug=False)
