#! /usr/bin/env python

import cli
import os
import cv2
import numpy as np
from tqdm import tqdm
from utils import draw_boxes
from frontend import YOLO

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def main(argstate):

    weights_path = argstate.weights
    image_path = argstate.input

    ###############################
    #   Make the model
    ###############################

    yolo = YOLO(architecture=argstate.architecture,
                input_size=argstate.input_size,
                labels=argstate.labels,
                max_box_per_image=argstate.max_box_per_image,
                anchors=argstate.anchors)

    ###############################
    #   Load trained weights
    ###############################

    yolo.load_weights(weights_path)

    ###############################
    #   Predict bounding boxes
    ###############################

    # if it's an image, do detection, save image with bounding boxes to the same folder

    # if it's a folder, do detection, save images with boundins boxes to another folder

    # if result folder is present, save annotations to the result folder

    if image_path[-4:] == '.mp4':
        video_out = image_path[:-4] + '_detected' + image_path[-4:]

        video_reader = cv2.VideoCapture(image_path)

        nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

        video_writer = cv2.VideoWriter(video_out,
                                       cv2.VideoWriter_fourcc(*'MPEG'),
                                       20.0,
                                       (frame_w, frame_h))

        for i in tqdm(range(nb_frames)):
            _, image = video_reader.read()

            boxes = yolo.predict(image)
            image = draw_boxes(image, boxes, argstate.labels)

            video_writer.write(np.uint8(image))

        video_reader.release()
        video_writer.release()
    else:
        image = cv2.imread(image_path)
        boxes = yolo.predict(image)
        image = draw_boxes(image, boxes, argstate.labels)

        print(len(boxes), 'boxes are found')

        cv2.imwrite(image_path[:-4] + '_detected' + image_path[-4:], image)


if __name__ == '__main__':
    argstate = cli.parse_predict()
    main(argstate)
