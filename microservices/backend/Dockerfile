FROM python:3.7-alpine

ADD requirements.pip requirements.pip
RUN pip3 install -r requirements.pip

ADD src src

EXPOSE 5000
EXPOSE 8000

CMD ["python3", "/src/run.py"]
