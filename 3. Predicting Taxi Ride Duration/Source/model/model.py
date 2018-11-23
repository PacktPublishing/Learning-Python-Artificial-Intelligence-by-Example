"""
Create the NN model in Keras
"""

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import plot_model
from keras.callbacks import TensorBoard, Callback, ModelCheckpoint, ProgbarLogger
from keras.optimizers import Adam
from datetime import datetime

# Callbacks
tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=128, write_graph=True, write_grads=False,
                          write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None,
                          embeddings_data=None)   #, update_freq='epoch')

checkpoint = ModelCheckpoint(filepath='./logs/weights-{}.hdf5'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')),
                             monitor='val_loss', verbose=1,
                             save_best_only=True, save_weights_only=False,
                             mode='auto', period=1)

progressbar = ProgbarLogger(count_mode='steps', stateful_metrics=None)

# Optimizer and learning rate
lr = 0.001
adam = Adam(lr=lr)


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


# Input = [
#           1, 2: 'PULocationLat', 'PULocationLong',
#           3, 4: 'DOLocationLat', 'DOLocationLong',
#           Not using distance...  'TripDistance',
#           5: 'PUDate',
#           6 - 12: 'PUDayOfWeek' (one-hot encoding),
#           13, 14: 'PUHour', 'PUMinute',
#           15: 'Precipitation'
#         ]
#
# Could also add in:
#         [
#           'Temperature', 'WindSpeed', 'SnowDepth', 'Snow'
#         ]
# Output = [
#           'Duration' | 'Price excl tip'
#          ]
def nn(input_shape=68, output_shape=1,
       activation='elu', loss='mean_squared_error',
       optimizer=adam, dropout=0.25, debug=False, label=None):

    print('nn(): Creating NN with parameters:\n')
    print('image_shape={}\noutput_shape={}\ndropout={}\nactivation={}\noptimizer={}\nloss={}'
          .format(input_shape, output_shape, dropout, activation, optimizer, loss))

    model = Sequential()

    # 1st Fully Connected Layer
    model.add(Dense(8192, input_dim=input_shape))
    model.add(Activation(activation))
    # model.add(Dropout(dropout))

    # 2nd Fully Connected Layer
    model.add(Dense(1024))
    model.add(Activation(activation))
    # model.add(Dropout(dropout))

    # # 3rd Fully Connected Layer
    # model.add(Dense(128))
    # model.add(Activation(activation))
    # model.add(Dropout(dropout))

    # Output
    model.add(Dense(1))
    model.add(Activation('linear'))

    model.compile(loss=loss, optimizer=optimizer)

    if debug:
        print(model.summary())
        model_filename = './logs/model_{}.png'.format(label) if label else './logs/model.png'
        plot_model(model, to_file=model_filename)

    return model