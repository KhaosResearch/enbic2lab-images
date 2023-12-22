FROM python:3.11.5-bullseye

LABEL Khaos Research Group <khaos.uma.es>

COPY LICENSE ACKNOWLEDGEMENTS /mnt/shared/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

# Environment variables
ENV MONGO_HOST=
ENV MONGO_USERNAME=
ENV MONGO_ACCESS_KEY=
ENV MONGO_DB=
ENV MONGO_COLLECTION=

ENTRYPOINT ["python", "main.py"]
