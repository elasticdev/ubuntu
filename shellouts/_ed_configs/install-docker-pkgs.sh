#!/bin/bash

apt-get update -y 

#snap install docker
apt-get install gnupg2 pass docker.io docker-compose -y || exit 9
