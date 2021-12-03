from math import cos, sin
from gaussian_filter_operator import GaussianFilterOperator
import numpy as np
from numpy import sign


# TODO сюда добавить конвертацию в серый
class HandmadeCanny:
    def __init__(self, image: np.ndarray, low, high):
        self.kernel_size = 3
        self.kernel_x = np.array([[-1, 0, 1],
                                  [-2, 0, 2],
                                  [-1, 0, 1]])

        self.kernel_y = np.array([[-1, -2, -1],
                                  [0, 0, 0],
                                  [1, 2, 1]])

        self.images = {'Gray': image}
        # По умолчанию используется kernel_size = 3, sigma = 1.0
        self.image = GaussianFilterOperator(image).blur()
        self.images['Blurred'] = self.image

        self.gradient, self.theta = self.operator_sobel()
        self.non_m_grad = self.non_maximum_suppression()
        self.thresh = self.double_thresholding(low, high)

    def operator_sobel(self):
        image_row, image_col = self.image.shape

        output_x = self.image.copy().astype(np.float)
        output_y = self.image.copy().astype(np.float)
        # добавляем дополнительные границы по размерам ядра, чтобы все правильно считалось
        padding = int((self.kernel_size - 1) / 2)

        padded_image = np.zeros((image_row + (2 * padding), image_col + (2 * padding)))

        padded_image[padding:padded_image.shape[0] - padding, padding:padded_image.shape[1] - padding] = self.image

        for iy in range(image_row):
            for ix in range(image_col):
                output_x[iy, ix] = np.sum(self.kernel_x *
                                          padded_image[iy:iy + self.kernel_size, ix:ix + self.kernel_size])
                output_y[iy, ix] = np.sum(self.kernel_y *
                                          padded_image[iy:iy + self.kernel_size, ix:ix + self.kernel_size])

        gradient = np.sqrt(np.square(output_x) + np.square(output_y))
        gradient *= 255.0 / gradient.max()

        theta = np.round(np.arctan2(output_x, output_y) / np.pi / 4) * np.pi / 4 - np.pi / 2
        self.images['Sobel operator'] = gradient.astype(np.uint8)
        return gradient, theta

    def is_correct_index(self, x, y):
        if x < 0 or x > self.gradient.shape[1] - 1 or y < 0 or y > self.gradient.shape[0] - 1:
            return False
        return True

    def check(self, x, y, v):
        if not self.is_correct_index(x, y):
            return False
        else:
            if self.gradient[y][x] <= v:
                return True
        return False

    def non_maximum_suppression(self):
        ang_matrix = self.theta.copy().astype(np.float)
        output = self.gradient.copy().astype(np.float)

        for y in range(self.gradient.shape[0]):
            for x in range(self.gradient.shape[1]):
                dx = int(sign(cos(ang_matrix[y][x])))
                dy = int(-sign(sin(ang_matrix[y][x])))
                if self.check(x + dx, y + dy, self.gradient[y][x]):
                    output[y + dy][x + dx] = 0
                if self.check(x - dx, y - dy, self.gradient[y][x]):
                    output[y - dy][x - dx] = 0
        self.images['NonMaximum Suppression'] = output.astype(np.uint8)
        return output

    def double_thresholding(self, low, high):
        down = low * 255 / 100
        up = high * 255 / 100
        output = self.non_m_grad.copy().astype(np.float)
        output[output >= up] = 255
        output[output <= down] = 0
        output[np.logical_and(output < up, output > down)] = 127
        self.images['Double thresholding'] = output.astype(np.uint8)
        return output
