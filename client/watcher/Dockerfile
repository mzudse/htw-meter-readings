FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir /home/watcher_files && chmod +x 

CMD ["python3", "watcher.py"]

EXPOSE 5004