FROM python:3.6-alpine
RUN apk add --no-cache --allow-untrusted --repository http://dl-3.alpinelinux.org/alpine/edge/testing hdf5 hdf5-dev
RUN apk add --no-cache build-base gcc musl-dev hdf5-dev lapack-dev gfortran git jpeg-dev zlib-dev
ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN pip install https://github.com/better/alpine-tensorflow/releases/download/alpine3.7-tensorflow1.7.0/tensorflow-1.7.0-cp36-cp36m-linux_x86_64.whl
RUN pip install git+https://www.github.com/keras-team/keras-contrib.git
WORKDIR /app
CMD ["python", "-u", "main.py"]

