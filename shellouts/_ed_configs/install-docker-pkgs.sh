#!/bin/bash

apt-get update -y 

#snap install docker
apt-get install docker.io docker-compose -y || exit 9
