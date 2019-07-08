Copied and tested from Starter for deploying [fast.ai](https://www.fast.ai) models on [Render](https://render.com)

Tested on Windows docker environment.

Model file is kept under app, where the server.py file resides.


# Steps to run in windows environment are:

Download this repository in a local folder, say C:\docker-starter

Open Command Prompt.

Navigate to the directory as above, Dockerfile should be visible.

docker build C:\docker-starter

To check the images type, docker images

docker run  -p 5000:5000 <image-name-you-want-to-run>, e.g. e76782de76a6
  
to shutdown

find the instance by writing docker ps

docker stop <instance-name>, e.g., 
