
import time
import threading
from random import uniform
from utils import *

class NMZ():

    # initialize variables
    def __init__(self):
        # idle for 5 seconds
        idle(5)
        # constants
        self.scale = 1
        self.absorb_time = 200 * self.scale
        self.overload_time = 300 * self.scale
        self.pray_time = 40 * self.scale
        

        # variables
        self.end = False
        self.start_time = time.process_time()
        self.n_absorb = self.start_time
        self.loc_absorb = get_location('a')
        self.dose_absorb = 4
        self.n_overload = self.start_time
        self.loc_overload = get_location('o')
        self.dose_overload = 4
        self.n_pray = self.start_time
        self.loc_pray = get_location('p')
        
    def absorb(self):
        # if potion at this location has doses left
        if self.dose_absorb > 0:
            # move mouse to and click this potion
            if not mouse_move(self.loc_absorb):
                print('Not Mouse Move!!')
                # if location is (-1,-1) then check to see if end
                if chk_end():
                    # if end, wait 30 seconds, logout and end program
                    idle(uniform(200,300))
                    log()
                    self.end = True
                    return
                # if not end, check again in 30 seconds
                self.n_absorb = time.process_time() + 30 
                return
            click()
            idle(uniform(3,4))
            self.dose_absorb-=1
            # set next absorbtion time
            self.n_absorb = time.process_time() + self.absorb_time + uniform(-7, 7)
        # if no more doses left at this location
        else:
            # find the next potion and set doses to 4
            self.loc_absorb = get_location('a')
            self.dose_absorb = 4
        return

    def overload(self):
        if self.dose_overload > 0:
            # move mouse to and click this potion
            if not mouse_move(self.loc_overload):
                print('Not Mouse Move!!')
                # if location is (-1,-1) then check to see if end
                if chk_end():
                    print('check_end was true')
                    # if end, wait 30 seconds, logout and end program
                    idle(uniform(200,300))
                    print('idle done')
                    log()
                    self.end = True
                    return
                self.n_overload = time.process_time() + 30 
                return
            click()
            idle(uniform(3,4))
            self.dose_overload-=1
            # set next overload time
            self.n_overload = time.process_time() + self.overload_time + uniform(5, 10)
        else:
            # find the next potion and set doses to 4
            self.loc_overload = get_location('o')
            self.dose_overload = 4
        return

    def pray(self):
        # move to and click prayer icon
        if not mouse_move(self.loc_pray):
            return
        click()
        

        # get current time
        t = time.process_time()

        # get time to turn off prayer
        off_time = t + uniform(.2,.4)

        # idle till it is time to turn prayer off
        while t < off_time:
            t = time.process_time()

        click()
        # set next time to flick prayer
        self.n_pray = time.process_time() + self.pray_time + uniform(-10, 10) 
        return
        
    def start(self):
        while not self.end:
            # get current time
            t = time.process_time()

            # check pray
            if t > self.n_pray and not self.end:
                print('pray')
                self.pray()

            # check overload
            if t > self.n_overload and not self.end:
                print('overload')
                self.overload()

            # check absorb
            if t > self.n_absorb and not self.end:
                print('absorb')
                self.absorb()
            
        return

if __name__ == '__main__':
    
    # create new instance of NMZ
    nmz = NMZ()
    nmz.start()

    # create list of threads
    threads = []

    # append all threads
    threads.append(threading.Thread(name='run', target=nmz.start))

    # start all threads
    for thread in threads:
        thread.start()

    # join all threads
    for thread in threads:
        thread.join()

