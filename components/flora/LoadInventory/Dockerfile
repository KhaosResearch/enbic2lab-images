FROM python:3.11.5-bullseye

LABEL Khaos Research Group <khaos.uma.es>

COPY LICENSE ACKNOWLEDGEMENTS /mnt/shared/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG mongo_host
ENV MONGO_HOST=${mongo_host}
ARG mongo_username
ENV MONGO_USERNAME=${mongo_username}
ARG mongo_access_key
ENV MONGO_ACCESS_KEY=${mongo_access_key}
ARG mongo_database
ENV MONGO_DATABASE=${mongo_database}

ENTRYPOINT ["python", "main.py"]