from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import shutil
from app.analyzer import analyze_code

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

class CodeRequest(BaseModel):
    code: str

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_code_input(req: CodeRequest):
    temp_file = "temp_code.py"
    with open(temp_file, "w") as f:
        f.write(req.code)
    results = analyze_code(temp_file)
    return {"suggestions": results}

@app.post("/analyze-file")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    temp_file = f"uploaded_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    results = analyze_code(temp_file)
    return {"suggestions": results}
