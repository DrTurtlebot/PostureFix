import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import time

class Camera:
    def __init__(self, width, height, desired_fps):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.frame_time = 1.0 / desired_fps
        self.last_frame_time = time.time()

    def is_opened(self):
        return self.cap.isOpened()

    def get_frame(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_frame_time
        if elapsed_time < self.frame_time:
            time.sleep(self.frame_time - elapsed_time)
            return None
        self.last_frame_time = current_time
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
