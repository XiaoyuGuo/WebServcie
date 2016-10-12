FROM ubuntu:16.04
RUN apt-get -y update && apt-get install -y python3 && apt-get install -y python3-pip && pip3 install flask && pip3 install Pillow
ADD image_server.py /home/image_server.py
EXPOSE 8888
CMD ["python3", "/home/image_server.py"]