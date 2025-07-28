import os
import requests

AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

def get_ai_suggestions(code_report):
    url = f"{AZURE_ENDPOINT}/language/:analyze-text?api-version=2023-04-01"
    headers = {"Ocp-Apim-Subscription-Key": AZURE_KEY, "Content-Type": "application/json"}

    data = {
        "kind": "Language",
        "analysisInput": {
            "documents": [{"id": "1", "language": "en", "text": code_report}]
        },
        "parameters": {"modelVersion": "latest"}
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("documents", [{}])[0].get("text", "No feedback")
    return "Azure analysis failed"
