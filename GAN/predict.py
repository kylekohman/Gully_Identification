from os import listdir

import numpy as np
from numpy import asarray, load
from numpy import vstack
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.models import load_model

from matplotlib import pyplot

def create_box(xy, offset):
    '''
    Given an (x,y) position and an offset,
    Return a box (left, top, right, bottom) centered at (x,y) with sidelength equal to twice the offset
    '''
    x = xy[0]
    y = xy[1]
    box = (x - offset, y - offset, x + offset, y + offset)
    return box
def tile(original_image_path, sub_image_size=256):
    original_image = np.array(Image.open(original_image_path))
    num_rows = original_image.shape[0] // sub_image_size
    num_cols = original_image.shape[1] // sub_image_size

    # Initialize a list to store the sub-images
    sub_images = []

    # Loop through each row and column to extract sub-images
    for row in range(num_rows):
        for col in range(num_cols):
            # Calculate the starting and ending coordinates for the current sub-image
            start_y = row * sub_image_size
            end_y = start_y + sub_image_size
            start_x = col * sub_image_size
            end_x = start_x + sub_image_size

            # Extract the current sub-image using array slicing
            sub_image = original_image[start_y:end_y, start_x:end_x]

            # Add the sub-image to the list
            sub_images.append(sub_image)
    return sub_images

def single_tile(img,x ,y, size=256):
    sub = img.crop((x, y, x+size, y+size))
    return sub


# def tile(path, subimage_size=256, step_size=256):
#     subs = []
#     with Image.open(path) as im:
#         w = im.size[0]
#         h = im.size[1]
#         offset = subimage_size // 2
#         for x in range(offset, w - offset, step_size):
#             for y in range(offset, h - offset, step_size):
#                 box = create_box((x, y), offset)
#                 subimage = im.crop(box)
#                 subs.append(subimage)
#     return subs
# load all images in a directory into memory
def load_images(path, size=(256, 256)):
    # enumerate filenames in directory, assume all are images
    src_list = []
    for filename in listdir(path):
        # load and resize the image
        pixels = load_img(path + filename, target_size=size)
        # convert to numpy array
        pixels = img_to_array(pixels)
        print(pixels.shape)
        # split into satellite and map
        #sat_img, map_img = pixels[:, :256], pixels[:, 256:]
        src_list.append(pixels)
        #tar_list.append(map_img)
    return asarray(src_list)

def preprocess_data(data):
    # load compressed arrays
    # unpack arrays

    # scale from [0,255] to [-1,1]
    data = (data - 127.5) / 127.5

    return data

def plot_images(gen_img):
    # scale from [-1,1] to [0,1]
    scaled_gen_img = (gen_img + 1) / 2.0
    #titles = ['Source', 'Generated', 'Expected']
    #pyplot.subplot(1, 3, 1)
    pyplot.axis('off')
    pyplot.imshow(scaled_gen_img)
    pyplot.show()
    # plot images row by row
    # for i in range(len(images)):
    #     # define subplot
    #     pyplot.subplot(1, 3, 1 + i)
    #     # turn off axis
    #     pyplot.axis('off')
    #     # plot raw pixel data
    #     pyplot.imshow(images[i])
    #     # show title
    #     pyplot.title(titles[i])
    # pyplot.show()


# test_images = load_images("images/test_rgb_subs/")
# gen = load_model("30_epoch_GAN.h5")
# img = preprocess_data(test_images[1])
# img_batch = np.expand_dims(img, axis=0)
# print(img_batch.shape)
# predictions = gen.predict(img_batch)
#
# from PIL import Image
# gen_img = predictions[0]
# predicted_image = (gen_img * 127.5 + 127.5).astype(np.uint8)
# # scaled_gen_img = (gen_img + 1) / 2.0
# # gen_img = np.squeeze(scaled_gen_img, axis=0)
# # gen_img
# image = Image.fromarray(predicted_image)
# image.show()
# #plot_images(gen_img)


from PIL import Image
# def predict(image_path, generator, sub_size=256):
#     subs = tile(image_path)
#     outputs = []
#     for sub in subs:
#         sub = preprocess_data(sub)
#         img_batch = np.expand_dims(sub, axis=0)
#         raw_output = generator.predict(img_batch)
#         output = raw_output[0]
#         output = (output * 127.5 + 127.5).astype(np.uint8)
#         outputs.append(output)
#     with Image.open(image_path) as im:
#         w = im.size[0]
#         h = im.size[1]
#         blank_image = Image.new('RGB', (w, h), color='white')
#     offset = sub_size // 2
#     index = 0
#     for x in range(0, w - sub_size, sub_size):#(offset, w - offset, sub_size):
#        for y in range(0, h- sub_size, sub_size):#(offset, h - offset, sub_size):
#            print(index)
#            img = Image.fromarray(outputs[index])
#            #start_x = x - offset
#            #start_y = y - offset
#            blank_image.paste(img, (x, y))
#            index += 1
#     blank_image.show()

def predict(image_path, generator, size=256):
    image_name = image_path[-11:-6]
    with Image.open(image_path) as img:
        w = img.size[0]
        h = img.size[1]
        blank_image = Image.new('RGB', (w, h), color='white')
        for x in range(0, w - size, size):
            for y in range(0, h - size, size):
                sub = single_tile(img, x, y)
                sub_array = np.asarray(sub)
                img_batch = preprocess_data(sub_array)
                img_batch = np.expand_dims(img_batch, axis=0)
                raw_output = generator.predict(img_batch)
                output = raw_output[0]
                output = (output * 127.5 + 127.5).astype(np.uint8)
                im = Image.fromarray(output)
                blank_image.paste(im, (x, y))
        blank_image.show()
        blank_image.save("D:/USERS/KYLE_KOHMAN/GAN/outputs/full_images/" + image_name + "_mark_25000_images_first_set.png")

gen = load_model("20_epoch_2500_images.h5")
image_path = "images/RGB_satellites/262_rgb.png"
predict(image_path, gen)