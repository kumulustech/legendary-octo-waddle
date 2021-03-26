from flask import Blueprint, redirect, request, jsonify

bp = Blueprint("ready", __name__, url_prefix="/ready")


@bp.route("/", methods=["GET"])
def ready():
    return '{"status":"ready"}'
