FROM python:3.9.7-bullseye

LABEL Khaos Research Group <khaos.uma.es>

RUN apt-get update && apt-get install -y python3-dev
	
# Java
# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;
    
# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME
# End Java

COPY LICENSE ACKNOWLEDGEMENTS /mnt/shared/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install numpy~=1.26.2
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN curl -o ./bioformats/bioformats_package.jar https://downloads.openmicroscopy.org/bio-formats/6.9.1/artifacts/bioformats_package.jar
RUN chmod +x ./bioformats/bfconvert
RUN chmod +x ./bioformats/bf.sh

ENTRYPOINT ["python", "main.py"]
