# SudokuVision (Pipeline that solves Sudoku with Computer Vision and Knuth's DLX with Dancing Links)

## How it works
SudokuVision is a pipeline designed to solve Sudoku puzzles from images. It uses Computer Vision techniques, Machine Learning (SVM), and optimized C++ backend.

Invidual modules do one thing and are run by a bash script in sequence.

## Architecture

1. **Computer Vision & ML (Python/OpenCV/scikit-learn)**
   - **Perspective Transform** Detects the Sudoku grid and warps the image.
   - **Cell Extraction & SVM** A custom-trained Support Vector Machine Digit Classificator
   - Outputs A standardized `board.txt` matrix.

2. **Solver with DLX**
   - **Algorithm X with Dancing Links** Exact cover algorithm implemented in C++ for speed.
   - Input: `board.txt` -> Output: `solved_board.txt`.

3. **Rendering (Python / OpenCV)**
   - Puts the computed sudoku board onto the original perspective-warped image.
   - Outputs `final_result.png`.

## Structure
```text
.
├── backend_cpp/        # DLX Engine in C++ and Makefile
├── vision_python/      # Computer Vision, SVM Model and Rendering
├── data/               # Test inputs intermediate txt files and outputs
├── solve.sh            # Pipeline bash script
└── README.md           # Readme file
