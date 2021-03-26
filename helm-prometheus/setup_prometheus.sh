#!/bin/bash

echo "Add the helm repo for prometheus"
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

echo creat the monitoring namespace and install prometheus with the alertmanager webhook
kubectl create ns monitoring
helm install kube-prometheus-stack prometheus-community/prometheus --namespace monitoring --values alertmanager-values.yaml

#echo "check https://github.com/prometheus-operator/kube-prometheus for more info on prometheus"

echo "Add additional metrics monitoring"
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
echo "check metrics availability with: kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1"
helm install kube-prometheus-alerts prometheus-community/prometheus-adapter --namespace monitoring

