import numpy as np
from PIL import Image


def read_img(path):
    return np.array(Image.open(path))


def save_img(img_array, path):
    Image.fromarray(img_array.astype(np.uint8)).save(path)


def crop_image(img, x1, y1, x2, y2):
    result = img.copy()
    # Обрезаем: сначала строки (y), потом столбцы (x)
    return result[y1:y2, x1:x2]


def rectangle(img, x1, y1, x2, y2, pixel):
    result = img.copy()
    pixel = np.array(pixel)

    # Верхняя граница (y1 от x1 до x2)
    result[y1, x1:x2] = pixel

    # Нижняя граница (y2-1 от x1 до x2)
    result[y2 - 1, x1:x2] = pixel

    # Левая граница (от y1 до y2 по x1)
    result[y1:y2, x1] = pixel

    # Правая граница (от y1 до y2 по x2-1)
    result[y1:y2, x2 - 1] = pixel

    return result


def rm_color(img, c):
    result = img.copy()

    if len(result.shape) == 3:
        result[:, :, c] = 0

    return result


def rotate(img):
    result = img.copy()

    if len(result.shape) == 2:
        # Для черно-белых изображений (2D)
        result = np.rot90(result, k=-1)
    else:
        # Для цветных изображений (3D)
        result = np.rot90(result, k=-1, axes=(0, 1))

    return result


def flip(img, mode):
    result = img.copy()

    if mode == "vertical":
        # Отражаем по вертикали (верх-низ)
        result = np.flipud(result)
    elif mode == "horizontal":
        # Отражаем по горизонтали (лево-право)
        result = np.fliplr(result)
    else:
        raise ValueError("mode должен быть 'vertical' или 'horizontal'")

    return result


def make_gray(img, mode):
    result = img.copy()

    if len(result.shape) == 3:  # Если цветное изображение
        # Разделяем каналы
        r = result[:, :, 0].astype(np.float32)
        g = result[:, :, 1].astype(np.float32)
        b = result[:, :, 2].astype(np.float32)

        if mode == "mean":
            # Среднее значение
            gray = (r + g + b) / 3
        elif mode == "max":
            # Максимальное значение
            gray = np.maximum.reduce([r, g, b])
        elif mode == "min":
            # Минимальное значение
            gray = np.minimum.reduce([r, g, b])
        else:
            raise ValueError("mode должен быть 'mean', 'max' или 'min'")

        gray = np.clip(gray, 0, 255).astype(np.uint8)
        result = np.stack([gray, gray, gray], axis=-1)

    return result
