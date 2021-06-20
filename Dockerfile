FROM ubuntu:18.04
COPY . /usr/app/
EXPOSE 8000
WORKDIR /usr/app/
RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3.6 -y 
RUN apt install python3-pip -y
RUN pip3 install -r requirments.txt
