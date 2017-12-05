# Live code for the robot

import cli
import cv2
from time import sleep
from threaddispatch import VideoThreadDispatcher, process_image
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

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

    td = VideoThreadDispatcher(argstate,argstate.timeout)
    td.load(process_image)
    sleep(4)
    # Begin main loop
    while 1:
        td.dispatch() # Build a new thread
        sleep(0.2) # Wait 2/10ths of a second

if __name__ == "__main__": # Entry point
    argstate = cli.parse_production()
    main(argstate)