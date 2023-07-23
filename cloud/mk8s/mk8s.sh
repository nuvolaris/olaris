#!/bin/bash
apt update
apt install -y snapd curl grep sudo
snap install microk8s --classic
microk8s stop
IP="$(curl -sL http://169.254.169.254/latest/meta-data/public-ipv4)"
sed -i "/IP.1/a IP.2 = $IP" /var/snap/microk8s/current/certs/csr.conf.template
microk8s start
while microk8s kubectl get nodes | grep NotReady
do echo Waiting for Ready ; sleep 5
done
microk8s enable hostpath-storage dns ingress cert-manager
