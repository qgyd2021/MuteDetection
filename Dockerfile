FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["python3", "run_voicemail_detection_server.py"]
