
import cv2
import numpy as np 
import time
from os import system
from random import uniform

## logout
## Finds x, clicks x, waits for ~1.5 seconds
## finds logout button, clicks logout button
def logout():
    scrot()
    loc = get_location('x')
    mouse_move(loc)
    click()
    idle(uniform(1,2))
    scrot()
    loc = get_location('b')
    mouse_move(loc)
    click()
    

## click
def click():
    system('xdotool click 1')

## a sleep that doesn't stop process time
def idle(wait_time):
    end_time = time.process_time() + wait_time
    t = 0
    while t < end_time:
        t = time.process_time()
    

## move mouse
## to a random place within 5 pixels of 
## location given as parameter loc
def mouse_move(loc):
    if loc[0] == -1:
        return False
    # randomize coordinares slightly
    x = str(loc[0] + uniform(-5, 5))
    y = str(loc[1] + uniform(-5, 5))
    # click at radomized coordinates
    system('xdotool mousemove ' + x + ' ' + y)
    return True

## take new screenshot
def scrot():
    system('scrot Pictures/sc.png')
    return

## checks to see if absorbtion icon is still on
## the screen
def check_end():
    if get_location('as') == (-1, -1):
        return True
    return False

## Returns array of upper right and lower left
## corners of where this image first occurs on  
## the screen 
def get_location(img):

    # get most recent screenshot
    scrot()
    img_rgb = cv2.imread('Pictures/sc.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    # get Overload data
    if img == 'o':
        template = cv2.imread('Pictures/Overload.png', 0)
        threshold = .95
    # get Absorbtion data
    elif img == 'a':
        template = cv2.imread('Pictures/Absorbtion.png', 0)
        threshold = .95
    # get Pray data
    elif img == 'p':
        template = cv2.imread('Pictures/Pray.png', 0)
        threshold = .95
    # get AbsorbtionStat data
    elif img == 'as':
        template = cv2.imread('Pictures/AbsorbtionStat.png', 0)
        threshold = .95
    # get OverloadStat data
    elif img == 'os':
        template = cv2.imread('Pictures/OverloadStat.png', 0)
        threshold = .95
    # get logout x data
    elif img == 'x':
        template = cv2.imread('Pictures/X.png', 0)
        threshold = .5
    # get logout button data
    elif img == 'b':
        template = cv2.imread('Pictures/LogButton.png', 0)
        threshold = .95
    else:
        print('Wrong get_locations input.')
        return

    # get width and height of template
    w, h = template.shape[::-1]
    # find instances in image
    match = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)


    # get locations of instances
    loc = np.where( match >= threshold)

    # if image was not found, regurn location (-1, -1)
    if len(loc[0]) == 0:
        return (-1, -1)

    # get center location of first occurance
    x = loc[1][0] + w/2
    y = loc[0][0] + h/2

    return (x, y)

