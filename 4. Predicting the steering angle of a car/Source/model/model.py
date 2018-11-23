"""
Create the CNN model in Keras

"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import plot_model
from keras.callbacks import TensorBoard, Callback, ModelCheckpoint, ProgbarLogger
from keras.optimizers import Adam
from datetime import datetime

# Callbacks
tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=32, write_graph=True, write_grads=False,
                          write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None,
                          embeddings_data=None)   #, update_freq='epoch')

checkpoint = ModelCheckpoint(filepath='./logs/weights-{}.hdf5'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')),
                             monitor='val_loss', verbose=1,
                             save_best_only=True, save_weights_only=False,
                             mode='auto', period=1)

progressbar = ProgbarLogger(count_mode='steps', stateful_metrics=None)

# Optimizer and learning rate
lr = 0.0003
adam = Adam(lr=lr)


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


def cnn(input_shape=(66, 200, 3),
        kernel_size=(5, 5),
        padding='same',
        activation='elu',
        loss='mean_squared_error',
        optimizer=adam,
        pool_size=(2, 2),
        dropout=0.5,
        debug=False):

    print('cnn(): Creating CNN with parameters:\n')
    print('image_shape={}\nkernel_size={}\npool_size={}\ndropout={}\nactivation={}\noptimizer={}\nloss={}'
          .format(input_shape, kernel_size, pool_size, dropout, activation, optimizer, loss))

    model = Sequential()

    # First convolutional layer
    model.add(Conv2D(24, kernel_size, padding=padding, input_shape=input_shape))
    model.add(Activation(activation))
    model.add(MaxPooling2D(pool_size=pool_size))

    # 2nd conv layer
    model.add(Conv2D(36, kernel_size, padding=padding))
    model.add(Activation(activation))
    model.add(MaxPooling2D(pool_size=pool_size))
    # model.add(Dropout(dropout))

    # 3rd conv layer
    model.add(Conv2D(48, kernel_size, padding=padding))
    model.add(Activation(activation))
    model.add(MaxPooling2D(pool_size=pool_size))

    # 4th conv layer
    model.add(Conv2D(64, kernel_size, padding=padding))
    model.add(Activation(activation))
    model.add(MaxPooling2D(pool_size=pool_size))
    # model.add(Dropout(dropout))

    model.add(Flatten())

    # 1st Fully Connected Layer
    model.add(Dense(100))
    model.add(Activation(activation))
    model.add(Dropout(dropout))

    # 2nd Fully Connected Layer
    model.add(Dense(50))
    model.add(Activation(activation))
    model.add(Dropout(dropout))

    # Output
    model.add(Dense(1))
    model.add(Activation('linear'))

    model.compile(loss=loss, optimizer=optimizer)

    if debug:
        print(model.summary())
        plot_model(model, to_file='./logs/model.png')

    return model
