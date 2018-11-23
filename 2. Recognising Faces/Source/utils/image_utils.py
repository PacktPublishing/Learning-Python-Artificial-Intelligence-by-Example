import cv2
import numpy as np
import matplotlib.pyplot as plt


def load_image_as_array(path: str, convert_colour=cv2.COLOR_BGR2RGB, image_size: tuple=(300,300)) -> np.ndarray:
    """Load image from disk into numpy array"""
    img = cv2.cvtColor(cv2.imread(path), convert_colour)
    return cv2.resize(img, image_size)


def show_side_by_side(images: list, cmap: str='gray', figsize: tuple=None, labels: list=[]) -> None:
    """Pass a list of images to display them side by side"""
    fig, axes = plt.subplots(ncols=len(images), nrows=1)

    if figsize:
        fig.set_size_inches(*figsize)

    for i, im in enumerate(images):
        axes[i].imshow(im, cmap=cmap)
        axes[i].set_xticks([])
        axes[i].set_yticks([])

    if len(labels) > 0:
        for i, label in enumerate(labels):
            axes[i].set_title(label)

    plt.tight_layout()


def show_image(image: np.ndarray):
    img = image.squeeze()
    plt.axis("off")
    plt.imshow(img, cmap='gray', interpolation='nearest')  # Manipulation to display image in the correct orientation!
    plt.show()