import cv2
import numpy as np
import joblib
from sklearn.svm import SVC

def order_points(pts):
    rect = np.zeros((4,2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def process_image(image_path):
    print(f"[*] Opening file: {image_path}")
    img = cv2.imread(image_path)

    if img is None:
        print(f"[!] Error: Couldn't load the image.")
        return

    print("[*] Loading the SVM model...")

    try:
        model = joblib.load('svm_model.pkl')
    except Exception as e:
        print("[!] svm_model.pkl not found! Run train_model.py first!")
        return

    height, width = img.shape[:2]
    max_height = 800
    if(height > max_height):
        scaling_factor = max_height / float(height)
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor,
                         interpolation=cv2.INTER_AREA)
    original = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    edges = cv2.Canny(blur, 50, 150)

    kernel = np.ones((5,5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    board_contour = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        if len(approx) == 4:
            board_contour = approx
            break

    if board_contour is not None:
        cv2.drawContours(img, [board_contour], -1, (0, 255, 0), 3)
        print("[+] Success: Found the contours!")

        pts = board_contour.reshape(4, 2)
        rect = order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(original, M, (maxWidth, maxHeight))

        warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        warped_blur = cv2.GaussianBlur(warped_gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(warped_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 55, 45)

        cv2.imshow("4 - Whole threshold mask", thresh)

        step_x = maxWidth // 9
        step_y = maxHeight // 9

        sudoku_grid = []
        for y in range(9):
            row = []
            for x in range(9):
                startX = x * step_x
                startY = y * step_y
                endX = (x + 1) * step_x
                endY = (y + 1) * step_y

                cell = thresh[startY:endY, startX:endX]

                trim_x = int(cell.shape[1] * 0.1)
                trim_y = int(cell.shape[0] * 0.1)
                if cell.shape[0] > trim_y * 2 and cell.shape[1] > trim_x * 2:
                    cell = cell[trim_y:cell.shape[0]-trim_y, trim_x:cell.shape[1]-trim_x]

                cell_contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cell_area = cell.shape[0] * cell.shape[1]

                if len(cell_contours) > 0:
                    largest_contour = max(cell_contours, key=cv2.contourArea)

                    for cc in cell_contours:
                        if cc is not largest_contour:
                            cv2.drawContours(cell, [cc], -1, 0, -1)

                    cell_h = cell.shape[0]
                    x_c, y_c, w_c, h_c = cv2.boundingRect(largest_contour)
                    
                    if h_c < cell_h * 0.45:
                        cell.fill(0)

                non_zero = cv2.findNonZero(cell)
                if non_zero is not None:
                    x_b, y_b, w_b, h_b = cv2.boundingRect(non_zero)

                    if w_b > 5 and h_b > 10:
                        digit_roi = cell[y_b:y_b+h_b, x_b:x_b+w_b]
                        resized_digit = cv2.resize(digit_roi, (28, 28), interpolation=cv2.INTER_AREA)

                        flattened = resized_digit.flatten().reshape(1, -1)
                        prediction = model.predict(flattened)[0]
                        row.append(int(prediction))
                    else:
                        row.append(0)
                else:
                    row.append(0)

            sudoku_grid.append(row)

        for r in sudoku_grid:
            print(r)

        cv2.imshow("3 - Straightened board", warped)
    else:
        print("[-] Error: Couldn't find the contours.")

    print("[*] Press any key to exit...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_image('../data/test3.png')
