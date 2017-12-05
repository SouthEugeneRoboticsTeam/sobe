# Customized multithreading helper for SOBE
# Made by Jackson Lewis

import multiprocessing
from time import sleep
from camera import CameraProcessor, is_on
from frontend import YOLO
from utils import draw_boxes
import time
import cv2
import threading

thread_cap = 1 # Maximum amount of threads that we want running at once

locked = False

updated_frame = None

retake = False

def process_image(frame,argstate):
    global updated_frame,retake
    if frame is None:
        return
    print("Processing image")
    yolo = YOLO(architecture=argstate.architecture,
                input_size=argstate.input_size,
                labels=argstate.labels,
                max_box_per_image=argstate.max_box_per_image,
                anchors=argstate.anchors)
    yolo.load_weights(argstate.weights)
    boxes = yolo.predict(frame)
    yolo = None
    accuracylist = sorted(boxes,key=lambda x: x.score,reverse=True)
    if len(accuracylist) == 0:
        retake = True
        print("Could not identify bucket")
        return
    retake = False
    mostaccurate = accuracylist[0]
    height, width = frame.shape[:2]
    x = mostaccurate.x - 0.5
    updated_frame = (x * width)
    image = draw_boxes(frame,[mostaccurate],argstate.labels)
    # temporary, for verification
    print(cv2.imwrite("/home/jacksoncoder/PycharmProjects/Sobe/latest" + str(int(time.time())) + ".jpg",image))

class VideoThreadDispatcher:

    def __init__(self,argstate,timeout):
        self.args = argstate
        self.camlink = CameraProcessor(0)
        self.timeout = timeout
        self.camlink.start_read()

    # Load function to run in thread

    def load(self,func):
        self.tfunc = func

    # function sent to stop thread

    def stop_after(self,time,thread):
        sleep(time)
        thread.terminate()

    def camera_on(self):
        return is_on()

    def need_retake(self):
        return retake

    def dispatch(self):
        global retake
        retake = False
        if len(multiprocessing.active_children()) > thread_cap:
            print("Waiting for threads to finish")
            return
        # Read latest frame
        f = self.camlink.get_latest()
        t = threading.Thread(target=self.tfunc,args=[f,self.args])
        t.start()
        # Start a thread to stop the other one after a certain amount of time
        #stop = multiprocessing.Process(target=self.stop_after,args=[self.timeout,t])
        #stop.start()

def latest_frame():
    return updated_frame