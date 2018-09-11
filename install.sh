# sudo apt-get install python-setuptools python3-dev build-essential swig
# wget https://raw.githubusercontent.com/vanoudh/hello/master/install.sh

# basics
sudo apt-get install build-essential swig git
sudo apt-get install python3 python3-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip install --upgrade virtualenv

# virtual env
virtualenv --python python3 env1
source env1/bin/activate 

# app
git clone https://github.com/vanoudh/hello.git
pip install flask flask-login pandas pyopenssl category_encoders

# auto sklearn
curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt | xargs -n 1 -L 1 pip install
pip install auto-sklearn

# gunicorn
pip install gunicorn

# run
gunicorn app:app --chdir hello
