import cv2
import sys
import numpy as np

def load_board(file_path):
    board = []
    with open(file_path, 'r') as f:
        for line in f:
            row = [int(x) for x in line.split()]
            if row:
                board.append(row)
    return board

def main():
    try:
        original_board = load_board("data/board.txt")
        solved_board = load_board("data/solved_board.txt")
    except Exception as e:
        print(f"[-] Error: Cannot load board text files.")
        sys.exit(1)

    img = cv2.imread("data/warped_board.png")
    if img is None:
        print("[-] Error: Cannot load warped image.")
        sys.exit(1)

    height, width, _ = img.shape
    step_y = height // 9
    step_x = width // 9

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = min(step_y, step_x) / 35.0
    color = (0, 200, 0)
    thickness = max(2, int(font_scale * 2))

    for r in range(9):
        for c in range(9):
            if original_board[r][c] == 0:
                digit = str(solved_board[r][c])

                text_size = cv2.getTextSize(digit, font, font_scale, thickness)[0]
                text_x = (c * step_x) + (step_x - text_size[0]) // 2
                text_y = (r * step_y) + (step_y + text_size[1]) // 2

                cv2.putText(img, digit, (text_x, text_y), font, font_scale, color, thickness)

    output_path = "data/final_result.png"
    cv2.imwrite(output_path, img)
    print(f"[+] Final solution rendered and saved to {output_path}!")

if __name__ == "__main__":
    main()
