"""
train.py

Train the CNN
"""

import pandas as pd
import argparse
import cv2
from sklearn.utils import shuffle
from model.model import cnn, LossHistory, tensorboard, checkpoint, progressbar
from data import generators

image_size = (66, 200, 3)   # (78, 227, 3)

# Process command line arguments if supplied
parser = argparse.ArgumentParser(
        description='Train our cnn to predict steering angles')
show_default = ' (default %(default)s)'

parser.add_argument('-debug', dest='debug',
                    default='N',
                    choices=('Y', 'N'),
                    help='Debug (Y)es or (N)o')
parser.add_argument('-batch-size', dest='batch-size',
                    default=128,
                    type=int,
                    help='Batch size (suggest 32 - 128)')
parser.add_argument('-limit-batches', dest='limit-batches',
                    default=0,
                    type=int,
                    help='Limit batches to train on ')
parser.add_argument('-epochs', dest='epochs',
                    default=200,
                    type=int,
                    help='Number of epochs')
parser.add_argument('-data-file', dest='data-file',
                    default='./data/data.txt',
                    help='File containing list of images and steering angles')
parser.add_argument('-log-images', dest='log-images',
                    default='N',
                    choices=('Y', 'N'),
                    help='Log training images to disk (Y)es or (N)o')
args = vars(parser.parse_args())

# Prepare data for training, validation and test
columns = ['image_name', 'angle', 'date', 'time']
df = pd.read_csv(args['data-file'], names=columns, delimiter=' ').sample(frac=1).reset_index(drop=True)

sample_idx = {}
num_samples = len(df)
sample_idx['train'] = [i for i in range(0, num_samples, 2)]
sample_idx['valid'] = [i for i in range(1, num_samples, 4)]
sample_idx['test'] = [i for i in range(3, num_samples, 4)]

# Setup debugging
log_images = True if args['log-images'] == 'Y' else False
debug = True if args['debug'] == 'Y' else False
if debug:
    print('train.py: batch-size={}, limit-batches={}, epochs={}, data-file={}'
          .format(args['batch-size'], args['limit-batches'], args['epochs'], args['data-file']))
    cv2.startWindowThread()

# Set up a generator
train_generator = generators.DataGenerator(df.loc[sample_idx['train']],
                                           data_dir='./data/data',
                                           image_size=image_size,
                                           debug=debug,
                                           log_images=log_images,
                                           batch_size=args['batch-size'],
                                           limit_batches=args['limit-batches'],
                                           label='Train')
valid_generator = generators.DataGenerator(df.loc[sample_idx['valid']],
                                           data_dir='./data/data',
                                           image_size=image_size,
                                           debug=debug,
                                           log_images=log_images,
                                           batch_size=args['batch-size'],
                                           limit_batches=args['limit-batches'],
                                           label='Validate')

# Setup the CNN
history = LossHistory()
cnn = cnn(input_shape=image_size, debug=debug)

# Train CNN
cnn.fit_generator(train_generator, validation_data=valid_generator, epochs=args['epochs'],
                  callbacks=[history, tensorboard, checkpoint, progressbar])
if debug:
    print(history.losses)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
