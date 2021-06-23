import jetraw
import dpcore
import numpy as np
import pathlib
import os

# In this example the pyDpcore module is used to import dpcore functionalities, if it is not
# installed in your python environment this example will not work.
# The goal of this example is to present the usage of Buffer Encoding instead of using TIFF files as
# data containers.

# create a 3D container
image = np.zeros((10, 256, 384))
for page in range(image.shape[0]):
    for row in range(image.shape[1]):
        for column in range(image.shape[2]):
            image[page][row][column] = column*(page+1)

# load the calibration file to be used to dpcore prepare the image
path = pathlib.Path(__file__).parent.absolute()
dpcore.load_parameters(os.path.join(path, "test\\pco_3a2dd3a.dat"))
image = image.astype(np.uint16)

# encode each page using buffers
encoded_pages = []
for page in range(image.shape[0]):
    # prepare image buffer with dpcore
    dpcore.prepare_image(image[page][:][:], "PCO_3A2DD3A")
    # encode buffer
    encoded_pages.append(jetraw.encode(image[page][:][:]))

# decode each page using buffers
decoded_pages = []
for page in range(len(encoded_pages)):
    # decode buffer
    decoded_pages.append(jetraw.decode(encoded_pages[page]))
