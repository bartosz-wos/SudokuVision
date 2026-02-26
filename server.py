import os
import subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SudokuVision API")

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

DATA_DIR = "data"
TEMP_INPUT = os.path.join(DATA_DIR, "temp_input.png")
FINAL_OUTPUT = os.path.join(DATA_DIR, "final_result.png")
SOLVER_EXEC = "./backend_cpp/build/solver"

@app.post("/solve")
async def solve_sudoku(file: UploadFile = File(...)):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TEMP_INPUT, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    print(f"[*] API received: {file.filename} and saved it as {TEMP_INPUT}")

    try:
        print("[*] API triggers vision module...")
        vision_result = subprocess.run(
                ["python3", "vision_python/main.py", TEMP_INPUT],
                capture_output=True, text=True, check=True
        )
        print(vision_result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise HTTPException(status_code=500, detail="Vision processing failed")

    try:
        print("[*] API triggering C++ DLX solver...")
        solver_result = subprocess.run(
                [SOLVER_EXEC],
                capture_output=True, text=True, check=True
        )
        print(solver_result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise HTTPException(status_code=500, detail="C++ solver failed.")

    try:
        print("[*] API triggers renderer...")
        render_result = subprocess.run(
                ["python3", "vision_python/render.py"],
                capture_output=True, text=True, check=True
        )
        print(render_result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise HTTPException(status_code=500, detail="Rendering image failed.")
    
    if not os.path.exists(FINAL_OUTPUT):
        raise HTTPException(status_code=500, detail="Final result image not found.")

    return FileResponse(FINAL_OUTPUT, media_type="image/png", filename="solved_sudoku.png")

@app.get("/ping")
def health_check():
    return {"status": "System is online and ready."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

