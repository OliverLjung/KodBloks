import time
import numpy
import cv2

class Camera:
    halt = False
    picReady = False
    def camera_thread(stop):
        Camera.halt = False
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        # cam.set(cv2.CAP_PROP_BRIGHTNESS, 1000)
        cam.set(cv2.CAP_PROP_AUTO_WB , 1)
        cam.set(cv2.CAP_PROP_FOCUS , 255)

        while True:
            if Camera.halt is True:
                time.sleep(0.1)
                continue

            success,image = cam.read()
            Camera.picReady = False
            cv2.imwrite("bildSRC.jpg", image)
            Camera.picReady = True
            if stop() is True:
                break

    def halt_setter(status):
        Camera.halt = status

    @property
    def picReady():
        return Camera.picReady