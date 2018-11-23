"""
View the results of our trained model

"""

import cv2
import pandas as pd
import numpy as np
import os
import argparse
import scipy.misc
from model.model import cnn
from data.generators import get_image

image_size = (66, 200, 3)

# Process command line arguments if supplied
parser = argparse.ArgumentParser(
        description='Run our model to view predicted steering angles')
show_default = ' (default %(default)s)'

parser.add_argument('-data-file', dest='data-file',
                    default='./data/data.txt',
                    help='File containing list of images and steering angles')

parser.add_argument('-model-file', dest='model-file',
                    default='./logs/weights-2018-11-02-11-00-18.hdf5',
                    help='File containing saved weights')

parser.add_argument('-data-dir', dest='data-dir',
                    default='./data/data',
                    help='Directory containing images')

args = vars(parser.parse_args())

model = cnn(input_shape=image_size)
model.load_weights(args['model-file'])

columns = ['image_name', 'angle', 'date', 'time']
df = pd.read_csv(args['data-file'], names=columns, delimiter=' ')

steering_wheel_img = cv2.imread('./data/steering_wheel_image.png')
steering_wheel_w, steering_wheel_h, _ = steering_wheel_img.shape

smoothed_angle = 0
cv2.startWindowThread()

for i, sample in df.iterrows():
    # Load the image
    image_path = os.path.join(args['data-dir'], sample['image_name'])
    image, resized = get_image(image_path, image_size=image_size)

    # Get predicted steering angle from this frame
    angle = model.predict(resized.reshape(1, *resized.shape))[0][0] / scipy.pi * 180
    actual = sample['angle']
    delta = angle - actual

    # Make smooth angle transitions by turning the steering wheel based on the difference of the current angle
    # and the predicted angle
    if angle:
        smoothed_angle += 0.2 * pow(abs((angle - smoothed_angle)), 2.0 / 3.0) * (angle - smoothed_angle) \
                          / abs(angle - smoothed_angle)
    M = cv2.getRotationMatrix2D((steering_wheel_h/2,steering_wheel_w/2),-smoothed_angle,1)
    dst = cv2.warpAffine(steering_wheel_img,M,(steering_wheel_h,steering_wheel_w))

    # Create single image to display - road on the left, rotated steering wheel on the right
    display_img = np.zeros((image.shape[0], image.shape[1] + steering_wheel_w + 1, 3), dtype=np.uint8)
    display_img[0:image.shape[0], 0:image.shape[1], 0:3] = image
    display_img[0:dst.shape[0], (image.shape[1] + 1):(image.shape[1] + dst.shape[1] + 1), 0:3] = dst
    cv2.putText(display_img, 'Predicted angle = {0:.2f}'.format(angle), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(display_img, 'Actual angle = {0:.2f}'.format(actual), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(display_img, 'Delta (predicted - actual) = {0:.2f}'.format(delta), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)

    # Write the image to the output directory so we can create a video of this later
    cv2.imwrite(os.path.join('./output', '{0:05d}.jpg'.format(i)), display_img)

    # Display the image
    cv2.imshow("Steering Demo", display_img)
    k = cv2.waitKey(1)

cv2.destroyAllWindows()
cv2.waitKey(1)



