import os, requests
from app.analyzer import analyze_code

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

def get_changed_files():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    resp = requests.get(url, headers=headers)
    return [f["filename"] for f in resp.json()]

def post_review_comment(pr_url, comment):
    url = f"{pr_url}/reviews"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": comment, "event": "COMMENT"}
    requests.post(url, json=data, headers=headers)

if __name__ == "__main__":
    files = get_changed_files()
    for f in files:
        if f.endswith(".py"):
            results = analyze_code(f)
            for r in results:
                post_review_comment(f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}", r)
