# -*- coding: utf-8 -*-
"""
Basic test case for classifier
"""
import json
import sys
import unittest
from typing import Dict

import requests

sys.path.insert(0, "../")
from datastructure.Classifier import Classifier
from utils.util import init_main_data

config_file: str = "conf_test.json"
CFG, log, TMP_UPLOAD_PREDICTION, TMP_UPLOAD_TRAINING, TMP_UPLOAD, TMP_UNKNOWN, detection_model, jitter, encoding_models, _ = init_main_data(
    config_file)

url = "http://0.0.0.0:8081/"


class TestPredict(unittest.TestCase):
    def load_classifier(self, config: Dict) -> Classifier:
        clf = Classifier()
        clf.model_path = config["classifier"]["model_path"]
        clf.load_classifier_from_file(config["classifier"]["timestamp"])
        return clf

    clf = load_classifier(CFG)

    def test_predict_without_file(self):
        values = {"threshold": "45"}
        r = requests.post(url, data=values)
        log.debug(r.content)
        response = json.loads(r.content)["response"]["error"]
        self.assertEqual("NO_FILE_IN_REQUEST", response)
        return

    def test_predict_without_threshold(self):
        image = open('test_images/bush_test.jpg', 'rb')
        files = {"file": image}
        r = requests.post(url, files=files)
        image.close()
        log.debug(r.content)
        response = json.loads(r.content)["response"]["error"]
        self.assertEqual("THRESHOLD_NOT_PROVIDED", response)
        return

    def test_predict_without_threshold_not_number(self):
        image = open('test_images/bush_test.jpg', 'rb')
        files = {"file": image}
        data = {"threshold": "a"}
        r = requests.post(url, files=files, data=data)
        image.close()
        log.debug(r.content)
        response = json.loads(r.content)["response"]["error"]
        self.assertEqual("UNABLE_CAST_INT", response)
        return

    def test_predict_without_threshold_invalid_number(self):
        image = open('test_images/bush_test.jpg', 'rb')
        files = {"file": image}
        data = {"threshold": "-1"}
        r = requests.post(url, files=files, data=data)
        image.close()
        log.debug(r.content)
        response = json.loads(r.content)["response"]["error"]
        self.assertEqual("THRESHOLD_ERROR_VALUE", response)
        return

    def test_predict_with_no_face(self):
        image = open('test_images/no_face_test.png', 'rb')
        files = {"file": image}
        data = {"threshold": "1"}
        r = requests.post(url, files=files, data=data)
        image.close()
        log.debug(r.content)
        response = json.loads(r.content)["response"]
        self.assertEqual("FACE_NOT_FOUND", response["error"])
        return

    def test_predict_one_face(self):
        image = open('test_images/bush_test.jpg', 'rb')
        files = {"file": image}
        data = {"threshold": "1"}
        r = requests.post(url, files=files, data=data)
        image.close()
        log.debug(r.content)
        response = json.loads(r.content)["response"]
        self.assertIsNone(response["error"])
        data = response["data"]
        self.assertEqual(list(data.keys())[0], "George_W_Bush")
        self.assertGreater(list(data.values())[0], 0.99)
        return

    def test_predict_multiple_face(self):
        image = open('test_images/multi_face_test.jpg', 'rb')
        files = {"file": image}
        data = {"threshold": "1"}
        r = requests.post(url, files=files, data=data)
        image.close()
        log.debug(r.content)
        response = json.loads(r.content)["response"]
        self.assertIsNone(response["error"])
        data = response["data"]
        self.assertEqual(list(data.keys())[0], "Angelina_Jolie")
        self.assertEqual(list(data.keys())[1], "Clint_Eastwood")
        self.assertGreater(list(data.values())[0], 0.85)
        self.assertGreater(list(data.values())[1], 0.93)
        return

    def test_predict_unknown_face(self):
        image = open('test_images/unknown_face.jpg', 'rb')
        files = {"file": image}
        data = {"threshold": "90"}
        r = requests.post(url, files=files, data=data)
        image.close()
        log.debug(r.content)
        response = json.loads(r.content)["response"]
        self.assertEqual("FACE_NOT_RECOGNIZED", response["error"])
        return


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
