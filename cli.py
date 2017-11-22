# Parses input from command line arguments
import argparse
import json


class ArgState:  # Anonymous class used by the returned state
    pass


def parse_predict():
    # This factors in command line arguments and config and merges them to
    # produce a single configuration object
    argparser = argparse.ArgumentParser(
        description='Train and validate YOLO_v2 model on any dataset')

    argparser.add_argument(
        '-c',
        '--conf',
        help='path to configuration file')

    argparser.add_argument(
        '-w',
        '--weights',
        help='path to pretrained weights')

    argparser.add_argument(
        '-i',
        '--input',
        help='path to an image or an video (mp4 format)')

    args = argparser.parse_args()
    config_path = args.conf
    with open(config_path) as config_buffer:
        config = json.load(config_buffer)
    print(config)
    argstate = ArgState
    argstate.architecture = config['model']['architecture']
    argstate.input_size = config['model']['input_size']
    argstate.labels = config['model']['labels']
    argstate.max_box_per_image = config['model']['max_box_per_image']
    argstate.anchors = config['model']['anchors']

    argstate.weights = args.weights if args.weights is not None else config[
        'train']['saved_weights_name']
    argstate.input = args.input
    return argstate
