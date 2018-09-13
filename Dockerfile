FROM docker.io/vanoudh/python-ml

# Add files
ADD . .

# Install
RUN pip3 install flask flask-login urllib3 gunicorn

# Run web app with one worker
ENTRYPOINT gunicorn -b 0.0.0.0:8080 --workers 1 --timeout 120 --log-level debug app:app