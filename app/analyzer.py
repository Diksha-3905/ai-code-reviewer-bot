import subprocess
from app.azure_nlp import get_ai_suggestions

def run_static_analysis(path):
    result = subprocess.run(["pylint", path], capture_output=True, text=True)
    return result.stdout

def analyze_code(path):
    static_results = run_static_analysis(path)
    ai_feedback = get_ai_suggestions(static_results)

    comments = []
    for line in ai_feedback.splitlines():
        if "suggestion" in line.lower():
            comments.append(line)
    return comments
