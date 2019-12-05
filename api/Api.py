# -*- coding: utf-8 -*-
"""
Custom function that will be wrapped for be HTTP compliant
"""

import time
from datetime import datetime
from logging import getLogger
import os
import shutil
import datetime

from datastructure.Response import Response
from datastructure.Administrator import Administrator
from utils.util import print_prediction_on_image, random_string, retrieve_dataset

log = getLogger()


def predict_image(img_path, clf, PREDICTION_PATH, TMP_UNKNOWN, treshold=45):
    """

    :param PREDICTION_PATH: global variable where image recognized are saved
    :param img_path: image that have to be predicted
    :param clf: classifier in charge to predict the image
    :return: Response dictionary jsonizable
    """
    response = Response()
    if clf is None:
        log.error("predict_image | FATAL | Classifier is None!")
        prediction = None
    else:
        log.debug("predict_image | Predicting {}".format(img_path))
        prediction = clf.predict(img_path, treshold)
        log.debug("predict_image | Result: {}".format(prediction))

    # Manage error
    if prediction is None:
        response.error = "CLASSIFIER_NOT_LOADED"
        response.description = "Classifier is None | Training mandatory"
        response.status = "KO"
        log.error("predict_image | Seems that the classifier is not loaded :/")
    # return Response(status="KO", description="CLASSIFIER_NOT_LOADED", data=prediction).__dict__

    elif isinstance(prediction, int):
        response.status = "KO"
        if prediction == -1:
            response.error = "FACE_NOT_RECOGNIZED"
            response.description = "Seems that this face is related to nobody that i've seen before ..."
            response.status = "KO"
            log.error("predict_image | Face not recognized ...")
            
            # Saving unkown faces for future clustering
            now = str(datetime.datetime.now())[:23]
            now = now.replace(":","_")
            now = now.replace(".","_")
            head,tail = os.path.split(img_path)
            filename, file_extension = os.path.splitext(tail)
            filename = filename + "__"+now+file_extension
            filename = os.path.join(TMP_UNKNOWN,filename)
            log.info("Image not recognized, saving it in: {}".format(filename))
            shutil.copy(img_path,filename)


        elif prediction == -2:
            response.error = "FILE_NOT_VALID"
            response.description = "Seems that the file that you have tried to upload is not valid ..."
            log.error(
                "predict_image |Seems that the file that you have tried to upload is not valid ...")

        # Manage no face found
        elif prediction == -3:
            log.error(
                "predict_image | Seems that this face is related to nobody that i've seen before ...")
            response.error = "FACE_NOT_FOUND"
            response.description = "No face found in the given image ..."
    # Manage success
    elif "predictions" in prediction and isinstance(prediction['predictions'], list):
        # Be sure to don't overwrite an existing image
        exists = True
        while exists:
            # img_name = os.path.join(PREDICTION_PATH, random_string() + ".png"
            img_name = random_string() + ".png"
            img_file_name = os.path.join(PREDICTION_PATH, img_name)
            if not os.path.exists(img_file_name):
                exists = False

        log.debug("predict_image | Generated a random name: {}".format(img_name))
        log.debug("predict_image | Printing prediction on image ...")
        print_prediction_on_image(
            img_path, prediction["predictions"], img_file_name)

        # response.error = "FACE_FOUND"
        # response.description = "/uploads/"+img_name
        # response.status = "OK"
        # response.data = prediction["predictions"]
        return Response(status="OK", description="/uploads/" + img_name, data=prediction).__dict__

    return response.__dict__


def train_network(folder_uncompress, zip_file, clf):
    """
    Train a new neural model with the zip file provided
    :param folder_uncompress:
    :param zip_file:
    :param clf:
    :return:
    """

    log.debug("train_network | Starting training phase ...")
    dataset = retrieve_dataset(folder_uncompress, zip_file, clf)
    if dataset is None:
        return Response(error="ERROR DURING LOADING DAT", description="Seems that the dataset is not valid").__dict__

    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        neural_model_file, _ = clf.train(dataset["X"], dataset["Y"], timestamp)

        response = Response(status="OK", data=neural_model_file)
        response.description = "Model succesfully trained!"
        log.debug("train_network | Tuning phase finihsed! | {}".format(
            response.description))

        return response.__dict__


def tune_network(folder_uncompress, zip_file, clf):
    """
    Train a new neural model with the zip file provided
    :param folder_uncompress:
    :param zip_file:
    :param clf:
    :return:
    """
    log.debug("tune_network | Starting tuning phase ...")
    dataset = retrieve_dataset(folder_uncompress, zip_file, clf)

    if dataset is None:
        return Response(error="ERROR DURING LOADING DAT", description="Seems that the dataset is not valid").__dict__

    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        neural_model_file, elapsed_time = clf.tuning(
            dataset["X"], dataset["Y"], timestamp)

        response = Response(status="OK", data=neural_model_file)
        response.description = "Model succesfully trained! | {}".format(
            time.strftime("%H:%M:%S.%f", time.gmtime(elapsed_time)))
        log.debug("train_network | Tuning phase finihsed! | {}".format(
            response.description))

        return response.__dict__
