import time
import numpy as np
import cv2
from var import Config

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
        cam = cv2.VideoCapture(1)
        if not cam.isOpened():
            # (Failed): Trying to find external camera (for laptop).
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                # (Failed): Trying to find external camera (for stat. computer) or laptop's built in camera.
                Config.stopThreads_setter(True)

        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        Camera.halt = False
        Camera.picReady = False
        
        while cam.isOpened():
            if (Camera.halt is True) and (Camera.picReady is True) :
                time.sleep(0.1)
                continue
            
            Camera.picReady = False
            successPic,image = cam.read()
            if successPic:
                successWrite = cv2.imwrite("bildSRC.jpg", image)
                if successWrite:
                    Camera.picReady = True
            else:
                Camera.picReady = False
                
            if stop() is True:
                break

        removedPic = np.zeros((700,700,3))
        cam.release()
        successWrite1, successWrite2 = False, False
        while (successWrite1, successWrite2) == (False, False):
            if not successWrite1:
                successWrite1 = cv2.imwrite("bildSRC.jpg", removedPic)
            if not successWrite2:
                successWrite2 = cv2.imwrite("bild.jpg", removedPic)

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