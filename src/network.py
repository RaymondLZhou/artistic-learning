import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from tensorflow.keras.applications import vgg16
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.applications.imagenet_utils import preprocess_input

from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

nb_closest_images = 5
imgs_path = "../data/images/"

vgg_model = vgg16.VGG16(weights='imagenet')
feat_extractor = Model(inputs=vgg_model.input, outputs=vgg_model.get_layer("fc2").output)
feat_extractor.summary()

image_width = eval(str(vgg_model.layers[0].output.shape[1]))
image_height = eval(str(vgg_model.layers[0].output.shape[2]))

files = [imgs_path + x for x in os.listdir(imgs_path) if "jpg" in x]
files = files[:100]
print("Number of images:", len(files))

importedImages = []

for f in files:
    filename = f
    original = load_img(filename, target_size=(image_width, image_height))
    numpy_image = img_to_array(original)
    image_batch = np.expand_dims(numpy_image, axis=0)
    
    importedImages.append(image_batch)
    
images = np.vstack(importedImages)
processed_imgs = preprocess_input(images.copy())

imgs_features = feat_extractor.predict(processed_imgs)

print("Features successfully extracted!")
print("Number of image features:", imgs_features.shape)
print(imgs_features)