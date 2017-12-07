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

updated_data = None

retake = False

start = True

current_frame = None

def process_image(argstate):
    yolo = YOLO(architecture=argstate.architecture,
                input_size=argstate.input_size,
                labels=argstate.labels,
                max_box_per_image=argstate.max_box_per_image,
                anchors=argstate.anchors)
    yolo.load_weights(argstate.weights)
    finished = False
    while not finished:
        global updated_data,retake, start, current_frame
        print(current_frame)
        if current_frame is None:
            return
        boxes = yolo.predict(current_frame)
        accuracylist = sorted(boxes,key=lambda x: x.score,reverse=True)
        if len(accuracylist) == 0:
            retake = True
            start = False
            while not start:
                sleep(0.1)
            continue
        retake = False
        finished = True
        mostaccurate = accuracylist[0]
        _, width = current_frame.shape[:2]
        x = mostaccurate.x - 0.5
        updated_data = (x * width)
        image = draw_boxes(current_frame,[mostaccurate],argstate.labels)

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
        global retake, current_frame
        retake = False
        if len(multiprocessing.active_children()) > thread_cap:
            return
        # Read latest frame
        current_frame = self.camlink.get_latest()
        print(current_frame)
        t = threading.Thread(target=self.tfunc,args=[self.args])
        t.start()
    def update_frame(self):
        global updated_data, start, retake, current_frame
        retake = False
        current_frame = self.camlink.get_latest()
        start = True

    def close_camera(self):
        self.camlink.close()

def latest_frame():
    return updated_data
