FROM gcr.io/google-appengine/python

RUN virtualenv -p python3.6 /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Upgrade pip
RUN pip3 install --upgrade pip

# Install dependencies
RUN curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt \
  | xargs -n 1 -L 1 pip3 install

# Install
RUN pip3 install pandas category_encoders auto-sklearn
