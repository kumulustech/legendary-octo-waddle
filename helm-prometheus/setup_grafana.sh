helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana/grafana --namespace monitoring grafana
