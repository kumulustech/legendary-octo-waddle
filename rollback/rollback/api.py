import os
import json
import logging

from flask import Blueprint, flash, g, redirect, request, jsonify, session, url_for
import kubernetes


LOG_LEVEL = str(os.getenv("LOG_LEVEL", "WARN")).upper()

logging.basicConfig(level=LOG_LEVEL)
logging.root.setLevel(LOG_LEVEL)

state_data = {}

with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as in_file:
    namespace = in_file.read()

kubernetes.config.load_incluster_config()

core_client = kubernetes.client.CoreV1Api()
apps_client = kubernetes.client.AppsV1Api()
api_client = kubernetes.client.ApiClient()

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/", methods=["POST", "GET"])
def api():
    if request.method == "POST":
        record = json.loads(request.data)
        logging.info(f"api:root:POST - received request: {record}")
        fix_issue(record)
        return f"{record}"
    logging.info(f"api:root:GET - received parameters: {request.status_code}")
    return '{"status":"ok"}'


def fix_issue(record):
    replicasets = apps_client.list_namespaced_replica_set(namespace)
    pod = None
    for alert in record["alerts"]:
        if "PodUnscheduleable" in alert["labels"]["alertname"]:
            if alert["status"] == "firing":
                pod = alert["labels"]["pod"]
    if pod == None:
        return '{"status":"NoAlertFiring"}'
    deployment, rs_gen, pod_gen = pod.split("-")
    logging.info(f"api:fix_issue - Unscheduleable pod in Deployment: {deployment}")
    deployments = apps_client.list_namespaced_deployment(namespace)
    for item in deployments.items:
        if deployment in item.metadata.name:
            dep = api_client.sanitize_for_serialization(item)
            logging.debug(
                f"api:fix_issue - pod spec: {dep['spec']}"
            )
    spec = []
    for n in replicasets.items:
        if deployment in n.metadata.name:
            spec.append(api_client.sanitize_for_serialization(n))

    items = {}
    for item in spec:
        items.update(
            {
                item["metadata"]["name"]: item["metadata"]["annotations"][
                    "deployment.kubernetes.io/revision"
                ]
            }
        )
    items = dict(sorted(items.items(), key=lambda item: item[1]))
    max = max_key = prev = prev_key = 0
    for k, v in items.items():
        if int(v) > int(max):
            prev = max
            prev_key = max_key
            max = v
            max_key = k

    logging.info(
        f"api:fix_issue: - Rollback to deployment.kubernetes.io/revision {prev} from {max}"
    )

    body = {}
    for item in spec:
        if prev_key in item["metadata"]["name"]:
            template = dep["spec"]["template"]
            template["spec"]["containers"][0]["resources"] = item["spec"]["template"][
                "spec"
            ]["containers"][0]["resources"]
            body = [
                {"op": "replace", "path": "/spec/template", "value": template},
                {
                    "op": "replace",
                    "path": "/metadata/annotations",
                    "value": dep["metadata"]["annotations"],
                },
            ]
            logging.debug(f"api:fix_issue - patch body {body}")
        logging.info(
            f"api:fix_issue - rev: {item['metadata']['annotations']['deployment.kubernetes.io/revision']} \n{item['spec']['template']['spec']['containers'][0]['resources']}"
        )

    logging.debug(
        f"api:fix_issue: - rolling back to spec {body[0]}"
    )
    response = apps_client.patch_namespaced_deployment(deployment, namespace, body)
    logging.debug(f"api_fix_issue: - K8s API patch response {response}")
    logging.info(f"api:fix_issue: - Rolled back {deployment} to version {prev_key}")

    deployments = apps_client.list_namespaced_deployment(namespace)
    for item in deployments.items:
        if deployment in item.metadata.name:
            dep = api_client.sanitize_for_serialization(item)
            logging.debug(
                f"api:fix_issue - Post patch deployment container spec {dep['spec']['template']['spec']['containers'][0]['resources']}"
            )
