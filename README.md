# TDD Fraud Detection GCP Project
In this project Fraud Detection Classification Machine Learning model is created using AutoML Tables. The main folders of the project are described below.
## src 
Src folder contains the pre processing python code and AutoML Tables related code.
## tests
Tests folder contains the Unittest tests written for pre processing and automl tables model creation.
## terraform

In this project terraform is used to create reources in the cloud and following are the commands used to execute the scripts. 

    terraform init
    terraform apply


## controls
To test the resource creation, InSpec GCP scripts are used and following are the commands used to run the tests.

    set GOOGLE_APPLICATION_CREDENTIALS={service-account-credentials path}
    inspec exec fraud-detection-project-profile --input-file=fraud-detection-project-profile/inputs.yml -t gcp://



