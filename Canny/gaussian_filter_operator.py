from math import floor

import numpy as np


def gauss_function(x, y, sigma):
    """
    Функция Гауса для 2 измерений
    :param x: координата по оси Ox
    :param y: координата по оси Oy
    :param sigma: среднеквадратическое отклонение нормального распределения
    :return: значение преобразования
    """
    return 1 / (2 * np.pi * sigma ** 2) * (np.e ** (-((x ** 2) * (y ** 2)) / 2 * sigma ** 2))


class GaussianFilterOperator:

    def __init__(self, image: np.ndarray, kernel_size=3, sigma=1.0):
        self.image = image
        self.kernel_size = kernel_size
        self.sigma = sigma
        self.kernel = self.create_kernel()

    def create_kernel(self):
        """
        Функция создания ядра свертки
        :return: Ядро [size x size]
        """
        shift = int(floor(self.kernel_size / 2))
        kernel = np.zeros((self.kernel_size, self.kernel_size))
        for y in range(self.kernel_size):
            for x in range(self.kernel_size):
                kernel[y][x] = gauss_function(x - shift, y - shift, self.sigma)
        # Нормализуем ядро
        kernel /= np.sum(kernel)
        return kernel

    def blur(self):
        """
        Фукнция размытия
        :return: размытую коии
        """
        image_row, image_col = self.image.shape
        output = self.image.copy()
        # добавляем дополнительные границы по размерам ядра, чтобы все правильно считалось
        padding = int((self.kernel_size - 1) / 2)

        padded_image = np.zeros((image_row + (2 * padding), image_col + (2 * padding)))

        padded_image[padding:padded_image.shape[0] - padding, padding:padded_image.shape[1] - padding] = self.image

        for iy in range(image_row):
            for ix in range(image_col):
                output[iy, ix] = np.sum(self.kernel * padded_image[iy:iy + self.kernel_size, ix:ix + self.kernel_size])
        return output
