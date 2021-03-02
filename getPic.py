import time
import cv2


try:
    camera = cv2.VideoCapture(0)
    time.sleep(0.5)  # If you don't wait, the image will be dark
    check, image = camera.read()
    if check:
        cv2.imwrite("bild.jpg", image)
    else:
        raise(Exception)
    camera.release() 
except Exception:
    print("Error in camera")
