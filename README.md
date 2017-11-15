<p align="center">
  <img alt="SOBE" title="SOBE" src="/images/logo.png" width="150">
</p>
<h1 align="center">SOBE</h1>
<p align="center">
  SERT's Own Bucket Extractor
</p>

## What?

SOBE is a neural network based off of the YOLO model to detect the locations of
buckets within an image. It was originally used in the 2017 Bunnybots
competition.

## Dataset

The dataset used to train SOBE is available in the
[SouthEugeneRoboticsTeam/bucket-dataset](https://github.com/SouthEugeneRoboticsTeam/bucket-dataset)
repository. Feel free to contribute more images and labels!

## Usage

### Training

To train the network, first configure the `config.json` file for your dataset,
then run the following command:

```bash
$ python train.py -c config.json
```

### Testing

To test the trained weights on a specific image, use the following command:

```bash
$ python predict.py -c config.json /path/to/image.jpg
```

This command will use the saved weights generated in training. If you'd like to
use different weights, set them in the `config.json`'s `saved_weights_name`
parameter.
