import os
import subprocess
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

DATA_DIR = ROOT_DIR / "data"
TEMP_INPUT = DATA_DIR / "temp_input.png"
FINAL_OUTPUT = DATA_DIR / "final_result.png"
BOARD_TXT = DATA_DIR / "board.txt"
SOLVED_TXT = DATA_DIR / "solved_board.txt"

SOLVER_EXEC = ROOT_DIR / "backend" / "build" / "solver"
VISION_MAIN = ROOT_DIR / "core" / "main.py"
VISION_RENDER = ROOT_DIR / "core" / "render.py"
INDEX_HTML = BASE_DIR / "index.html"

app = FastAPI(title="SudokuVision API")

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open(str(INDEX_HTML), "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error loading UI: {str(e)}"

@app.post("/solve")
async def solve_sudoku(file: UploadFile = File(...)):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(TEMP_INPUT, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    print(f"[*] API received: {file.filename} and saved it as {TEMP_INPUT}")

    try:
        print("[*] API triggers vision module...")
        vision_result = subprocess.run(
                ["python3", str(VISION_MAIN), str(TEMP_INPUT)],
                capture_output=True, text=True, check=True
        )
        print(vision_result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise HTTPException(status_code=500, detail="Vision processing failed")

    try:
        print("[*] API triggering C++ DLX solver...")
        solver_result = subprocess.run(
                [str(SOLVER_EXEC), str(BOARD_TXT), str(SOLVED_TXT)],
                capture_output=True, text=True, check=True
        )
        print(solver_result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise HTTPException(status_code=500, detail="C++ solver failed.")

    try:
        print("[*] API triggers renderer...")
        render_result = subprocess.run(
                ["python3", str(VISION_RENDER)],
                capture_output=True, text=True, check=True
        )
        print(render_result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise HTTPException(status_code=500, detail="Rendering image failed.")
    
    if not FINAL_OUTPUT.exists():
        raise HTTPException(status_code=500, detail="Final result image not found.")

    return FileResponse(str(FINAL_OUTPUT), media_type="image/png", filename="solved_sudoku.png")

@app.get("/ping")
def health_check():
    return {"status": "System is online and ready."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

