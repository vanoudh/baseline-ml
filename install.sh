# sudo apt-get install python-setuptools python3-dev build-essential swig

# basics
sudo apt-get install build-essential swig
easy_install pip

# virtual env
pip install --upgrade virtualenv
virtualenv --python python3 env1
source env1/bin/activate 

# app
pip install flask flask-login pandas pyopenssl category_encoders

# auto sklearn
curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt | xargs -n 1 -L 1 pip install
pip install auto-sklearn
