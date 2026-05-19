import json

import httpx
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-with-your-secret"

TEMPLATE_NAME = "index.html"

def fetch_json(endpoint: str, payload=None):
    try:
        if payload is None:
            response = httpx.get(endpoint, timeout=30.0)
        else:
            response = httpx.post(endpoint, json=payload, timeout=30.0)

        response.raise_for_status()
        return json.dumps(response.json(), indent=2), None
    except Exception as exc:
        return None, str(exc)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        TEMPLATE_NAME,
        backend_url="http://localhost:8000",
        user_id="user-123",
        message="",
        request_result=None,
        audit_result=None,
        memory_result=None,
        error_message=None,
    )


@app.route("/submit", methods=["POST"])
def submit_request():
    backend_url = request.form.get("backend_url", "http://localhost:8000").rstrip("/")
    user_id = request.form.get("user_id", "user-123")
    message_text = request.form.get("message", "")

    request_result, error_message = fetch_json(
        f"{backend_url}/request",
        payload={"user_id": user_id, "message": message_text},
    )

    return render_template(
        TEMPLATE_NAME,
        backend_url=backend_url,
        user_id=user_id,
        message=message_text,
        request_result=request_result,
        audit_result=None,
        memory_result=None,
        error_message=error_message,
    )


@app.route("/audit", methods=["POST"])
def load_audit():
    backend_url = request.form.get("backend_url", "http://localhost:8000").rstrip("/")
    user_id = request.form.get("user_id", "user-123")
    message_text = request.form.get("message", "")

    audit_result, error_message = fetch_json(f"{backend_url}/audit")

    return render_template(
        TEMPLATE_NAME,
        backend_url=backend_url,
        user_id=user_id,
        message=message_text,
        request_result=None,
        audit_result=audit_result,
        memory_result=None,
        error_message=error_message,
    )


@app.route("/memory", methods=["POST"])
def load_memory():
    backend_url = request.form.get("backend_url", "http://localhost:8000").rstrip("/")
    user_id = request.form.get("user_id", "user-123")
    message_text = request.form.get("message", "")

    memory_result, error_message = fetch_json(f"{backend_url}/memory/{user_id}")

    return render_template(
        TEMPLATE_NAME,
        backend_url=backend_url,
        user_id=user_id,
        message=message_text,
        request_result=None,
        audit_result=None,
        memory_result=memory_result,
        error_message=error_message,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8500, debug=True)
