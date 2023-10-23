import cv2
import numpy as np

class BallDetector:
    def __init__(self):
        self.lower_yellow = np.array([20, 100, 100])
        self.upper_yellow = np.array([30, 255, 255])

    def detect_ball(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 10:
                return (int(x), int(y), int(radius))

        return None

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    detector = BallDetector()

    while True:
        ret, frame = cap.read()
        ball_coords = detector.detect_ball(frame)

        if ball_coords is not None:
            x, y, r = ball_coords
            print(f"Ball detected at ({x}, {y}) with radius {r}")
