import os

import cv2

from src.camera import CameraStream

def main():
    cam = CameraStream(
        source=os.getenv("CAM_SOURCE", "http://192.168.0.19:8080/video"), 
        width=os.getenv("CAM_WIDTH", 1280),
        height=os.getenv("CAM_HEIGHT", 720),
    )

    if not cam.start():
        return

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                continue

            cv2.imshow("The Machine", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cam.release()

if __name__ == '__main__':
    main()

