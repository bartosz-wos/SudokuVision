import os
import cv2
import numpy as np
from sklearn.svm import SVC
import joblib

def create_data():
    X = []
    y = []

    fonts = [
        cv2.FONT_HERSHEY_SIMPLEX,
        cv2.FONT_HERSHEY_PLAIN,
        cv2.FONT_HERSHEY_DUPLEX,
        cv2.FONT_HERSHEY_COMPLEX
    ]

    for digit in range(1, 10):
        for font in fonts:
            for thickness in [1, 2, 3]:
                for scale in [1.0, 1.5, 2.0, 2.5]:
                    img = np.zeros((50, 50), dtype=np.uint8)

                    cv2.putText(img, str(digit), (10, 40), font, scale, 255, thickness)

                    coords = cv2.findNonZero(img)
                    if coords is not None:
                        x, y_b, w, h = cv2.boundingRect(coords)
                        cropped = img[y_b:y_b+h, x:x+w]

                        resized = cv2.resize(cropped, (28, 28), interpolation=cv2.INTER_AREA)

                        X.append(resized.flatten())
                        y.append(digit)

    return np.array(X), np.array(y)

if __name__ == "__main__":
    X, y = create_data()

    model = SVC(kernel='linear', C=1.0)
    model.fit(X,y)
    
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, 'svm_model.pkl')

    joblib.dump(model, model_path)
