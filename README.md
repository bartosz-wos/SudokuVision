# SudokuVision

**Live Demo:** (https://sudokuvision-yezh.onrender.com/)
*(Note: Hosted on Render's free tier, it might take 30-50 seconds to spin up after a period of inactivity)*

## Overview
SudokuVision is a complete E2E cloud-ready pipeline that solves sudoku puzzles straight from images.
It started as a local bash script, now it is a fully dockerized REST API with responsive Web UI, powered by a very fast C++ backend and a Python based computer vision module.

## Tech Overview
- Frontend: HTML, CSS, Vanilla JS
- Backend API: Python, FastAPI, Uvicorn
- CV and ML: OpenCV, scikit-learn (SVM digit classifier)
- Core Solver: C++ (Knuth's Algorithm X with Dancing Links)
- Infrastructure: Docker, Render (for cloud hosting)

## How it works
1. **Interface:** The user uploads a Sudoku image via a browser
2. **API Layer:** FastAPI receives the image asynchronously and runs the pipeline
3. **Vision Module:** OpenCV applies perspective transform and extracts 81 cells. SVM model classifies the digits, generating a matrix
4. **C++ DLX Engine:** The matrix is passed to the C++ executable, which solves the exact cover problem very fast
5. **Rendering:** The solved digits are overlaid onto the original warped image and sent back to the client via the API

## Structure
```text
.
├── backend_cpp/        # DLX Engine in C++
├── vision_python/      # Computer Vision, SVM Model and processing
├── data/               # Temporary storage for processing
├── server.py           # REST API implementation in FastAPI
├── index.html          # Web UI
├── Dockerfile          # Containerization instructions
├── solve.sh            # CLI bash script for local execution
└── README.md           # Readme file
```

## Running Locally
You can run the exact same environment as the production server using Docker:
```bash
docker build -t sudokuvision .
docker run -p 8000:8000 sudokuvision
```
Then open `http://localhost:8000` in your browser

## The CLI Way
If you prefer to use it in terminal without the Web UI:
```bash
chmod +x solve.sh
./solve.sh path-to-your-image.png
```
And check the `data/` folder for the `final_result.png`.

