import cv2

cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cam.set(6 ,cv2.VideoWriter_fourcc('M', 'J', 'E', 'G') )
cam.set(cv2.CAP_PROP_BUFFERSIZE, 3)

while True:
    success, image = cam.read()
    cv2.imshow("Try2Catch", image)

    if cv2.waitKey(20) &  0xFF == ord("q"):
        raise SystemExit

