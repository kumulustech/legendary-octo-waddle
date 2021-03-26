from flask import Blueprint, redirect, request, jsonify
import requests
import logging
import os

LOG_LEVEL = str(os.getenv("LOG_LEVEL", "WARN")).upper()
PROM_URL = str(os.getenv("PROM_URL", "http://kube-prometheus-stack-server.monitoring.svc.cluster.local"))

logging.basicConfig(level=LOG_LEVEL)
logging.root.setLevel(LOG_LEVEL)

bp = Blueprint("ready", __name__, url_prefix="/ready")

@bp.route("/", methods=["GET"])
def ready():
    alerts=requests.get(url=f"{PROM_URL}/api/v1/alerts", headers={"content-type": "application/json", "accepts": "application/json"})
    logging.info(f"ready:root - prometheus alerts: {alerts.json()['data']}")
    return alerts.json()
