# Live code for the robot

import cli
import cv2
from time import sleep
from threaddispatch import VideoThreadDispatcher, process_image, latest_frame
import os
from network import net_init, send_to_network

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def main(argstate):


    #
    # Step 1: Connect to camera:
    #
    camera1 = cv2.VideoCapture(0)
    camera2 = cv2.VideoCapture(0)
    assert(camera1.read()[1] is not None or
    camera2.read()[1] is not None)
    camera1.release()
    camera2.release()

    #
    # Step 2: Connect to network
    #

    result = net_init(argstate.ip)

    if not result[0]:
        print(result[1])
        exit(0)

    #
    # Step 3: Start thread dispatching
    #

    td = VideoThreadDispatcher(argstate,argstate.timeout)
    td.load(process_image)
    while not td.camera_on():
        sleep(0.1)
    td.dispatch()

    while latest_frame() is None and not td.need_retake():
        sleep(0.1)
    while td.need_retake():
        print("retaking")
        td.update_frame()
        while latest_frame() is None and not td.need_retake():
            sleep(0.1)
    #
    # Step 4: Attempt to broadcast to the RoboRIO
    #
    data = latest_frame()
    result = send_to_network(data)
    if not result[0]:
        print(result[1])
        td.close_camera()
        exit(0)
    td.close_camera()
    exit(0)

if __name__ == "__main__": # Entry point
    argstate = cli.parse_production()
    main(argstate)
