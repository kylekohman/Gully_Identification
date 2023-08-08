from __future__ import division

from PIL import Image
import numpy as np


def evaluate(source, image, radius):
    with Image.open(source) as source, Image.open(image) as image:
        s = source.convert('RGB')
        im = image.convert('RGB')
        source_array = np.array(s)
        second_array = np.array(im)

        white_pixel_coords = np.argwhere(np.all(source_array == [255, 255, 255], axis=-1))

        counter = 0
        for center_y, center_x in white_pixel_coords:

            found_white_pixel = False

            min_x = max(center_x - radius, 0)
            max_x = min(center_x + radius + 1, second_array.shape[1])
            min_y = max(center_y - radius, 0)
            max_y = min(center_y + radius + 1, second_array.shape[0])

            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2 and np.all(second_array[y, x] == [255, 255, 255]):
                        found_white_pixel = True
                        break
                if found_white_pixel:
                    break
            if found_white_pixel:
                counter += 1

        print("counter: " + str(counter))
        print("total: " + str(len(white_pixel_coords)))
        print((counter / len(white_pixel_coords)) * 100)


source = "images/white_targets/262_target.png"
image = "outputs/full_images/mix_image_mark_20.png"
evaluate(source, image, 5)