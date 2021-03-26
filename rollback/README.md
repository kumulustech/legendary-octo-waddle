# A Simple Rollback utility

A simple Flask based webhook utility to accept an Alertmanager Alert and trigger a `rollout undo` to the previous revision.

## Install

1. Install a K8s Cluster (GCP, EKS, etc. should all be fine)
2. Install prometheus and the prometheus alert manager (see the [helm-prometheus](file:///../helm-prometheus) directory).
3. Launch the rollout.yaml app against the namespace of the app (note the service account assumes 'bofa' as the namespace, see the end of the rollout.yaml document)

## Test

### 1. Install an application

(see the bofa app [helm-prometheus/bofa](file:///../helm-prometheus/bofa) directory) 

```sh
kubectl create ns bofa; kubectl apply -f helm-prometheus/bofa -n bofa
```

### 2. Verify that the app is running

```sh
kubectl port-forward -n bofa svc/frontend 8080:80 >& /dev/null & curl localhost:8080
```

### 3. Trigger an update to the frontend app 

We'll emulate a new release that requires more capacity, which, on the target cluster is unprovisionable (e.g. too much memory requested)

```sh
kubectl apply -f helm-prometheus/bofa-update/frontend.yaml
```

### 4. verify that there is a pod that is "unprovisionable"

```sh
kubectl get pods -l app=frontend
```

### 5. wait ~3 minutes.
  
The rollback function should rollback to the previous (initial good) cofiguration is re-applied. Verify that there is no longer a pod that is "unprovisionable"

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

## Functional Concept

Input is a Prometheus Alert

```json
{
  "version": "4",
  "groupKey": <string>,              // key identifying the group of alerts (e.g. to deduplicate)
  "truncatedAlerts": <int>,          // how many alerts have been truncated due to "max_alerts"
  "status": "<resolved|firing>",
  "receiver": <string>,
  "groupLabels": <object>,
  "commonLabels": <object>,
  "commonAnnotations": <object>,
  "externalURL": <string>,           // backlink to the Alertmanager.
  "alerts": [
    {
      "status": "<resolved|firing>",
      "labels": <object>,
      "annotations": <object>,
      "startsAt": "<rfc3339>",
      "endsAt": "<rfc3339>",
      "generatorURL": <string>       // identifies the entity that caused the alert
    },
    ...
  ]
}
```

An alert rule of the following format is the expected trigger:

```yaml
groups:
- name: deployment state
    rules:
    - alert: PodUnscheduleable
    expr: sum by (pod) (kube_pod_status_unschedulable) > 0
    for: 3m
    labels:
        severity: rollback
    annotations:
        summary: "Pod {{ $labels.pod }} update is unschedulable"
        description: "Pod {{ $labels.pod }} has be unschedulable for more than 3 minutes.  Rollback should trigger"
```

The expression will generate a label of the form:

```json
{"alerts":{"labels":{"alertname":"PodUnscheduleable","pod":"deployment-~rs~-~pod~","severity":"rollback"}}}
```

Alertmanager will then send the alert message to the webhook as configured, and that will trigger a rollback to
the previous deployment revision.