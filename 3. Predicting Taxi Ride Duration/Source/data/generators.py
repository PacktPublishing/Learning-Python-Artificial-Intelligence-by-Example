"""
Data generators for loading training, validation and test data sets
"""

import numpy as np
from keras.utils import Sequence, to_categorical
from datetime import datetime


class DataGenerator(Sequence):
    """
    Data Generator to load training, validation and test batches
    """
    def __init__(self, trip_data, weather_data, taxizone_data, zone_ids,
                 generator_type='duration',
                 num_features=68, batch_size=128, limit_batches=0,
                 label=None, debug=False):
        """
        :param df:
        :param data_dir:
        :param data_file:
        :param batch_size:
        """
        self.num_features = num_features
        self.num_outputs = 1
        self.batch_size = batch_size
        self.label = label
        self.idx = 0
        self.batch_count = 0
        self.debug = debug
        self.num_batches = int(np.floor(len(trip_data) / self.batch_size))
        self.limit_batches = limit_batches if limit_batches < self.num_batches and limit_batches else self.num_batches
        self.trip_data = trip_data   # tripdata.reset_index().loc[:self.limit_batches * self.batch_size]
        self.weather_data = weather_data
        self.taxizone_data = taxizone_data
        self.generator_type=generator_type
        self.zone_ids = zone_ids
        if debug:
            print('DataGenerator(): generator_type={}, num_batches = {}, batch_size = {}, len(tripdata) = {}'
                  .format(self.generator_type, self.limit_batches, self.batch_size, len(self.trip_data)))

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
        batch_data = self.trip_data[batch_num * self.batch_size:(batch_num + 1) * self.batch_size]
        X, y = self.__data_generation(batch_data.reset_index())
        return X, y

    def __data_generation(self, batch_data):
        """
        Generates data containing batch_size samples
        Input = [
                  'PULocationLat',
                  'PULocationLong',
                  'DOLocationLat',
                  'DOLocationLong',
                  'Euclidean distance',
                  'Precipitation',
                  'PUDayOfWeek' (one-hot encoding),
                  'PUMonthDate'  (one-hot encoding),
                  'PUHour'  (one-hot encoding)
                ]
        Output = [
                  'Duration' '
                 ]
        :param index: list
        """
        X = np.zeros((self.batch_size, self.num_features), dtype=float)
        y = np.zeros((self.batch_size, self.num_outputs), dtype=float)

        for i, sample in batch_data.iterrows():
            # Get lat/long of pickup and dropoff locations
            PULocation = self.taxizone_data.loc[sample['PULocationID']].centroids
            PULocationLong, PULocationLat = PULocation.x, PULocation.y
            DOLocation = self.taxizone_data.loc[sample['DOLocationID']].centroids
            DOLocationLong, DOLocationLat = DOLocation.x, DOLocation.y

            # Get month date, day of week and hours/mins for pickup
            PUDateTime = datetime.strptime(sample.tpep_pickup_datetime, '%Y-%m-%d %H:%M:%S')
            PUDate = PUDateTime.strftime('%Y-%m-%d')
            PUYear, PUMonth, PUMonthDate = PUDate.split('-')
            # TODO - Add this to pre-processing of trip data! Some random months in the data!!
            if PUYear != '2018' or PUMonth != '06':
                continue
            PUDayOfWeek = PUDateTime.weekday()
            PUTimeHour, PUTimeMinute = datetime.strptime(
                sample.tpep_pickup_datetime, '%Y-%m-%d %H:%M:%S'
            ).strftime('%H:%M').split(':')

            # Get precipitation for that day
            Precipitation = self.weather_data[self.weather_data['DATE'] == PUDate]['PRCP'].values[0]

            X[i] = np.concatenate((np.array([

                PULocationLat,
                PULocationLong,
                DOLocationLat,
                DOLocationLong,
                abs((PULocationLat - DOLocationLat) ** 2 + abs(PULocationLong - DOLocationLong) ** 2) ** 0.5,
                Precipitation
            ]),
                to_categorical(PUDayOfWeek, 7),
                to_categorical(PUMonthDate, 31),
                to_categorical(PUTimeHour, 24)
            ))

            y[i] = [sample['duration']] if self.generator_type == 'duration' \
                else [sample['total_amount'] - sample['tip_amount']]

        return X, y

