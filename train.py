#! /usr/bin/env python

"""
This script takes in a configuration file and produces the best model.
The configuration file is a json file and looks like this:
"""

import cli
import os
import numpy as np
from preprocessing import parse_annotation
from frontend import YOLO

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def main(argstate):
    ###############################
    #   Parse the annotations
    ###############################

    # parse annotations of the training set
    train_imgs, train_labels = parse_annotation(argstate.train.annot_folder,
                                                argstate.train.image_folder,
                                                argstate.labels)

    # parse annotations of the validation set, if any, otherwise split the training set
    if os.path.exists(argstate.v_annot_folder):
        valid_imgs, valid_labels = parse_annotation(argstate.valid.annot_folder,
                                                    argstate.valid.image_folder,
                                                    argstate.labels)
    else:
        train_valid_split = int(0.8*len(train_imgs))
        np.random.shuffle(train_imgs)

        valid_imgs = train_imgs[train_valid_split:]
        train_imgs = train_imgs[:train_valid_split]

    print(train_labels)

    if len(set(argstate.labels).intersection(set(train_labels.keys()))) == 0:
        print("Labels to be detected are not present in the dataset! Please revise the list of labels in the config.json file!")
        return

    ###############################
    #   Construct the model
    ###############################

    yolo = YOLO(architecture=argstate.architecture,
                input_size=argstate.image_size,
                labels=argstate.labels,
                max_box_per_image=argstate.mbpi,
                anchors=argstate.anchors)

    ###############################
    #   Load the pretrained weights (if any)
    ###############################

    if os.path.exists(argstate.pretrained_weights):
        print("Loading pre-trained weights in",
              argstate.pretrained_weights)
        yolo.load_weights(argstate.pretrained_weights)

    ###############################
    #   Start the training process
    ###############################

    yolo.train(train_imgs=train_imgs,
               valid_imgs=valid_imgs,
               train_times=argstate.train_times,
               valid_times=argstate.valid_times,
               nb_epoch=argstate.nb_epoch,
               learning_rate=argstate.learning_rate,
               batch_size=argstate.batch_size,
               warmup_bs=argstate.warmup_bs,
               object_scale=argstate.object_scale,
               no_object_scale=argstate.no_object_scale,
               coord_scale=argstate.coord_scale,
               class_scale=argstate.class_scale,
               saved_weights_name=argstate.saved_weights_name,
               debug=argstate.debug)


if __name__ == '__main__':
    argstate = cli.parse_train()
    main(argstate)
