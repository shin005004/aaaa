from PIL import Image
import numpy as np

from picamera import PiCamera

def capture_to_load(cam, name):
    cam.capture(name)
    return Image.open(name)

cam = PiCamera()
img = capture_to_load(cam, 'test_image.jpg')

img_np = np.asarray(img)
print(img_np[width_min:width_max, height_min:height_max, color])
print(img_np.shape)