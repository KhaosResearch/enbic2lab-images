FROM python:3.11.5-bullseye

LABEL Khaos Research Group <khaos.uma.es>

COPY LICENSE ACKNOWLEDGEMENTS

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_HOST=mongodb://192.168.219.5:27017
ENV MONGO_USERNAME=root
ENV MONGO_PASSWORD=kha0sd3v
ENV MONGO_DATABASE=enbic2lab
ENV MONGO_COLLECTION=enbic2lab_import2db

ENTRYPOINT ["python", "main.py"]