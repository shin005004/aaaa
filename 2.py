from picamera import PiCamera
from time import sleep

def show_cam_seconds(cam, sec):
    cam.start_preview()
    sleep(sec)
    cam.stop_preview()

cam = PiCamera()
show_cam_seconds(cam, 5)