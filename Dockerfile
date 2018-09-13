FROM ubuntu

# System requirements
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  python3-pip \
  swig \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Install auto-sklearn dependencies
RUN curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt \
  | xargs -n 1 -L 1 pip3 install


# Add app files
ADD . /

# Install
RUN pip3 install -r requirements.txt

# RUN pip3 install flask flask-login urllib3 pandas gunicorn

ENTRYPOINT gunicorn -b 0.0.0.0:8080 --workers 1 --timeout 120 --log-level debug app:app