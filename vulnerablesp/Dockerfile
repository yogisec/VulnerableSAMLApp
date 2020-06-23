FROM ubuntu:bionic

RUN apt-get update -y
RUN apt-get install -y python2.7 python2.7-dev libxmlsec1 libxmlsec1-dev git python-pip python-dev build-essential nginx
RUN pip install --upgrade pip
RUN pip install -U setuptools

COPY . /vulnerableSP
WORKDIR /vulnerableSP

RUN pip install uwsgi
RUN pip install -r requirements.txt

RUN python /vulnerableSP/setup.py install

EXPOSE 8000

WORKDIR /vulnerableSP/yogiSP
#CMD ["python", "index.py"]
CMD ["uwsgi", "--ini", "vulnsp.ini"]
