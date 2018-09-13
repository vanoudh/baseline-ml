docker build -t python-ml .
docker tag python-ml vanoudh/python-ml
docker login
docker push vanoudh/python-ml