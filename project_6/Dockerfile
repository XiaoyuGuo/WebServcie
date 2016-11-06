FROM ubuntu:16.04
RUN apt-get -y update && apt-get install -y python3 && apt-get install -y python3-pip && pip3 install flask && pip3 install psutil
ADD server /home/server
EXPOSE 5000
CMD ["python3", "/home/server/server.py"]