#!/bin/bash
apt update -y
apt install git -y
mkdir /var/repodata/
cd /var/repodata/
git clone https://github.com/AcalephStorage/awesome-devops.git
apt install mc -y

