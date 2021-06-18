# pmhc-mds
The [Primary Mental Health Care - Minimum Data Set (PMHC-MDS)](https://docs.pmhc-mds.com/) describes a standard for collecting data about primary mental health service provision. Its objective is to enable consistent reporting and monitoring of services funded by the Australian Government and delivered via commissioning by the Primary Health Networks. More information about the PMHC-MDS is available [here](https://pmhc-mds.com/).

This repo is a project to create an open-source Flask application to collect the PMHC-MDS. The aims of this project are to:

* Provide a codebase for a secure and reliable application that can be deployed by an organisation into a live environment.
* Create an opportunity for a healthcare organisation to develop inhouse skills for web application development. 
* Create an opportunity for people in technology roles in healthcare organisations to collaborate and innovate, both in UX and data modelling. 

# Set up on local machine
## Flask virtual environment
1. Use Python’s venv module (part of core Python) to create the Flask virtual environment: 
```python -m venv flask```
2. Activate the environment:
* *Nix: ```source flask/bin/activate```
* Windows: ```flask\Scripts\activate.bat```
3. Install the required modules into the virtual environment: 
```pip install -r requirements.txt```
Note: if you make a change to the app that requires the installation of a module not previously installed, after you install the module you update the requirements for the Python virtual environment by running: ```pip freeze > requirements.txt```


# Troubleshooting
You get this message: 

```
flask/bin/python: bad interpreter: No such file or directory
```

You haven't set up the flask venv folder. 
