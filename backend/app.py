"""
Application Flask - Interface graphique + API pour le bot de formulaire.
"""

import json
import os
import sys
import time
import random

from flask import Flask, Response, jsonify, render_template, request, stream_with_context

sys.path.insert(0, os.path.dirname(__file__))
from bot import submit_single, build_submission_payload
from form_config import QUESTIONS, get_sections
from strategies import resolve_strategy, get_strategies_info, ALL_STRATEGIES

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "..", "frontend", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend", "static"),
)

PROFILES_DIR = os.path.join(os.path.dirname(__file__), "..", "profiles")
os.makedirs(PROFILES_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/questions")
def api_questions():
    return jsonify(get_sections())


@app.route("/api/strategies")
def api_strategies():
    return jsonify(get_strategies_info())


@app.route("/api/strategies/<key>/preview")
def api_strategy_preview(key):
    answers = resolve_strategy(key)
    return jsonify({"answers": answers})


@app.route("/api/strategies/<key>/compare")
def api_strategy_compare(key):
    """Genere N apercus cote a cote pour montrer la variation."""
    n = min(int(request.args.get("n", 3)), 5)
    previews = []
    for _ in range(n):
        previews.append(resolve_strategy(key))
    return jsonify({"previews": previews})


@app.route("/api/dryrun", methods=["POST"])
def api_dryrun():
    """Genere le payload qui serait envoye, sans l'envoyer."""
    data = request.get_json()
    strategy = data.get("strategy")
    answers = data.get("answers", {})

    if strategy:
        resolved = resolve_strategy(strategy)
    else:
        resolved = answers

    payload = build_submission_payload(resolved)
    return jsonify({
        "payload": payload,
        "answers_resolved": resolved,
        "answer_count": len([v for v in resolved.values() if v is not None]),
    })


@app.route("/api/submit/stream", methods=["POST"])
def api_submit_stream():
    """Soumission en streaming SSE - envoie les resultats un par un."""
    data = request.get_json()
    strategy = data.get("strategy")
    answers = data.get("answers", {})
    count = min(data.get("count", 1), 100)
    delay_min = data.get("delay_min", 1.0)
    delay_max = data.get("delay_max", 3.0)

    def generate():
        for i in range(count):
            if strategy:
                current_answers = resolve_strategy(strategy)
            else:
                current_answers = answers

            result = submit_single(current_answers)
            result["attempt"] = i + 1
            result["total"] = count

            yield f"data: {json.dumps(result)}\n\n"

            if i < count - 1:
                time.sleep(random.uniform(delay_min, delay_max))

        yield f"data: {json.dumps({'done': True, 'total': count})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/submit", methods=["POST"])
def api_submit():
    """Soumission classique (non-streaming)."""
    data = request.get_json()
    strategy = data.get("strategy")
    answers = data.get("answers", {})
    count = min(data.get("count", 1), 100)

    results = []
    for i in range(count):
        if strategy:
            current_answers = resolve_strategy(strategy)
        else:
            current_answers = answers

        result = submit_single(current_answers)
        result["attempt"] = i + 1
        results.append(result)

        if i < count - 1:
            time.sleep(random.uniform(1, 3))

    return jsonify({"results": results})


@app.route("/api/profiles", methods=["GET"])
def list_profiles():
    profiles = []
    for f in os.listdir(PROFILES_DIR):
        if f.endswith(".json"):
            profiles.append(f[:-5])
    return jsonify({"profiles": sorted(profiles)})


@app.route("/api/profiles/<name>", methods=["GET"])
def load_profile(name):
    path = os.path.join(PROFILES_DIR, f"{name}.json")
    if not os.path.exists(path):
        return jsonify({"error": "Profil introuvable"}), 404
    with open(path) as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/profiles/<name>", methods=["POST"])
def save_profile(name):
    data = request.get_json()
    path = os.path.join(PROFILES_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return jsonify({"success": True})


@app.route("/api/profiles/<name>", methods=["DELETE"])
def delete_profile(name):
    path = os.path.join(PROFILES_DIR, f"{name}.json")
    if os.path.exists(path):
        os.remove(path)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
