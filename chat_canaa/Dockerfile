FROM python:alpine 

LABEL Name=carminho Version=0.0.1
EXPOSE 5005

ADD . /app 
WORKDIR /app

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install pip --upgrade

CMD docker-compose.yml
CMD ["python3", "start.py"]
