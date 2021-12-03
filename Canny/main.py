import cv2
import numpy as np
import GaussianFilterOperator as gfo
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


# TODO: Возможно переделать эту функцию
def open_file():
    filename = askopenfilename()
    if filename:
        # just formatting the path from "C:/Dev/images/horses.bmp" to "C:\\Dev\\images\\horses.bmp"
        path_to_file = str(filename).replace('/', r'\\')
    return path_to_file


# TODO: Возможно переделать и эту функцию
def save_image(image):
    filename = asksaveasfilename(filetypes=(("BMP files", "*.bmp"),
                                            ("TXT files", "*.txt"),
                                            ("HTML files", "*.html;*.htm"),
                                            ("All files", "*.*")))
    if filename:
        reformated_filename = str(filename).replace('/', r'\\') + ".bmp"
        print(reformated_filename)
        cv2.imwrite(reformated_filename, image)


def run():
    # TODO: Добавить возможность выбора фото из системы
    # path_to_file = open_file()
    image = cv2.imread(r"C:\Dev\Fuzzy\images\src\horses.bmp")
    cv2.imshow("original", image)
    # TODO: Прописать свой алгоритм перевода изображения из RGB в GRAY, а не использовать этот
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)

    # По умолчанию используется kernel_size = 3, sigma = 1.0
    g_filter = gfo.GaussianFilterOperator(gray)
    image_blurred = g_filter.blur()

    cv2.imshow("blurred", image_blurred)
    # TODO: Добавить возможность сохранения фото в систему
    # save_image(image_blur)
    cv2.waitKey(0)


if __name__ == '__main__':
    run()
