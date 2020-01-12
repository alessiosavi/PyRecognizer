# PyRecognizer

A simple face recognition engine

[![License](https://img.shields.io/github/license/alessiosavi/PyRecognizer)](https://img.shields.io/github/license/alessiosavi/PyRecognizer) [![Version](https://img.shields.io/github/v/tag/alessiosavi/PyRecognizer)](https://img.shields.io/github/v/tag/alessiosavi/PyRecognizer) [![Code size](https://img.shields.io/github/languages/code-size/alessiosavi/PyRecognizer)](https://img.shields.io/github/languages/code-size/alessiosavi/PyRecognizer) [![Repo size](https://img.shields.io/github/repo-size/alessiosavi/PyRecognizer)](https://img.shields.io/github/repo-size/alessiosavi/PyRecognizer) [![Issue open](https://img.shields.io/github/issues/alessiosavi/PyRecognizer)](https://img.shields.io/github/issues/alessiosavi/PyRecognizer)
[![Issue closed](https://img.shields.io/github/issues-closed/alessiosavi/PyRecognizer)](https://img.shields.io/github/issues-closed/alessiosavi/PyRecognizer)

## Video guide for train/predict

<https://youtu.be/Tctui-KzPaM>

## Model tuned for some celebrities

The following list contains the name of the celebrity and the number of photos used for training, ordered by the number of photos

<details><summary> Celebrites list</summary><br><pre>
George_W_Bush  530
Colin_Powell  236
Tony_Blair  144
Donald_Rumsfeld  121
Gerhard_Schroeder  109
Ariel_Sharon  77
Hugo_Chavez   71
Junichiro_Koizumi  60
Jean_Chretien  55
John_Ashcroft  53
Serena_Williams 	52
Jacques_Chirac  52
Vladimir_Putin  49
Luiz_Inacio_Lula_da_Silva 	48
Gloria_Macapagal_Arroyo  44
Jennifer_Capriati 	42
Arnold_Schwarzenegger  42
Lleyton_Hewitt 	41
Laura_Bush 	41
Hans_Blix  39
Alejandro_Toledo 	39
Nestor_Kirchner  37
Andre_Agassi  36
Alvaro_Uribe  35
Tom_Ridge  33
Silvio_Berlusconi  33
Megawati_Sukarnoputri  33
Vicente_Fox  32
Roh_Moo-hyun  32
Kofi_Annan  32
John_Negroponte  31
David_Beckham  31
Recep_Tayyip_Erdogan  30
Guillermo_Coria  30
Mahmoud_Abbas 	29
Bill_Clinton  29
Juan_Carlos_Ferrero  28
Jack_Straw 	28
Ricardo_Lagos  27
Rudolph_Giuliani  26
Gray_Davis  26
Tom_Daschle 	25
Winona_Ryder 	24
Jeremy_Greenstock  24
Atal_Bihari_Vajpayee  24
Tiger_Woods 	23
Saddam_Hussein  23
Jose_Maria_Aznar 	23
Pete_Sampras  22
Naomi_Watts 	22
Lindsay_Davenport  22
Hamid_Karzai 	22
George_Robertson  22
Jennifer_Lopez 	21
Jennifer_Aniston 	21
Carlos_Menem 	21
Amelie_Mauresmo 	21
Paul_Bremer 	20
Michael_Bloomberg 	20
Jiang_Zemin 	20
Igor_Ivanov 	20
Angelina_Jolie 	20
Tim_Henman 	19
Nicole_Kidman 	19
Julianne_Moore 	19
Joschka_Fischer 	19
John_Howard 	19
Carlos_Moya 	19
Abdullah_Gul 	19
Richard_Myers 	18
Pervez_Musharraf 	18
Michael_Schumacher 	18
Lance_Armstrong 	18
Fidel_Castro 	18
Venus_Williams 	17
Spencer_Abraham 	17
Renee_Zellweger 	17
John_Snow 	17
John_Kerry 	17
John_Bolton  17
Jean_Charest  17
Bill_Gates  17
Trent_Lott 	16
Tommy_Franks  16
Halle_Berry 	16
Taha_Yassin_Ramadan  15
Pierce_Brosnan 	15
Norah_Jones  15
Nancy_Pelosi 	15
Mohammed_Al-Douri 	15
Meryl_Streep 	15
Julie_Gerberding 	15
Hu_Jintao 	15
Dominique_de_Villepin 	15
Bill_Simon 	15
Andy_Roddick 	15
Yoriko_Kawaguchi 	14
Roger_Federer 	14
Mahathir_Mohamad 	14
Kim_Clijsters 	14
James_Blake 	14
Hillary_Clinton 	14
Eduardo_Duhalde 	14
Dick_Cheney 	14
David_Nalbandian 	14
Britney_Spears 	14
Wen_Jiabao 	13
Salma_Hayek 	13
Queen_Elizabeth_II 	13
Lucio_Gutierrez 	13
Joe_Lieberman 	13
Jackie_Chan 	13
Gordon_Brown 	13
George_HW_Bush 	13
Edmund_Stoiber 	13
Charles_Moose 	13
Ari_Fleischer 	13
Rubens_Barrichello 	12
Michael_Jackson 	12
Keanu_Reeves 	12
Jennifer_Garner 	12
Jeb_Bush 	12
Howard_Dean 	12
Harrison_Ford 	12
Gonzalo_Sanchez_de_Lozada 	12
Anna_Kournikova 	12
Adrien_Brody 	12
Tang_Jiaxuan 	11
Sergio_Vieira_De_Mello 	11
Sergey_Lavrov 	11
Richard_Gephardt 	11
Paul_Burrell 	11
Nicanor_Duarte_Frutos 	11
Mike_Weir 	11
Mark_Philippoussis 	11
Kim_Ryong-sung 	11
John_Paul_II 	11
John_Allen_Muhammad 	11
Jiri_Novak 	11
James_Kelly 	11
Condoleezza_Rice 	11
Catherine_Zeta-Jones 	11
Ann_Veneman 	11
Walter_Mondale 	10
Tommy_Thompson 	10
Tom_Hanks 	10
Tom_Cruise 	10
Richard_Gere 	10
Paul_Wolfowitz 	10
Paradorn_Srichaphan 	10
Muhammad_Ali 	10
Mohammad_Khatami 	10
Jean-David_Levitte 	10
Javier_Solana 	10
Jason_Kidd 	10
Jacques_Rogge 	10
Ian_Thorpe 	10
Bill_McBride 	10
Zhu_Rongji 	9
Vaclav_Havel 	9
Tung_Chee-hwa 	9
Thomas_OBrien 	9
Sylvester_Stallone 	9
Richard_Armitage 	9
Ray_Romano 	9
Paul_ONeill 	9
Li_Peng 	9
Leonardo_DiCaprio 	9
Kate_Hudson 	9
Jose_Serra 	9
John_Abizaid 	9
Joan_Laporta 	9
Jimmy_Carter 	9
Jesse_Jackson 	9
Jeong_Se-hyun 	9
Hugh_Grant 	9
Hosni_Mubarak 	9
Heizo_Takenaka 	9
George_Clooney 	9
Fernando_Gonzalez 	9
Colin_Farrell 	9
Charles_Taylor 	9
Bill_Graham 	9
Bill_Frist 	9
Yasser_Arafat 	8
Yao_Ming 	8
Shimon_Peres 	8
Sheryl_Crow 	8
Ron_Dittemore 	8
Robert_Redford 	8
Robert_Duvall 	8
Robert_Blake 	8
Richard_Virenque 	8
Ralf_Schumacher 	8
Paul_Martin 	8
Naji_Sabri 	8
Mohamed_ElBaradei 	8
Michelle_Kwan 	8
Michael_Chang 	8
Maria_Shriver 	8
Li_Zhaoxing 	8
Kim_Dae-jung 	8
Kevin_Costner 	8
Justin_Timberlake 	8
Juan_Pablo_Montoya 	8
Jonathan_Edwards 	8
John_Edwards 	8
Jelena_Dokic 	8
Gerry_Adams 	8
Fernando_Henrique_Cardoso 	8
Cesar_Gaviria 	8
Celine_Dion 	8
Bob_Hope 	8
Antonio_Palocci 	8
Ana_Palacio 	8
Ali_Naimi 	8
Al_Gore 	8
Yashwant_Sinha 	7
William_Ford_Jr 	7
William_Donaldson 	7
Vojislav_Kostunica 	7
Vincent_Brooks 	7
Steven_Spielberg 	7
Sophia_Loren 	7
Romano_Prodi 	7
Robert_Zoellick 	7
Pedro_Almodovar 	7
Paul_McCartney 	7
Oscar_De_La_Hoya 	7
Norm_Coleman 	7
Mike_Myers 	7
Mike_Martz 	7
Matthew_Perry 	7
Martin_Scorsese 	7
Mariah_Carey 	7
Liza_Minnelli 	7
Larry_Brown 	7
Justine_Pasek 	7
Jon_Gruden 	7
John_Travolta 	7
John_McCain 	7
John_Manley 	7
Jean-Pierre_Raffarin 	7
Holly_Hunter 	7
Gunter_Pleuger 	7
Goldie_Hawn 	7
Geoff_Hoon 	7
Elton_John 	7
Dennis_Kucinich 	7
David_Wells 	7
Bob_Stoops 	7
Binyamin_Ben-Eliezer 	7
Ben_Affleck 	7
Ana_Guevara 	7
Amelia_Vega 	7
Al_Sharpton 	7
Zinedine_Zidane 	6
Yoko_Ono 	6
Valery_Giscard_dEstaing 	6
Valentino_Rossi 	6
Tony_Stewart 	6
Tommy_Haas 	6
Thaksin_Shinawatra 	6
Tariq_Aziz 	6
Susan_Sarandon 	6
Steve_Lavin 	6
Silvan_Shalom 	6
Sarah_Jessica_Parker 	6
Sarah_Hughes 	6
Roy_Moore 	6
Roman_Polanski 	6
Rob_Marshall 	6
Robert_De_Niro 	6
Rick_Perry 	6
Ricardo_Sanchez 	6
Paula_Radcliffe 	6
Natalie_Coughlin 	6
Monica_Seles 	6
Mike_Krzyzewski 	6
Michael_Douglas 	6
Marco_Antonio_Barrera 	6
Luis_Horna 	6
Luis_Ernesto_Derbez_Bautista 	6
Leonid_Kuchma 	6
Kamal_Kharrazi 	6
Jose_Manuel_Durao_Barroso 	6
JK_Rowling  6
Jim_Furyk 	6
Jay_Garner 	6
Jan_Ullrich 	6
Gwyneth_Paltrow 	6
Fujio_Cho  6
Elsa_Zylberstein 	6
Edward_Lu 	6
Diana_Krall 	6
Dennis_Hastert 	6
Costas_Simitis 	6
Clint_Eastwood 	6
Clay_Aiken 	6
Christine_Todd_Whitman 	6
Charlton_Heston 	6
Carmen_Electra 	6
Cameron_Diaz 	6
Calista_Flockhart 	6
Bulent_Ecevit 	6
Boris_Becker 	6
Bob_Graham 	6
Billy_Crystal 	6
Arminio_Fraga 	6
Angela_Bassett 	6
Albert_Costa 	6
</pre></details>

## Introduction

This project is developed for have a plug-and-play facial recognition tool able to detect and recognize *__multiple__* faces from photos.
It aim to be inter-operable with other tool. For this purpose, it expose REST api in order to interact with the internal face-recognition engine (train/tune/predict) and return the result of the prediction in a JSON format.

It's written for be a basecode/project-template for future project where a more complicated facial detect + neural network have to be engaged.
But is a complete face recognition tool that can be deployed on Docker.
Currently it use a Multi Layer Perceptron (MLP) as neural network in order to predict the given faces.

The tool is powered with `Flask_MonitoringDashboard` that expose some useful utilization/performance graph at the `/dashboard` endpoint

## Requirements

- [face_recognition](https://github.com/ageitgey/face_recognition) Extract face point from image
- [Flask](https://github.com/pallets/flask) The Python micro framework for building web applications
- [Flask_MonitoringDashboard](https://github.com/flask-dashboard/Flask-MonitoringDashboard) Automatically monitor the evolving performance of Flask/Python web services
- [numpy](https://github.com/numpy/numpy) The fundamental package for scientific computing with Python.
- [olefile](https://github.com/decalage2/olefile) Parse, read and write Microsoft OLE2 files (deal with image)
- [Pillow](https://github.com/python-pillow/Pillow) The friendly PIL fork (Python Imaging Library)
- [py-bcrypt](https://code.google.com/archive/p/py-bcrypt/) Python wrapper of OpenBSD's Blowfish password hashing code
- [redis-py](https://github.com/andymccurdy/redis-py) The Python interface to the Redis key-value store.
- [scikit-learn](https://github.com/scikit-learn/scikit-learn) Machine learning in Python
- [tqdm](https://github.com/tqdm/tqdm) A Fast, Extensible Progress Bar
- [werkzeug](https://github.com/pallets/werkzeug) The comprehensive WSGI web application library

***NOTE***: If you encounter an error during `pip install -r requirements.txt`, it's possible that you have not installed `cmake`. `dlib` need `cmake`.
You can install `cmake` using:  

- `apt install cmake -y` (Debian/Ubuntu).  
- `yum install cmake -y` (CentOS/Fedora/RedHat).

## Table Of Contents

- [PyRecognizer](#pyrecognizer)
  - [Video guide for train/predict](#video-guide-for-trainpredict)
  - [Model tuned for some celebrities](#model-tuned-for-some-celebrities)
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

At this point all the necessary library for run the tool are ready, and you can run the software.

## Usage

You can view the following example video in order to understand how to interact with the tool for the following process:

- Create dataset from images
- Predict image
- Train/Tune the neural network

[Video guide for train/predict](#video-guide-for-trainpredict)  

Before you can train the neural network with the photos, you need to create an archive that contains the image of the people's faces that you want to predict.

- Save a bunch of images of the people that you need to recognize.
- Copy the image in a folder. The name of that folder is important, cause it will be used as a label for the dataset (images) that contains during prediction.
- Compress the folders in a `zip` file.

Before train the neural network, you have to create a dataset with the people images that you want to recognize.
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

You can find an example dataset at the following link:
<https://www.kaggle.com/jessicali9530/lfw-dataset>

Some people in this dataset have only very few image.

We can create a new one dataset using the following `bash` command, in order to extract only the people that contains more than 5 images:

```bash
# Extract only the people that have more than 5 photos (-gt 5)
for i in $(ls); do a=$(ls $i |wc -l); if [ "$a" -gt 5 ]; then echo $i ; fi ; done > people_ok
# Create a directory for store the images
mkdir -p /tmp/faces
# Copy the filtered directory in the new one
for i in $(cat people_ok  | xargs echo -n) ; do cp -r $i /tmp/faces/ ; done
```

At this point the dataset is complete and you can continue with training/tuning.

Backup and remove the already present model (if present,inside the `dataset/model` directory), the tool will understand that you want to train the model and will initialize a new MLP model. The model have the following name template: `%Y%m%d_%H%M%S`, related to the time that was generated.

Open your browser at the `endpoint:port/train` specified in the configuration file (`conf/test.json`) and you will be redirect to the Administrator login page.
**NOTE:** you can switch on/off the SSL, be sure to add `https` before the endpoint ip/hostname if it is enabled.  
**NOTE:** In order to access to the training/tuning page, you have to run the script in [utils/add_users.py](utils/add_users.py) for create an admin user, capable of manage the train/tune for the neural network.  
**NOTE:** A instance of `redis` have to be up and running if you want to train your custom neural network, cause the login will read the data from `redis`.

At this point you can upload the dataset (the previous `zip` file) and wait for the training of the neural network.

You can tail the log in `log/pyrecognizer.log` in order to understand the status of the training (`lnav` is your friends).

Once completed, the browser page will be refreshed automatically and you can:

- predict a new photos that the neural network haven't seen before, realated to the peoeple in the dataset.
- reduce the treeshold and see how you are similar to a celebrity!.

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
│   ├── conf.json                        # Tool configuration file
│   ├── dashboard.ini                    # File related to the Dashboard configuration
│   ├── flask_monitoringdashboard.db     # Dashboard database
│   ├── ssl                              # SSL Certificates folder
│   │   ├── localhost.crt
│   │   └── localhost.key

├── dataset                              # Model folder + test dataset
│   ├── face_training_dataset_little.zip # Model used for test train
│   ├── face_training_dataset.zip
│   └── model                            # Neural network model's folder
│       ├── 20191123_171821              # Folder for the NN model
│       │   ├── model.clf                # Neural network dumped
│       │   ├── model.dat                # Data used for train/tune
│       │   └── model.json               # Hyperparmaters of the NN
│       └── README.md
├── datastructure                        # Datastructure/Class used
│   ├── Administrator.py                 # Class that handle the admin of the NN, for train/tune
│   ├── Classifier.py                    # Class delegated to predict the photos
│   ├── Person.py                        # Class delegated to handle the "stuff" related to loading people data
│   └── Response.py                      # Class delegated to wrap the response
├── docker-compose.yml                   # docker-compose file for raise up the PyRecognizer (predict + train/tune)
├── Dockerfile                           # Dockerfile related to the PyRecognizer only (only predict)
├── LICENSE                              # License file
├── log                                  # Log folder
│   └── pyrecognizer.log
├── main.py                              # Main program to spawn the tool
├── README.md
├── requirements.txt                     # Dependencies file
├── uploads                              # Folder that contains the upload data
├── test                                 # Test folder
│   ├── conf_test.json
│   ├── test_classifier.py               # File with test cases
│   ├── test_images                      # Test data
│   │   ├── bush_test.jpg
│   │   ├── multi_face_test.jpg
│   │   └── unknown_face.jpg
│   ├── test_log                         # Log of the test
│   │   └── pyrecognizer.log
│   └── uploads
│       ├── predict
│       ├── training
│       ├── unknown
│       └── upload
│   ├── predict
│   ├── training
│   └── upload
├── utils                                
│   ├── add_users.py                     # Python file for add a new user for train/tune the network
│   └── util.py                          # Common methods
└── wsgi.py
```

## Example response

- **Missing the photo in request**

```text
{
  "response": {
    "data": null,
    "date": "2020-01-12 15:12:14.762526",
    "description": "You have sent a request without the photo to predict :/",
    "error": "NO_FILE_IN_REQUEST",
    "status": "KO"
  }
}
```

- **Missing threshold parameter in request**

```text
{
  "response": {
    "data": null,
    "date": "2020-01-12 15:12:14.769286",
    "description": "You have sent a request without the `threshold` parameter :/",
    "error": "THRESHOLD_NOT_PROVIDED",
    "status": "KO"
  }
}
```

- **Threshold provided is a number not in the properly range**

```text
{
  "response": {
    "data": null,
    "date": "2020-01-12 15:12:14.776730",
    "description": "Threshold have to be greater than 0 and lesser than 100!",
    "error": "THRESHOLD_ERROR_VALUE",
    "status": "KO"
  }
}
```

- **File in request is not a valid one**
  
```text
{
  "response": {
    "data": null,
    "date": "2019-11-23 18:10:11.038329",
    "description": "Seems that the file that you have tried to upload is not valid ...",
    "error": "FILE_NOT_VALID",
    "status": "KO"
  }
}
```

- **Error parsing the threshold parameter**

```text
{
  "response": {
    "data": null,
    "date": "2020-01-12 15:12:14.784154",
    "description": "Threshold is not an integer!",
    "error": "UNABLE_CAST_INT",
    "status": "KO"
  }
}
```

- **Dataset upload is not valid**
  
```text
{
  "response": {
    "data": null,
    "date": "2019-11-23 18:10:11.038329",
    "description": "Seems that the dataset is not valid",
    "error": "ERROR DURING LOADING DAT",
    "status": "KO"
  }
}
```

- **Unable to detect a face**
  
```text
{
  "response": {
    "data": null,
    "date": "2019-11-23 18:10:11.038329",
    "description": "Seems that in this images there is no face :/",
    "error": "FACE_NOT_FOUND",
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
    "description": "FACE_NOT_RECOGNIZED",
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

- **Login not successfully**

```text
{
  "response": {
    "data": null,
    "date": "2019-11-23 18:27:55.761851",
    "description": "The password inserted is not valid!",
    "error": "PASSWORD_NOT_VALID",
    "status": "KO"
  }
}
```

- **Unable to connect to redis**

```text
{
  "response": {
    "data": null,
    "date": "2019-11-23 18:27:55.761851",
    "description": "Seems that the DB is not reachable!",
    "error": "UNABLE_CONNECT_REDIS_DB",
    "status": "KO"
  }
}
```


## Contributing

- Feel free to open issue in order to __*require new functionality*__;  
- Feel free to open issue __*if you discover a bug*__;  
- New idea/request/concept are very appreciated!;  

## Test

In order to run the basic test case, you need to:
- Spawn the `PyRecognizer` tool using `python main.py`
- Change directory into the `test/` folder
- Run `python -m unittest test_classifier.TestPredict`

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

- **Alessio Savi** - *Initial work & Concept* - [Linkedin](https://www.linkedin.com/in/alessio-savi-2136b2188/) - [Github](https://github.com/alessiosavi/PyRecognizer)

## Contributors
- **Alessio Savi** 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

Face data are sensible information. In order to mitigate the risk of stealing sensible data, the tool can run in SSL mode for avoid packet sniffing and secure every request using a CSRF mitigation
