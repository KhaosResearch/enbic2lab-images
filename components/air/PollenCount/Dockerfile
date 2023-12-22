FROM python:3.11.5-bullseye

LABEL Khaos Research Group <khaos.uma.es>

COPY LICENSE ACKNOWLEDGEMENTS /mnt/shared/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

ENTRYPOINT ["python", "main.py"]