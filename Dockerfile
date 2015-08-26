FROM debian:wheezy
MAINTAINER BeneDicere
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install python python-pip -y && \
   apt-get clean autoclean && apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
RUN mkdir /app
ADD . /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD /app/updater.py