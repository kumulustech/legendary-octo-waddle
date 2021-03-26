# A Simple Rollback utility

A simple Flask based webhook utility to accept an Alertmanager Alert and trigger a `rollout undo` to the previous revision.

## Install

Use the pre-build container available on docker hub `kumulustech/rollback:0.1.0`, you can build

```or```

Build the container and push it to your own registry:

```sh
export REGISTRY_PATH=${YOUR_REGISTRY:-kumulustech}
docker build . -t ${REGISTRY_PATH}/rollback:0.1.0
docker push ${REGISTRY_PATH}/rollback:0.1.0 && docker push ${REGISTRY_PATH}/rollback:latest
```

and update the `image:` key value in the rollout.yaml document to `${REGISTRY_PATH}/rollback:0.1.0`

## Deploy to k8s

*NOTE* The rollback.yaml document has hardcoded expectations (for ClusterRoleBinding) to the 'bofa' namespace. Update if the rollback is going to run in a different namespace.

*NOTE* As specified above, if you build your own container, please update the image parameter in the rollback.yaml document

```sh
kubectl apply -f rollback.yaml -n bofa
```

## Test

TBD.  there is a sample test script in tests/test.py, but needs a bypass for the 
required "in cluster" kubernetes config.

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

Alertmanager will then send the alert message to the webhook as configured, and that will trigger a rollback to the previous deployment revision.