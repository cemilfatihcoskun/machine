import threading
from queue import Queue, Empty

import cv2

from src.logger import logger

class CameraStream:
    def __init__(self, source, width, height):
        self.source = source
        self.width = width
        self.height = height
        self.cap = None 
        self.running = False
        self.thread = None
        self.frame_queue = Queue(maxsize=1)

    def start(self):
        logger.info(f"Connecting to the camera stream {self.source}.")
        self.cap = cv2.VideoCapture(self.source)
        
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if not self.cap.isOpened():
            logger.error("Could not started the connection.")
            return False

        self.running = True
        self.thread = threading.Thread(target=self._reader_loop, daemon=True)
        self.thread.start()
        logger.info("Camera connection is started.")
        return True

    def _reader_loop(self):
        while self.running:
            if not self.cap or not self.cap.isOpened():
                break
                
            ret, frame = self.cap.read()
            if not ret or frame is None:
                continue

            frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_AREA)

            if self.frame_queue.full():
                try:
                    self.frame_queue.get_nowait()
                except Empty:
                    pass
            
            try:
                self.frame_queue.put_nowait(frame)
            except Exception:
                pass

    def get_frame(self):
        try:
            return self.frame_queue.get_nowait()
        except Empty:
            return None

    def release(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        logger.info("Camera connection is closed.")

