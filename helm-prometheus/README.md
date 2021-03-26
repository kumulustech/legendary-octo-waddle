# Kubernetes, Helm Prometheus and Alerts, and the Google Bank-of-Anthos app

These scripts will help you launch and run an autoremediation service for unschedulable Pods
in a Kubernetes environment.

## Verify Prerequisites and install the running application

### 1 - Ensure you have a k8s cluster and can reach it

```sh
kubectl version
```

Ensure that helm 3 is installed

```sh
helm version
```

### 2 - Install Prometheus, Alertmanager, Rollback webhook, and the alert configuration

Install prometheus with Helm via the setup_prometheus.sh script

```sh
bash setup_prometheus.sh
```

Add the rollback webhook:

```sh
kubectl apply -f ../rollback/rollback.yaml -n bofa
```

In another terminal session, follow the rollback logs:

```sh
kubectl logs -f -n bofa -l app=rollback
```

### 3 - Deploy an app (using the Google Bank-of-Anthos sample application)

Deploy the bank-of-anthos test app:

```sh
bash launch_bofa.sh
```

Verify that the application is running

```sh
kubectl port-forward -n bofa svc/frontend 8080:80 >& /dev/null &
curl http://localhost:8080
# or
open http://localhost:8080 # in a web browser
```

## Generate an error - Emulate a bad configuration rollout

We'll emulate a new release that requires more capacity, which, on the target cluster is unprovisionable (e.g. too much memory requested)

```sh
kubectl apply -f bofa-update/frontend.yaml -n bofa
```

Verify that there is a pod that is "unprovisionable"

```sh
kubectl get pods -l app=frontend -n bofa
```

Wait ~3 minutes for the alert to be discovered, go into pending state, and the fire
  
The rollback function should rollback to the previous (initial good) cofiguration is re-applied. Verify that there is no longer a pod that is "unprovisionable". You should see these operations be discovered, and then acted upon from the rollback webhook application logs.

```sh
kubectl get pods -l app=frontend
```

## Additional queries

check to see if the pods are running:

```sh
 kubectl get pods -n bofa
```

Check the Prometheus ALERTS metric:

```sh
kubectl port-forward pod/`kubectl get pods -l component=server -n monitoring | awk '/Running/ {print $1}'` -n monitoring 9090

curl http://localhost:9090/api/v1/alerts
```

Check the state of the frontend deployment rollout:

```sh
kubectl rollout history deploy/frontend

kubectl rollout undo deploy/frontend --to-revision={previous}
```
