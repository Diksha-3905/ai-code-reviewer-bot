import os, requests
from app.analyzer import analyze_code
from app.azure_nlp import get_ai_suggestions

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

def get_changed_files():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    resp = requests.get(url, headers=headers)
    return [f["filename"] for f in resp.json()]

def post_review_comment(comment):
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/reviews"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": comment, "event": "COMMENT"}
    requests.post(url, json=data, headers=headers)

if __name__ == "__main__":
    files = get_changed_files()
    for f in files:
        if f.endswith(".py"):
            # Analyze locally
            basic_suggestions = analyze_code(f)
            # AI suggestions from Azure
            with open(f, "r") as file:
                code_content = file.read()
            ai_suggestions = get_ai_suggestions(code_content)

            # Combine suggestions
            comments = ["### 🤖 AI Code Review Suggestions:\n"]
            comments.extend([f"- {s}" for s in basic_suggestions])
            comments.append("\n### 🌐 Azure AI Suggestions:\n")
            comments.extend([f"- {s}" for s in ai_suggestions])

            post_review_comment("\n".join(comments))
