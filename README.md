# ATLAS Annotation Tool


## Introduction
Project ATLAS is an attempt to carry out a large scale and accurate mapping of UC Berkeley’s Campus, and develop generalizable algorithms based on this data for Augmented/ Virtual Reality (AR/VR). We are currently designing both hardware and software tools for data collection and annotation. This project involves designing, building and testing these tools to be incorporated in a beta version of the project.

## Getting Started
First clone the project
`git clone https://github.com/wuxiaohua1011/annotation_app.git && cd annotation_app`

Create a virtual environment, we recommend with `Python 3.6`. Python Version has to `>= 3.6`

`conda create -n myenv python=3.6`

`conda activate myenv`

Install all necessary packages

`pip install -r requirements.txt`

Install a distribution of the app

`python setup.py install`

Run the main app

`python main.py`

Note: You should download data before start annotating. You can download data by going into the `Download/Upload` screen.



## Developers
Please first download Qt Designer, if you are going to do any thing related to GUI
https://build-system.fman.io/qt-designer-download

Fullstack Workflow:
1. Generate a .ui file using Qt Designer ([Tutorial](https://www.youtube.com/watch?v=Dmo8eZG5I2w)) and place it in the `/model` folder
2. Use the package [pyuic5](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html#pyuic5) to generate the associated python file in the `/view` folder
3. Code up the controller script and place it in the `/controller` folder
