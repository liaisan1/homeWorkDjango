import numpy as np

from task import (
    crop_image,
    flip,
    make_gray,
    read_img,
    rectangle,
    rm_color,
    rotate,
    save_img,
)

np_image = read_img("cat.jpg")

# Тест crop_image
cropped_img = crop_image(img=np_image, x1=100, x2=200, y1=200, y2=300)

save_img(cropped_img, "results/cropped.jpg")

# Тест rectangle
rectangle_img = rectangle(
    img=np_image, x1=100, x2=200, y1=200, y2=300, pixel=np.array([255, 0, 0])
)

save_img(rectangle_img, "results/rectangle.jpg")

# Тест rm_color
colors = zip(range(3), ["red", "green", "blue"])
for c, label in colors:
    rm_color_img = rm_color(img=np_image, c=c)

    save_img(rm_color_img, f"results/rm_{label}.jpg")

# Тест rotate
rotate_img = rotate(
    img=np_image,
)

save_img(rotate_img, "results/rotate.jpg")

# Тест flip
flip_modes = ["vertical", "horizontal"]
for flip_mode in flip_modes:
    flip_img = flip(img=np_image, mode=flip_mode)

    save_img(flip_img, f"results/filp_{flip_mode}.jpg")

# Тест make_gray
gray_modes = ["mean", "max", "min"]
for gray_mode in gray_modes:
    gray_img = make_gray(img=np_image, mode=gray_mode)

    save_img(gray_img, f"results/gray_{gray_mode}.jpg")
