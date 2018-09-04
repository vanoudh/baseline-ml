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


echo "Deploying to App Engine"
cp ./frontend/app_template.yaml ./frontend/app.yaml
sed -i -e "s/\[GCLOUD_PROJECT\]/$PID/g" ./frontend/app.yaml
gcloud -q app deploy ./frontend/app.yaml

echo "Project ID: $PID"
