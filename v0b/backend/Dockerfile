FROM gcr.io/google_appengine/python

RUN virtualenv -p python3.6 /env

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

RUN sudo apt-get install build-essential swig
RUN curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt | xargs -n 1 -L 1 pip install
RUN pip install auto-sklearn

CMD python -m quiz.console.worker
