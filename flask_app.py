import httpx
from flask import Flask, jsonify, render_template, request

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
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def _get_request_data():
    data = request.get_json(silent=True)
    if data is None:
        data = request.form.to_dict() or {}
    return data


@app.route("/", methods=["GET"])
def index():
    return render_template(
        TEMPLATE_NAME,
        backend_url="http://localhost:8000",
        user_id="user-123",
        message="Please schedule a meeting with my manager.",
    )


@app.route("/submit", methods=["POST"])
def submit_request():
    data = _get_request_data()
    backend_url = data.get("backend_url", "http://localhost:8000").rstrip("/")
    user_id = data.get("user_id", "user-123")
    message_text = data.get("message", "")

    request_result, error_message = fetch_json(
        f"{backend_url}/request",
        payload={"user_id": user_id, "message": message_text},
    )
    return jsonify({"result": request_result, "error": error_message})


@app.route("/audit", methods=["POST"])
def load_audit():
    data = _get_request_data()
    backend_url = data.get("backend_url", "http://localhost:8000").rstrip("/")

    audit_result, error_message = fetch_json(f"{backend_url}/audit")
    return jsonify({"result": audit_result, "error": error_message})


@app.route("/memory", methods=["POST"])
def load_memory():
    data = _get_request_data()
    backend_url = data.get("backend_url", "http://localhost:8000").rstrip("/")
    user_id = data.get("user_id", "user-123")

    memory_result, error_message = fetch_json(f"{backend_url}/memory/{user_id}")
    return jsonify({"result": memory_result, "error": error_message})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8500, debug=True)
