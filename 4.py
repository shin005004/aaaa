from picamera import PiCamera 
from time import sleep
from PIL import Image 
import numpy as np

# Capture using PiCamera to save image,
# Load the image & return in PIL Image Class 
def capture_to_load(cam, name):
    cam.capture(name) 
    return Image.open(name)
# Show camera preview for 'sec' seconds 
def show_cam_seconds(cam, sec):
    cam.start_preview() 
    sleep(sec) 
    cam.stop_preview()

# Preview for 'sec' seconds & pause system until stop_key entered 
def preview_wait_key(stop_key, cam, sec):
    while True:
        show_cam_seconds(cam, sec)
        try : is_end = (input()==stop_key) 
        except: continue
        else:
            pass

def main(color_to_detect, v_threshold, r_threshold):
    # instantiate PiCamera Module
    cam = PiCamera()
    # capture & load background image 
    print("***************************************************") 
    print("Clean up view of camera to capture background image")

    print("PRESS 's' + Enter to shoot")

    print("PRESS Enter for 5-more-seconds") 
    preview_wait_key('s', cam, 5)
    bkg_img = capture_to_load(cam, 'bkg_img.jpg') 
    print("Background image captured \n\n")

    # capture & load input image 
    print("***************************************************") 
    print("Stand with your-colored-cloak to capture input image") 
    print("PRESS 's' + Enter to shoot")
    print("PRESS Enter for 5-more-seconds") 
    preview_wait_key('s', cam, 5)
    img = capture_to_load(cam, 'input_img.jpg') 
    print("Input image captured")

    # Color detection
    img_n = np.asarray(img) 
    bkg_img_n = np.asarray(bkg_img)

    colors = {'R': 0, 'G': 1, 'B': 2}
    # what color do you want
    my_color = colors.pop(color_to_detect) # R : 0, G : 1, B : 2
    # masking by pixel value
    mask_v = img_n[:,:,my_color] > v_threshold
    avg_other_colors = np.zeros_like(mask_v, dtype=float) 
    for key in colors.keys():
        avg_other_colors += img_n[:,:,colors[key]] / len(colors.keys())
    # masking by the ratio of color dominance 
    # .5 to avoid divide-by-zero
    mask_r = (img_n[:,:,my_color] / (avg_other_colors+.5)) > r_threshold

    mask = mask_v & mask_r
    # Background Substitution
    img_new = img_n*~mask[...,np.newaxis] + bkg_img_n*mask[...,np.newaxis]
    # Save the output image
    img_new = Image.fromarray(img_new) 
    img_new.save('Cloaked_img.jpg')

# 'R', 'G', 'B' possible 
color_to_detect = 'R' 
v_threshold = 70
r_threshold = 2.5
main(color_to_detect, v_threshold, r_threshold)