FROM python:3

WORKDIR /cmartires_CS446_PA4

COPY pythonCode2.py pythonCode2.py

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

CMD ["python3", "pythonCode2.py", "--host=0.0.0.0"]