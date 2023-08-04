def create_box(xy, offset):
    '''
    Given an (x,y) position and an offset,
    Return a box (left, top, right, bottom) centered at (x,y) with sidelength equal to twice the offset
    '''
    x = xy[0]
    y = xy[1]
    box = (x - offset, y - offset, x + offset, y + offset)
    return box

GULLY_COLOR = (215, 25, 28)
NEW_COLOR = (255, 255, 255)
##UNMARKED SATS
from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = 1000000000
def produce_target(directory,images):
    #for file in os.listdir(directory):
    for image in images:
        #image = os.path.join(directory, file)
        with Image.open(image) as im:
            im = im.convert('RGB')
            image_name = image[-9:-6]
            w = im.size[0]
            h = im.size[1]
            for x in range(0, w):
                for y in range(0, h):
                    pixel = im.getpixel((x,y))
                    if pixel == GULLY_COLOR:
                        im.putpixel((x,y), NEW_COLOR)
            print("saving image")
            im.save("images/white_targets/" + image_name + "_target.png")

def tile(path, subimage_size, step_size):
    image_name = path[-7:-4]
    #image_name += "_t"
    with Image.open(path) as im:
        w = im.size[0]
        h = im.size[1]
        offset = subimage_size // 2
        count = 1
        for x in range(offset, w - offset, step_size):
            for y in range(offset, h - offset, step_size):
                box = create_box((x, y), offset)
                subimage = im.crop(box)
                filepath = "D:/USERS/KYLE_KOHMAN/GAN/images/small_step_subs/source/" + image_name

                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                subimage.save(filepath + "/" + image_name + "_" + str(count) + ".png")
                count += 1


import glob
# images = glob.glob("D:/USERS/KYLE_KOHMAN/GAN/images/white_targets/*.png")
# print(len(images))
# # produce_target(images)
#
# for image in images:
#     tile(image, 256, 128)
#
# source = glob.glob("D:/USERS/KYLE_KOHMAN/GAN/images/satellites/*.png")
# print(len(source))
# for image in source:
#     tile(image, 256, 128)
# image = "260_20.png"
# im1 = Image.open("D:/USERS/KYLE_KOHMAN/GAN/images/subimages/targets/262/262_271.png")
# im2 = Image.open("D:/USERS/KYLE_KOHMAN/GAN/images/subimages/source/262/262_271.png")
# combined_image = Image.new("RGB", (512,256))
# combined_image.paste(im2, (0,0))
# combined_image.paste(im1, (256,0))
# combined_image.save("D:/USERS/KYLE_KOHMAN/GAN/images/subimages/
# root = "D:/USERS/KYLE_KOHMAN/GAN/images/subimages"
# base_subs = os.listdir(root)
# for subfolder in base_subs:
#     subfolder_path = os.path.join(root, subfolder)
#     matching = os.listdir(subfolder_path)
#     for matching_sub in matching:
#         matching_subfolder_path = os.path.join(subfolder_path, matching_sub)
#         images = os.listdir(matching_subfolder_path)
#     print(len(images))
#     print(images)
#      #print(matching)
# print(base_subs)
root = "D:/USERS/KYLE_KOHMAN/GAN/images/small_step_subs/"
source = []
target = []
num_sub_folders = 2
base = os.listdir(root)
flag = True
for folder in base:
    path = os.path.join(root, folder)
    subs = os.listdir(path)
    for sub in subs:
        p = os.path.join(path, sub)
        images = os.listdir(p)
        for image in images:
            im_path = os.path.join(p, image)
            if flag is True:
                source.append(im_path)
            else:
                target.append(im_path)
    flag = False
print(len(source))
print(len(target))
# print(source[78])
# print(target[78])
for i in range(len(source)):
    im1 = Image.open(source[i])
    im2 = Image.open(target[i])
    combined_image = Image.new("RGB", (512, 256))
    combined_image.paste(im1, (0, 0))
    combined_image.paste(im2, (256,0))
    combined_image.save("D:/USERS/KYLE_KOHMAN/GAN/images/small_step_combined/image" + "_" + str(i) + ".jpg")

#ir = "images/satellites-remarked"
#produce_target(dir)
# img = "images/satellites/322.png"
# with Image.open(img) as im:
#     im = im.convert("RGB")
#     im.save("D:/USERS/KYLE_KOHMAN/GAN/images/satellites/RGB/662_rgb.png")