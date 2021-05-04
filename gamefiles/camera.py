import time
import numpy
import cv2

class Camera:
    """
    Class: Camera, made to run on separate thread and can therefore be locked, and give status on readiness of picture.
    """

    halt = False
    picReady = False
    def camera_thread(stop):
        """
        Function; args stop (Bool), the main function of camera; runs until stop is True.
        """
        Camera.halt = False
        Camera.picReady = False
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        while True:
            if (Camera.halt is True) and (Camera.picReady is True):
                time.sleep(0.1)
                continue
            
            successPic,image = cam.read()
            if successPic:
                Camera.picReady = False
                successWrite = cv2.imwrite("bildSRC.jpg", image)
                if successWrite:
                    Camera.picReady = True
            else:
                Camera.picReady = False
                
            if stop() is True:
                break

    def halt_setter(status):
        """
        Function: args status (Bool), sets halt to status.
        """
        Camera.halt = status

    @property
    def picReady():
        """
        Function: picReady getter.
        """
        return Camera.picReady