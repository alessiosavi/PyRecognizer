# -*- coding: utf-8 -*-
"""
Common method for reuse code

Generate certificate

openssl req -x509 -out localhost.crt -keyout localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
"""
import filecmp
import json
import logging
import os
import pickle
import random
import shutil
import string
import zipfile
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, Union

import PIL
import numpy as np
from PIL import Image, ImageDraw

levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def print_prediction_on_image(img_path, predictions, file_to_save):
    """
    Shows the face recognition results visually.

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
        _, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10),
                        (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5),
                  name, fill=(255, 255, 255, 255))
    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    # pil_image.show()
    pil_image.save(file_to_save, "PNG")


def init_main_data(config_file):
    """
    Parse the configuration file and return the necessary data for initalize the tool
    :param config_file:
    :return:
    """
    try:
        with open(config_file) as f:
            CFG = json.load(f)
    except json.decoder.JSONDecodeError:
        raise Exception("Unable to load JSON File: {}".format(config_file))

    log = load_logger(CFG["logging"]["level"], CFG["logging"]["path"], CFG["logging"]["prefix"])

    # Store the image predicted drawing a boc in the face of the person
    TMP_UPLOAD_PREDICTION = CFG["PyRecognizer"]["temp_upload_predict"]
    # Uncompress the images in this folder
    TMP_UPLOAD_TRAINING = CFG["PyRecognizer"]["temp_upload_training"]
    # Save the images sent by the customer
    TMP_UPLOAD = CFG["PyRecognizer"]["temp_upload"]
    # Save the images of unknown people for future clustering/labeling
    TMP_UNKNOWN = CFG["PyRecognizer"]["temp_unknown"]
    # Use CNN if you have a GPU, use  HOG if you have CPU only
    detection_model = CFG["PyRecognizer"]["detection_model"].lower()
    # Use data augmentation when retrieving face encodings
    jitter = CFG["PyRecognizer"]["jitter"]
    # Use 68 or 5 points
    encoding_models = CFG["PyRecognizer"]["encoding_models"].lower()

    enable_dashboard = CFG["PyRecognizer"]["enable_dashboard"]

    if detection_model not in ('hog', 'cnn'):
        log.warning("detection_model selected is not valid! [{}], using 'hog' as default!".format(detection_model))
        detection_model = "hog"

    if jitter < 0:
        log.warning("jitter can be lower than 0, using 1 as default")
        jitter = 1

    if encoding_models not in ('small', 'large'):
        log.warning("encoding_models have to be or 'large' or 'small', using 'small' as fallback")
        encoding_models = "small"

    if not os.path.exists(TMP_UPLOAD_PREDICTION):
        os.makedirs(TMP_UPLOAD_PREDICTION)
    if not os.path.exists(TMP_UPLOAD_TRAINING):
        os.makedirs(TMP_UPLOAD_TRAINING)
    if not os.path.exists(TMP_UPLOAD):
        os.makedirs(TMP_UPLOAD)
    if not os.path.exists(TMP_UNKNOWN):
        os.makedirs(TMP_UNKNOWN)

    return CFG, log, TMP_UPLOAD_PREDICTION, TMP_UPLOAD_TRAINING, TMP_UPLOAD, TMP_UNKNOWN, detection_model, jitter, encoding_models, enable_dashboard


def load_logger(level, path, name):
    """

    :param level:
    :param path:
    :param name:
    """
    logger = logging.getLogger()  # set up root logger
    if not os.path.exists(path):
        logger.warning("Folder {} not found, creating a new one ...".format(path))
        os.makedirs(path)
    filename = os.path.join(path, name)
    handler = TimedRotatingFileHandler(filename, when='H')
    handler.suffix = "%Y-%m-%d.log"
    handler.extMatch = r"^\d{4}-\d{2}-\d{2}\.log$"

    level = levels[level]
    handler.setLevel(level)  # set level for handler
    formatter = '%(asctime)s - %(name)s - %(levelname)s | [%(filename)s:%(lineno)d] | %(message)s'
    handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.warning("Logger initialized, dumping log in {}".format(filename))
    return logger


def random_string(string_length=13):
    """
    Generate a random string of fixed length
    :param string_length:
    :return:
    """
    letters = string.ascii_lowercase
    data = ""
    for _ in range(string_length):
        data += random.choice(letters)
    return data


def zip_data(file_to_zip, path):
    """

    :param file_to_zip:
    :param path:
    :return:
    """

    shutil.make_archive(file_to_zip, 'zip', path)


def unzip_data(unzipped_folder, zip_file):
    """
    Unzip the zip file in input in the given 'unzipped_folder'
    :param unzipped_folder:
    :param zip_file:
    :return: The name of the folder in which find the unzipped data
    """
    log = logging.getLogger()
    folder_name = os.path.join(unzipped_folder, random_string())
    log.debug("unzip_data | Unzipping {} into {}".format(zip_file, folder_name))
    zip_ref = zipfile.ZipFile(zip_file)
    zip_ref.extractall(folder_name)
    zip_ref.close()
    log.debug("unzip_data | File uncompressed!")
    return folder_name


def dump_dataset(X, Y, path):
    """

    :param X:
    :param Y:
    :param path:
    :return:
    """
    log = logging.getLogger()
    dataset = {
        'X': X,
        'Y': Y
    }
    log.debug("dump_dataset | Dumping dataset int {}".format(path))
    if not os.path.exists(path):
        os.makedirs(path)
        log.debug("dump_dataset | Path {} exist".format(path))
        dataset_name = os.path.join(path, "model.dat")
        with open(dataset_name, 'wb') as f:
            pickle.dump(dataset, f)
    else:
        log.error(
            "dump_dataset | Path {} ALREADY EXIST exist, avoiding to overwrite".format(path))


def remove_dir(directory: str):
    """
    Wrapper for remove a directory
    :param directory:
    :return:
    """
    log = logging.getLogger()
    log.debug("remove_dir | Removing directory {}".format(directory))
    if not os.path.exists(directory):
        log.warning("remove_dir | Folder {} does not exists!".format(directory))
        return
    if not os.path.isdir(directory):
        log.warning("remove_dir | File {} is not a folder".format(directory))
        return
    shutil.rmtree(directory)


def verify_extension(folder, file):
    """
    Wrapper for validate file
    :param folder:
    :param file:
    :return:
    """
    log = logging.getLogger()
    extension = os.path.splitext(file)[1]
    log.debug("verify_extension | File: {} | Ext: {}".format(file, extension))
    filepath = os.path.join(folder, file)
    file_ext = None
    if os.path.exists(filepath):
        if extension == ".zip":
            log.debug("verify_extension | Verifying zip bomb ...")
            zp = zipfile.ZipFile(filepath)
            size = sum(zinfo.file_size for zinfo in zp.filelist)
            zip_kb = float(size) / (1000 * 1000)  # MB
            if zip_kb > 250:
                log.error("verify_extension | ZIP BOMB DETECTED! | Zip file size is to much {} MB ...".format(size))
                return "ZIP_BOMB!"
            file_ext = "zip"

        elif extension == ".dat":
            # Photos have been already analyzed, dataset is ready!
            file_ext = "dat"

    log.error("verify_extension | Filename {} does not exist!".format(filepath))
    return file_ext


def retrieve_dataset(folder_uncompress, zip_file, clf, detection_model, jitter, encoding_models):
    """

    :param folder_uncompress:
    :param zip_file:
    :param clf:
    :return:
    """
    log = logging.getLogger()
    log.debug("retrieve_dataset | Parsing dataset ...")
    check = verify_extension(folder_uncompress, zip_file.filename)
    if check == "zip":  # Image provided
        log.debug("retrieve_dataset | Zip file uploaded")
        folder_name = unzip_data(folder_uncompress, zip_file)
        log.debug("retrieve_dataset | zip file uncompressed!")
        clf.init_peoples_list(detection_model, jitter, encoding_models, peoples_path=folder_name)
        dataset = clf.init_dataset()
        log.debug("retrieve_dataset | Removing [{}]".format(folder_name))
        remove_dir(folder_name)
    elif check == "dat":
        log.debug("retrieve_dataset | Pickle data uploaded")
        dataset = pickle.load(zip_file)
    else:
        log.warning("retrieve_dataset | Unable to understand the file type: {}".format(check))
        dataset = None
    log.debug("retrieve_dataset | Dataset parsed!")
    return dataset


def secure_request(request, ssl: bool):
    """

    :param ssl:
    :param request:
    :return:
    """
    # request.headers['Content-Security-Policy'] = "script-src 'self' cdnjs.cloudflare.com ; "
    request.headers['Feature-Policy'] = "geolocation 'none'; microphone 'none'; camera 'self'"
    request.headers['Referrer-Policy'] = 'no-referrer'
    request.headers['x-frame-options'] = 'SAMEORIGIN'
    request.headers['X-Content-Type-Options'] = 'nosniff'
    request.headers['X-Permitted-Cross-Domain-Policies'] = 'none'
    request.headers['X-XSS-Protection'] = '1; mode=block'
    if ssl:
        request.headers['expect-ct'] = 'max-age=60, enforce'
        request.headers["Content-Security-Policy"] = "upgrade-insecure-requests"
        request.headers['Strict-Transport-Security'] = "max-age=60; includeSubDomains; preload"

    return request


def concatenate_dataset(*dictionary) -> Union[Dict, None]:
    """
    Concatenate multiple dataset into a single one
    """
    dataset = {}
    for d in dictionary:
        if type(d) is dict:
            dataset.update(d)

    if len(dataset) == 2:
        if "X" in dataset and "Y" in dataset:
            if len(dataset["X"]) != len(dataset["Y"]):
                return None
    return dataset


def load_image_file(file, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array

    :param file: image file name or file object to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """

    im = PIL.Image.open(file)
    width, height = im.size
    w, h = width, height
    log = logging.getLogger()

    ratio = -1
    # Ratio for resize the image
    log.debug("load_image_file | Image dimension: ({}:{})".format(w, h))
    # Resize in case of to bigger dimension
    # In first instance manage the HIGH-Dimension photos
    if width > 3600 or height > 3600:
        if width > height:
            ratio = width / 800
        else:
            ratio = height / 800

    elif 1200 <= width <= 1600 or 1200 <= height <= 1600:
        ratio = 1 / 2
    elif 1600 <= width <= 3600 or 1600 <= height <= 3600:
        ratio = 1 / 3

    log.debug("load_image_file | Dimension: w: {} | h: {}".format(w, h))
    log.debug("load_image_file | New ratio -> {}".format(ratio))

    if 0 < ratio < 1:
        # Scale image in case of width > 1600
        w = width * ratio
        h = height * ratio
    elif ratio > 1:
        # Scale image in case of width > 3600
        w = width / ratio
        h = height / ratio
    if w != width:
        # Check if scaling was applied
        maxsize = (w, h)
        log.debug("load_image_file | Image have to high dimension, avoiding memory error. Resizing to {}"
                  .format(maxsize))
        im.thumbnail(maxsize, PIL.Image.ANTIALIAS)

    if mode:
        im = im.convert(mode)
    return np.array(im), ratio


def find_duplicates(directory: str):
    log = logging.getLogger()
    # List files in the directory
    files = []
    for _file in os.listdir(directory):
        files.append(_file)

    equals = []
    # Searching duplicates files
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            if filecmp.cmp(os.path.join(directory, files[i]), os.path.join(directory, files[j])):
                equals.append(os.path.join(directory, files[i]))
                break
    log.info("find_duplicates | Removing the following duplicates files: {}".format(equals))
    for _file in equals:
        log.debug("find_duplicates | Removing file: {}".format(_file))
        os.remove(_file)
