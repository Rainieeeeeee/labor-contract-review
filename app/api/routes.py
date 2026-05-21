from fastapi import FastAPI, UploadFile, File
import tempfile, os
from scripts.run_analysis import run_analysis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete = False, suffix=".txt") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    results = run_analysis(tmp_path)
    os.unlink(tmp_path)
    return results
