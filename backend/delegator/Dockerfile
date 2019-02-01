FROM python:3.6-alpine
ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
WORKDIR /app
CMD ["python", "main.py"]

