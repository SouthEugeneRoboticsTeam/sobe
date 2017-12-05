# Customized multithreading helper for SOBE
# Made by Jackson Lewis

import multiprocessing
from time import sleep
from camera import CameraProcessor
from frontend import YOLO
from utils import draw_boxes
import time
import cv2

thread_cap = 5 # Maximum amount of threads that we want running at once

locked = False


def process_image(frame,argstate):
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
    image = draw_boxes(frame,boxes,argstate.labels)
    # Right now, it just saves images
    cv2.imwrite("/home/jacksoncoder/PycharmProjects/Sobe/latest"+ str(int(time.time())) +  ".jpg", image)

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

    def dispatch(self):

        if len(multiprocessing.active_children()) >= thread_cap:
            print("Waiting for threads to finish")
            return
        # Read latest frame
        f = self.camlink.get_latest()
        t = multiprocessing.Process(target=self.tfunc,args=[f,self.args])
        t.start()
        # Start a thread to stop the other one after a certain amount of time
        #stop = multiprocessing.Process(target=self.stop_after,args=[self.timeout,t])
        #stop.start()