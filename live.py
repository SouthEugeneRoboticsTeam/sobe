# Live code for the robot

import cli
import cv2
from frontend import YOLO
from time import sleep
from threaddispatch import VideoThreadDispatcher
from utils import draw_boxes
import time

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


def main(argstate):


    #
    # Step 1: Connect to camera:
    #

    camera = cv2.VideoCapture(0) # First camera registered
    ret, frame = camera.read()
    if ret == False or frame is None:
        print("Could not connect to camera. Check the connection of the LiveCam and try again")
        return
    camera.release()
    #
    # Step 2: Start thread dispatching
    #

    td = VideoThreadDispatcher(argstate,argstate.timeout,30) # Iterates 30 frames each time
    td.load(process_image)

    # Begin main loop

    while 1:
        td.dispatch() # Build a new thread

if __name__ == "__main__": # Entry point
    argstate = cli.parse_production()
    main(argstate)