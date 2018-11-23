"""
Data generators for loading training, validation and test data sets

"""

import pandas as pd
import numpy as np
import cv2
import os
import scipy.misc
from keras.utils import Sequence


def get_image(image_path, crop_position=100, image_size=(66, 200, 3), debug=False):
    """
    Load an image and return resized image for training and actual image for viewing
    :param image_path: str
    :param crop_position: int
    :param image_size: tuple
    :param debug: string
    :return:
    """
    image = cv2.imread(image_path)
    cropped = image[crop_position:, :]
    resize_to = (int(cropped.shape[1] / 2), int(cropped.shape[0] / 2)) if not image_size \
        else (image_size[1], image_size[0])
    resized = cv2.resize(cropped, resize_to)
    return image, resized


class DataGenerator(Sequence):
    """
    Data Generator to load training, validation and test batches
    """
    def __init__(self, df: pd.DataFrame, data_dir='./data', data_file='./data/data.txt',
                 image_size=(256, 455, 3), batch_size=32, limit_batches=0,
                 label=None, debug=False, log_images=False):
        """
        :param df:
        :param data_dir:
        :param data_file:
        :param batch_size:
        """

        self.data_dir = data_dir
        self.data_file = data_file
        self.batch_size = batch_size
        self.image_size = image_size
        self.channels = 1
        self.label = label
        self.idx = 0
        self.batch_count = 0
        self.debug = debug
        self.log_images = log_images
        self.num_batches = int(np.floor(len(df) / self.batch_size))
        self.limit_batches = limit_batches if limit_batches < self.num_batches and limit_batches else self.num_batches
        self.df = df.reset_index().loc[:self.limit_batches * self.batch_size]
        if debug:
            print('DataGenerator(): num_batches = {}, batch_size = {}, len(df) = {}'
                  .format(self.limit_batches, self.batch_size, len(self.df)))

    def __len__(self):
        """
        Find number of batches per epoch
        """
        return self.limit_batches

    def __getitem__(self, batch_num):
        """
        Generate one batch of data
        :param batch_num:
        :return:
        """
        batch_data = self.df[batch_num * self.batch_size:(batch_num + 1) * self.batch_size]
        X, y = self.__data_generation(batch_data.reset_index())
        return X, y

    def __data_generation(self, batch_data):
        """
        Generates data containing batch_size samples
        :param index: list
        """
        X = np.zeros((self.batch_size, *self.image_size))
        y = np.zeros((self.batch_size), dtype=float)

        for i, sample in batch_data.iterrows():
            # if self.debug:
            #     print('{}: Loading image {}, steering angle {}'.format(i, sample['image_name'], sample['angle']))
            image_path = os.path.join(self.data_dir, sample['image_name'])
            image, resized = get_image(image_path)
            # image = cv2.imread(image_path)    # , cv2.IMREAD_GRAYSCALE)
            # cropped = image[100:, :]
            # resize_to = (int(cropped.shape[1] / 2), int(cropped.shape[0] / 2)) if not self.image_size \
            #     else (self.image_size[1], self.image_size[0])
            # resized = cv2.resize(cropped, resize_to)  # (self.image_size[1], self.image_size[0]))
            X[i] = resized
            y[i] = float(sample['angle']) * scipy.pi / 180   # Force into radians
            if self.log_images:
                text = 'Frame: {} Angle: {}'.format(i, sample['angle'])
                cv2.putText(resized, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
                file = './logs/images/{}-{}-{}'.format(self.label, i, sample['image_name'])
                print('Writing debug image to {}'.format(file))
                cv2.imwrite(file, resized)
        return X, y






