#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo -e "\033[1;31m[!] Error: Input path to the Sudoku image!\033[0m"
	echo -e "Usage: ./solve.sh <file_path>"
	exit 1
fi

IMAGE_PATH=$1

echo -e "\033[1;34m[*] Running the Vision Module...\033[0m"

source vision_python/venv/bin/activate
python vision_python/main.py "$IMAGE_PATH"

PYTHON_STATUS=$?
deactivate

if [ $PYTHON_STATUS -ne 0 ]; then
	echo -e "\033[1;31m[-] Vision Module got an error. Exitting.\033[0m"
	exit 1
fi

make -C backend_cpp > /dev/null 2>&1

echo -e "\033[1;36m[*] Running the Core DLX...\033[0m"

./backend_cpp/build/solver
SOLVER_STATUS=$?

if [ $SOLVER_STATUS -eq 0 ]; then
	echo -e "\033[1;33m[*] Rendering the final image...\033[0m"
	
	source vision_python/venv/bin/activate
	python vision_python/render.py
	deactivate

	echo -e "\033[1;32m[+] Pipeline executed successfully! Check data/final_result.png\033[0m"
elif [ $SOLVER_STATUS -eq 2 ]; then
	echo -e "\033[1;31m[-] Solver finished, but no solution exists.\033[0m"
	exit 2
else
	echo -e "\033[1;31m[-] Core DLX encountered a fatal error.\033[0m"
	exit 1
fi
