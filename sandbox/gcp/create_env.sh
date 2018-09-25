#!/bin/bash

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

PID=$1

echo "Creating Project $PID"
gcloud projects create $PID
gcloud config set project $PID
gcloud alpha billing projects link $PID --billing-account 0152E2-3F9848-40A9A2

echo "Creating Datastore/App Engine instance"
gcloud app create --region "us-central"

echo "Creating bucket: gs://$PID-media"
gsutil mb gs://$PID-media

echo "Exporting GCLOUD_PROJECT and GCLOUD_BUCKET"
export GCLOUD_PROJECT=$PID
export GCLOUD_BUCKET=$PID-media
export GCLOUD_NICKNAME=$PID

# echo "Creating virtual environment"
# mkdir ~/venvs
# virtualenv ~/venvs/$GCLOUD_NICKNAME
# source ~/venvs/$GCLOUD_NICKNAME/bin/activate
#
# echo "Installing Python libraries"
# pip install --upgrade pip
# pip install -r requirements.txt

# echo "Creating Datastore entities"
# python2 add_entities.py

echo "Creating Service Account"
gcloud iam service-accounts create $PID-account --display-name "$PID Account"
gcloud iam service-accounts keys create $PID-key.json --iam-account=$PID-account@$PID.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=$PID-key.json

echo "Setting IAM Role"
gcloud projects add-iam-policy-binding $PID --member serviceAccount:$PID-account@$PID.iam.gserviceaccount.com --role roles/owner

# echo "Creating Cloud Pub/Sub topic"
# gcloud beta pubsub topics create feedback

# echo "Creating Cloud Spanner Instance, Database, and Table"
# gcloud spanner instances create quiz-instance --config=regional-us-central --description="Quiz instance" --nodes=1
# gcloud spanner databases create quiz-database --instance quiz-instance --ddl "CREATE TABLE Feedback ( feedbackId STRING(100) NOT NULL, email STRING(100), quiz STRING(20), feedback STRING(MAX), rating INT64, score FLOAT64, timestamp INT64 ) PRIMARY KEY (feedbackId);"

# echo "Enabling Cloud Functions API"
# gcloud beta services enable cloudfunctions.googleapis.com
#
# echo "Creating Cloud Function"
# gcloud beta functions deploy process-feedback --trigger-topic feedback --source ./function --stage-bucket $GCLOUD_BUCKET --entry-point subscribe


echo "Project ID: $PID"
