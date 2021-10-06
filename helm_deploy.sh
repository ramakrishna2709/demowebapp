#!/bin/bash

#Helm deploy chart with default namespace(for demo)

helm install --name demoapp ./webapp

#Helm list charts
helm list 

#get deployments

kubectl get all -A

##helm delete chart

#helm delete demoapp
