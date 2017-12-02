# Customized multithreading helper for SOBE
# Made by Jackson Lewis

import multiprocessing
from time import sleep
import cv2

thread_cap = 10 # Maximum amount of threads that we want running at once

locked = False

class VideoThreadDispatcher:

    def __init__(self,argstate,timeout,fskip):
        self.args = argstate
        self.camlink = cv2.VideoCapture(0)
        self.timeout = timeout
        self.frame_skip = fskip

    # Load function to run in thread

    def load(self,func):
        self.tfunc = func

    # function sent to stop thread

    def stop_after(self,time,thread):
        sleep(time)
        thread.terminate()

    def dispatch(self):

        if len(multiprocessing.active_children()) >= thread_cap*2:
            print("Waiting for threads to finish")
            return
        # Load and skip <self.frame_skip> frames
        for i in range(self.frame_skip):
            self.camlink.grab()
        # Read next frame
        _, f = self.camlink.read()
        t = multiprocessing.Process(target=self.tfunc,args=[f,self.args])
        t.start()
        # Start a thread to stop the other one after a certain amount of time
        stop = multiprocessing.Process(target=self.stop_after,args=[self.timeout,t])
        stop.start()
