# PyRecognizer

A simple face recognition engine

## Introduction

This project is developed for have a plug-and-play facial recognition tool able to detect and recognize multiple faces from photos. It aim to be inter operable with other tool. For this purpose, it expose REST api in order to interact with the facial recognition engine (train/tune/predict).

It's written for be a basecode/project structure for future project where a more complicated facial detect + neural network have to be engaged.
Currently it use a KNN in order to predict the given faces.

## Requirements

- [olefile](https://github.com/decalage2/olefile) Parse, read and write Microsoft OLE2 files (deal with image)
- [werkzeug](https://github.com/pallets/werkzeug) The comprehensive WSGI web application library
- [face_recognition](https://github.com/ageitgey/face_recognition) Detect face point
- [tqdm](https://github.com/tqdm/tqdm) A Fast, Extensible Progress Bar
- [Flask_MonitoringDashboard](https://github.com/flask-dashboard/Flask-MonitoringDashboard) Automatically monitor the evolving performance of Flask/Python web services
- [Flask](https://github.com/pallets/flask) The Python micro framework for building web applications
- [Pillow](https://github.com/python-pillow/Pillow) The friendly PIL fork (Python Imaging Library)
- [scikit-learn](https://github.com/scikit-learn/scikit-learn) Machine learning in Python

## Table Of Contents

- [PyRecognizer](#pyrecognizer)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Table Of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
  - [In Details](#in-details)
  - [Example response](#example-response)
  - [Contributing](#contributing)
  - [Versioning](#versioning)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Prerequisites

The software is coded in `Python`, into the `requirements.txt` file are saved the necessary dependencies.

Create a virtual environment with you favorite `python` package manager

```bash
# Create a new environment
conda create -n PyRecognizer python=3.7.4
# Activate the environment
conda activate PyRecognizer
# Install the necessary dependencies
pip install -r requirements.txt
```

At this point you are ready to run the software.

## Usage

Before you can train the KNN with your photos, you need to create an archive that contains the image of the people's faces that you want to predict.

- Save a bunch of images of the people that you need to recognize.
- Copy the image in a folder. The name of that folder is important, cause it will be used as a label for the dataset (images) that contains during prediction.
- Compress the folders in a `zip` file.

If your dataset tree structure look likes the following tree dir, you can continue with training phase.

```text
├── bfegan
      └── ...
├── chris
      └── ...
├── dhawley
      └── ...
├── graeme
      └──...
├── heather
      └──...
```

In this case we have a dataset that contains the photos of 5 people (bfegan, dhawley, heather etc).  
Each directory, contains the photos related to the "target".

At this point the dataset is complete and you can continue with training/tuning.

Backup and remove the already present model (if present,inside the `dataset/model` directory), the tool will understand that you want to train the model and will initialize a new KNN model. The model have the following template: `%Y%m%d_%H%M%S`, related to the time that was generated.

Open your browser at the `endpoint:port/train` specified in the configuration file (`conf/test.json`).  
**NOTE:** you can switch on/off the SSL, be sure to add `https` before the endpoint ip/hostname if it is enabled.

At this point you can upload the dataset (the previous `zip` file) and wait for the training of the neural network.

You can tail the log in `log/pyrecognizer.log` in order to understand the status of the training.

Once completed, the browser page will be refreshed automatically and you can predict a new photos that the neural network haven't seen before.

**NOTE:** The same procedure can be applied for `tune` the neural network. By this way, you are going to execute an exhaustive search over specified parameter values for the KNN classifier. And, obviously, is more time consuming and the neural network produced will be more precise. The endpoint is `/tune` instead of `/train`

After `train/tune` phase, you have to modify the configuration file in order to use the new model. The model is saved in a new folder with the related timestamp (modify classifier -> timestamp in the configuration file)

## In Details

```bash
tree
.
├── api
│   ├── Api.py                           # Code that contains the API endpoint logic
│   └── templates                        # Folder that contains the HTML template for tune/train/predict
│       ├── train.html
│       └── upload.html
├── conf                                 # Configuration folder
│   ├── dashboard.ini                    # File related to the Dashboard configuration
│   ├── flask_monitoringdashboard.db     # Dashboard database
│   ├── ssl                              # SSL Certificates folder
│   │   ├── localhost.crt
│   │   └── localhost.key
│   └── test.json                        # Tool configuration file
├── dataset                              # Model folder + test dataset
│   ├── face_training_dataset_little.zip
│   ├── face_training_dataset.zip
│   └── model                            # Neural network model's folder
│       ├── 20191123_171821              # Neural network model
│       │   ├── model.clf
│       │   ├── model.dat
│       │   └── model.json
│       └── README.md
├── datastructure                        # Datastructure/Class used
│   ├── Classifier.py
│   ├── Person.py
│   └── Response.py
├── log                                  # Log folder
│   └── pyrecognizer.log
├── main.py                              # Main program to spawn the tool
├── README.md
├── requirements.txt                     # Dependencies file
├── uploads                              # Folder that contains the upload data
│   ├── predict
│   ├── training
│   └── upload
│       ├── photo_2019-11-18_15-47-35.jpg
│       └── vlcsnap-2019-11-18-16h07m28s988.png
└── utils                                # Common methods
    └── util.py
```

## Example response

- **Unable to detect a face**
  
```text
{
  "response": {
    "data": null,
    "date": "2019-11-23 18:10:11.038329",
    "description": "Seems that in this images there is no face :/",
    "error": "NO_FACE_FOUND",
    "status": "KO"
  }
}
```

- **Face not recognized**

```text
{
  "response": {
    "data": {},
    "date": "2019-11-23 18:17:58.287413",
    "description": "IMAGE_NOT_RECOGNIZED",
    "error": null,
    "status": "OK"
  }
}
```

- **Face recognized**

```text
{
  "response": {
    "data": {
      "iroy": 0.5762745881923004 # Name of the person: confidence
    },
    "date": "2019-11-23 18:23:01.762757",
    "description": "ijyibbvcgq.png", # Random string for view image prediction (visit /uploads/ijyibbvcgq.png)
    "error": null,
    "status": "OK"
  }
}
```

- **Missing model's classifier**

```text
{
  "response": {
    "data": null,
    "date": "2019-11-23 18:27:55.761851",
    "description": "CLASSIFIER_NOT_LOADED",
    "error": null,
    "status": "KO"
  }
}
```

## Contributing

- Feel free to open issue in order to __*require new functionality*__;  
- Feel free to open issue __*if you discover a bug*__;  
- New idea/request/concept are very appreciated!;  

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

- **Alessio Savi** - *Initial work & Concept* - [Linkedin](https://www.linkedin.com/in/alessio-savi-2136b2188/)  

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Face data are sensible information. In order to mitigate the risk of stealing sensible data, the tool can run in SSL mode for avoid packet sniffing and secure every request using a CSRF mitigation
