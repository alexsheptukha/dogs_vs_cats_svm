import numpy as np
import matplotlib.pyplot as plt
import os
import random
from PIL import Image
import tempfile
import cv2


class ImageLoader:
    def __init__(self, dir_name, img_ext=".jpg"):
        self.dir_name = dir_name
        self.img_ext = img_ext

    def get_one_image(self, labels: dict, new_size=None):
        file_names = [os.path.join(self.dir_name, img) for img in os.listdir(self.dir_name)]
        file_names = [file for file in file_names if os.path.splitext(file)[1] == self.img_ext]
        rand_image = random.choice(file_names)
        real_image_name = rand_image.split("/")[-1]
        label = None
        for class_name in labels:
            if class_name in real_image_name:
                label = labels[class_name]
        if label is None:
            raise Exception("no class specified for %s" % real_image_name)
        if not new_size:
            img_pixels = plt.imread(rand_image)
            return {"data": img_pixels, "target": label}
        with tempfile.TemporaryDirectory() as tmp:
            temp_file = os.path.join(tmp, real_image_name)
            img = Image.open(rand_image)
            img = img.resize(new_size)
            img.save(temp_file)
            img_pixels = plt.imread(temp_file)
            return {"data": img_pixels, "target": label}

    def rgb2gray(self, rgb):
        return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

    def sobel_image(self, im):
        im = np.float32(im) / 255.0
        gx = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=1)
        gy = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=1)
        mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
        return mag





