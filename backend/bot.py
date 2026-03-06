"""
Bot de soumission pour Microsoft Forms.
"""

import json
from datetime import datetime, timezone

import requests

from form_config import QUESTIONS, SUBMIT_URL, FORM_ID


def build_submission_payload(answers_dict):
    """Construit le payload de soumission pour Microsoft Forms."""
    now = datetime.now(timezone.utc)
    start_time = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    answers_list = []
    for question in QUESTIONS:
        qid = question["id"]
        if qid not in answers_dict or answers_dict[qid] is None:
            continue

        answer = answers_dict[qid]

        if question["type"] == "choice_multi" and isinstance(answer, list):
            value = ";".join(answer)
        elif question["type"] in ("rating", "nps"):
            value = str(answer)
        else:
            value = str(answer)

        answers_list.append({"questionId": qid, "answer1": value})

    return {
        "startDate": start_time,
        "submitDate": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "answers": json.dumps(answers_list),
    }


def submit_single(answers_dict):
    """Soumet une seule reponse. Retourne le resultat."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://forms.office.com",
        "Referer": f"https://forms.office.com/Pages/ResponsePage.aspx?id={FORM_ID}",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/133.0.0.0 Safari/537.36"
        ),
    }

    payload = build_submission_payload(answers_dict)

    try:
        response = requests.post(SUBMIT_URL, json=payload, headers=headers, timeout=30)
        resp_data = {}
        try:
            resp_data = response.json()
        except Exception:
            pass

        return {
            "status": response.status_code,
            "success": response.status_code in (200, 201, 204),
            "form_id": resp_data.get("id"),
        }
    except requests.RequestException as e:
        return {
            "status": 0,
            "success": False,
            "error": str(e),
        }
