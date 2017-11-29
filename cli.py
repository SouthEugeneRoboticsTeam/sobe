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
        '--config',
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

    config_path = args.config
    with open(config_path) as config_buffer:
        config = json.load(config_buffer)

    argstate = ArgState()
    argstate.architecture = config['model']['architecture']
    argstate.input_size = config['model']['input_size']
    argstate.labels = config['model']['labels']
    argstate.max_box_per_image = config['model']['max_box_per_image']
    argstate.anchors = config['model']['anchors']

    if args.weights is not None:
        argstate.weights = args.weights
    else:
        argstate.weights = config['train']['saved_weights_name']

    argstate.input = args.input

    return argstate


def parse_train():
    argparser = argparse.ArgumentParser(
        description='Train and validate YOLO_v2 model on any dataset')

    argparser.add_argument(
        '-c',
        '--config',
        help='path to configuration file')

    args = argparser.parse_args()

    config_path = args.config
    with open(config_path) as config_buffer:
        config = json.loads(config_buffer.read())

    argstate = ArgState()
    argstate.train = ArgState()
    argstate.valid = ArgState()
    argstate.train.annot_folder = config['train']['train_annot_folder']
    argstate.train.image_folder = config['train']['train_image_folder']
    argstate.labels = config['model']['labels']
    argstate.valid.annot_folder = config['valid']['valid_annot_folder']
    argstate.valid.image_folder = config['valid']['valid_image_folder']
    argstate.architecture = config['model']['architecture']
    argstate.input_size = config['model']['input_size']
    argstate.mbpi = config['model']['max_box_per_image']
    argstate.anchors = config['model']['anchors']
    argstate.train.times = config['train']['train_times']
    argstate.valid.times = config['valid']['valid_times']
    argstate.nb_epoch = config['train']['nb_epoch']
    argstate.learning_rate = config['train']['learning_rate']
    argstate.batch_size = config['train']['batch_size']
    argstate.warmup_bs = config['train']['warmup_batches']
    argstate.object_scale = config['train']['object_scale']
    argstate.no_object_scale = config['train']['no_object_scale']
    argstate.coord_scale = config['train']['coord_scale']
    argstate.class_scale = config['train']['class_scale']
    argstate.saved_weights_name = config['train']['saved_weights_name']
    argstate.debug = config['train']['debug']
    argstate.pretrained_weights = config['train']['pretrained_weights']

    return argstate
