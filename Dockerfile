#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="ramadan"


# Any working direcrtory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/share/

#to COPY the remote file at working directory in container
COPY . ./
# Now the structure looks like this '/usr/app/src/test.py'


#CMD instruction should be used to run the software
#contained by your image, along with any arguments.
RUN apt update && \
      apt install -y curl && \
      curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
      chmod +x ./kubectl && \
      mv ./kubectl /usr/local/bin/kubectl
#CMD kubectl get pods
CMD [ "python", "./share.py"]
#In order to keep a POD running it should to be performing certain task
CMD ["sh", "-c", "tail -f /dev/null"]
