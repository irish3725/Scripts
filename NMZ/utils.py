
import cv2
import numpy as np 
import time
from os import system
from random import uniform

S_Ab = 'Absorbtion.png'
S_Ov = 'Overload.png'



## logout
def log():
    print('in logout')
    scrot()
    loc = get_location('x')
    print(loc)
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
    system('scrot sc.png')
    return

def chk_end():
    print('checking end')
    print(get_location('as'))
    if get_location('as') == (-1, -1):
        return True
    return False

## Returns array of upper right and lower left
## corners of where this image first occurs on  
## the screen 
def get_location(img):

    # get most recent screenshot
    scrot()
    img_rgb = cv2.imread('sc.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    # get Overload data
    if img == 'o':
        template = cv2.imread('Overload.png', 0)
        threshold = .95
    # get Absorbtion data
    elif img == 'a':
        template = cv2.imread('Absorbtion.png', 0)
        threshold = .95
    # get Pray data
    elif img == 'p':
        template = cv2.imread('Pray.png', 0)
        threshold = .95
    # get Door data
    elif img == 'd':
        template = cv2.imread('Door.png', 0)
        threshold = .95
    # get Logout data
    elif img == 'l':
        template = cv2.imread('Logout.png', 0)
        threshold = .95
    # get AbsorbtionStat data
    elif img == 'as':
        template = cv2.imread('AbsorbtionStat.png', 0)
        threshold = .95
    # get OverloadStat data
    elif img == 'os':
        template = cv2.imread('OverloadStat.png', 0)
        threshold = .95
    # get OverloadStat data
    elif img == 'x':
        template = cv2.imread('X.png', 0)
        threshold = .5
    # get OverloadStat data
    elif img == 'b':
        template = cv2.imread('LogButton.png', 0)
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

    if len(loc[0]) == 0:
        return (-1, -1)

    #print(loc)

    # get center location of first instance
    x = loc[1][0] + w/2
    y = loc[0][0] + h/2

    return (x, y)

def check_end():
    return False

def logout():
    return

def draw_squares(loc):

    # write Sunday photo to res
    img_rgb = cv2.imread('Sunday.png')
    cv2.imwrite('res.png', img_rgb)

    for img in loc:
        # get res photo
        img_rgb = cv2.imread('res.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        
        # get Overload data
        if img == 'o':
            template = cv2.imread('Overload.png', 0)
        # get Absorbtion data
        elif img == 'a':
            template = cv2.imread('Absorbtion.png', 0)
        # get Pray data
        elif img == 'p':
            template = cv2.imread('Pray.png', 0)
        else:
            return
 

        # get width and height of template
        w, h = template.shape[::-1]
        # find instances in image
        match = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = .95 


        # get locations of instances
        loc = np.where( match >= threshold)


        color = (uniform(0,255), uniform(0,255), uniform(0,255))

        for pt in zip(*loc[::-1]):
            if img == 'o':
                color = (uniform(50,200), 0, 0)
            # get Absorbtion data
            elif img == 'a':
                color = (0, uniform(50,200), 0)
            # get Pray data
            elif img == 'p':
                color = (0, 0, uniform(50,200))
 
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), color, 2)

        cv2.imwrite('res.png', img_rgb)

    return

