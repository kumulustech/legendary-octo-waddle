# Kubernetes, Helm Prometheus and Alerts, and the Google Bank-of-Anthos app

Ensure you have a k8s cluster and can reach it (there is a sample GKE script that can help)

```sh
kubectl get nodes
```

Install prometheus with Helm via the setup_prometheus.sh script

```sh
bash setup_prometheus.sh
```

Deploy the bank-of-anthos test app:

```sh
bash launch_bofa.sh
```

Add the rollback webhook:

```sh
kubectl apply -f ../rollback/rollback.yaml
```

Check [../rollback/README.md](file:///../rollback/README.md) for more on validating the rollback remediation function