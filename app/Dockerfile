FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
ADD main.py /app
ADD instrumentation /app/instrumentation
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]