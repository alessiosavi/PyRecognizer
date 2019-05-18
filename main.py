from datetime import datetime
import json
import os
import pickle
from pprint import pformat

from Datastructure.Classifier import Classifier
from Datastructure.Person import Person
from utils.log import load_logger
from utils.util import  predict,show_prediction_labels_on_image

CONFIG_FILE = "conf/test.json"

CFG = None

with open(CONFIG_FILE) as f:
	CFG = json.load(f)

log = load_logger(CFG["logging"]["level"], CFG["logging"]["path"], CFG["logging"]["prefix"])

log.debug("Init classifier ...")
clf = Classifier()
clf.trainin_dir = CFG["classifier"]["trainin_dir"]
clf.model_path = CFG["classifier"]["model_path"]
peoples = []

log.debug("loading peoples ... {}".format(clf.trainin_dir))
# TODO: Be sure that no Person have same name
for people_name in os.listdir(clf.trainin_dir):
	# Filter only folder
	if os.path.isdir(os.path.join(clf.trainin_dir, people_name)):
		log.debug("{0}".format(os.path.join(clf.trainin_dir, people_name)))
		person = Person()
		person.name = people_name
		person.path = os.path.join(clf.trainin_dir, people_name)
		person.init_dataset()
		peoples.append(person)

DATASET = {
	# Image data (numpy array)
	"X": [],
	# Person name
	"Y": []
}

for people in peoples:
	log.debug(people.name)
	for item in people.dataset["X"]:
		DATASET["X"].append(item)
	for item in people.dataset["Y"]:
		DATASET["Y"].append(item)

log.debug(pformat(DATASET))

clf.init_specs(X_len=len(DATASET["X"]))
clf.classifier.fit(DATASET["X"],DATASET["Y"])
# Save the trained KNN classifier
if clf.model_path != "" and os.path.isdir(clf.model_path):
	time_parsed = datetime.now().strftime('%Y%m%d_%H%M%S')
	classifier_file = 'model.clf'
	with open(os.path.join(clf.model_path, classifier_file), 'wb') as f:
		pickle.dump(clf.classifier, f)


test_folder = "/home/alessiosavi/PycharmProjects/FaceDetect/test"

for image_file in os.listdir(test_folder):
	full_file_path = os.path.join(test_folder, image_file)

	log.info("Looking for faces in {}".format(image_file))

	# Find all people in the image using a trained classifier model
	# Note: You can pass in either a classifier file name or a classifier model instance
	predictions = predict(full_file_path, model_path=os.path.join(clf.model_path, classifier_file))

	# Print results on the console
	for name, (top, right, bottom, left) in predictions:
		log.info("- Found {} at ({}, {})".format(name, left, top))

	# Display results overlaid on an image
	show_prediction_labels_on_image(os.path.join(test_folder, image_file), predictions)
