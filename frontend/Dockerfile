FROM python:3.5-alpine
RUN apk add --no-cache build-base gcc musl-dev lapack-dev gfortran git jpeg-dev zlib-dev
ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
WORKDIR /app
CMD ["python", "-u", "PyMail.py"]
