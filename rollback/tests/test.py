import os
import sys
import uuid
import time
import requests
import json


def main():
    job_id = str(uuid.uuid4())

    url = "http://127.0.0.1:5000/api/"
    header = {"content-type": "application/json", "accepts": "application/json"}
    data = {
        "version": "4",
        "groupKey": "UnschedulablePods",
        "truncatedAlerts": 0,
        "status": "firing",
        "externalURL": "http://alerts.svc.monitoring",
        "alerts": [
            {
                "status": "firing",
                "labels": {"pod": "frontend-123sdf234-234sdf"},
                "annotations": {},
                "generatorURL": "prometheus alert",
            },
        ],
    }
    data = {
        "receiver": "rollback-webhook",
        "status": "resolved",
        "alerts": [
            {
                "status": "resolved",
                "labels": {
                    "alertname": "PodUnscheduleable",
                    "pod": "frontend-84db8c8c89-jcc9j",
                    "severity": "rollback",
                },
                "annotations": {
                    "description": "Pod frontend-84db8c8c89-jcc9j has be unschedulable for more than 3 minutes.  Rollback should trigger",
                    "summary": "Pod frontend-84db8c8c89-jcc9j update is unschedulable",
                },
                "startsAt": "2021-03-24T15:00:54.80104526Z",
                "endsAt": "2021-03-24T15:12:54.80104526Z",
                "generatorURL": "http://kube-prometheus-stack-server-7b4cd58d4f-8xt57:9090/graph?g0.expr=sum+by%28pod%29+%28kube_pod_status_unschedulable%29+%3E+0&g0.tab=1",
                "fingerprint": "966ac0a4ed76728d",
            }
        ],
        "groupLabels": {},
        "commonLabels": {
            "alertname": "PodUnscheduleable",
            "pod": "frontend-84db8c8c89-jcc9j",
            "severity": "rollback",
        },
        "commonAnnotations": {
            "description": "Pod frontend-84db8c8c89-jcc9j has be unschedulable for more than 3 minutes.  Rollback should trigger",
            "summary": "Pod frontend-84db8c8c89-jcc9j update is unschedulable",
        },
        "externalURL": "http://localhost:9093",
        "version": "4",
        "groupKey": '{}/{severity=~"^(?:rollback)$"}:{}',
        "truncatedAlerts": 0,
    }

    print("get all tasks")
    print(get_api(url, header))

    print(f"triggering task")
    print(trigger_alert(url, header, job_id, data))


def trigger_alert(url, header, job_id, data):
    """start operation via post

    params:
    - url: service endpoint
    - header: header parameters
    - job_id: if needed
    - data: message to test

    returns: job_object
    """

    try:
        request = requests.post(url, data=json.dumps(data), headers=header)
        return request.text
    except:
        pass


def get_api(url, header):

    try:
        request = requests.get(f"{url}", headers=header)
        return request.json()
    except:
        pass


if __name__ == "__main__":
    main()
