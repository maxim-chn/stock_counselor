FROM ubuntu:18.04

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y gnupg
RUN apt-get install -y sudo

# Mongodb
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org

# Nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs