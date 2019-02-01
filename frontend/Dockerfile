FROM python:3.5-alpine
ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
WORKDIR /app
CMD ["python", "PyMail.py"]

