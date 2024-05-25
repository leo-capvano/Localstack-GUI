import streamlit as st

st.markdown("""
# :fire: Welcome to AWS GUI for Localstack
## Overview 

This application provides a graphical interface to manage Amazon S3 and AWS Secrets Manager on Localstack. 
Easily upload, view, and manage your S3 files and create, read, and update your AWS secrets.

---

## S3 Features :white_check_mark:
- create bucket
- list buckets
- delete bucket
- add object to a bucket
- list bucket objects
- see object details
- remove object from a bucket
- download an object from a bucket
- change AWS endpoint url

## Secrets Manager Features :white_check_mark:
- create secret
- list secrets
- delete secret
- see secret details
- see secret value
- change AWS endpoint url

---

## System Requirements
- docker 
- localstack on docker
```
cd localstack_gui/res
docker-compose -f docker-compose-localstack.yml up -d # to pull localstack image and run it into a docker container
docker ps # to check if the localstack container has been created and it is running
```
- python 3.12

---

## Usage
```
clone the project
cd localstack_gui
pip install -r requirements.txt
streamlit run ./Home.py
```

---

## Contribute

This is an open-source project, any contribution is appreciated.  
Thank You :raised_hands:

""")
