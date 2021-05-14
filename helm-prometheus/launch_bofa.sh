#!/bin/bash

echo "create bofa namespace"
kubectl create ns bofa

echo "create JWT token and store in k8s secret for Bank-of-Anthos"
openssl genrsa -out jwtRS256.key 4096
openssl rsa -in jwtRS256.key -outform PEM -pubout -out jwtRS256.key.pub
kubectl create -n bofa secret generic jwt-key --from-file=./jwtRS256.key --from-file=./jwtRS256.key.pub --namespace bofa
rm ./jwt*key*

echo "launch kubectl"
kubectl apply -f bofa/ --namespace bofa