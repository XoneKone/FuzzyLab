import os

import cv2
import numpy as np
import gaussian_filter_operator as gfo
import handmade_canny as hc
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
    image = cv2.imread(r"C:\Dev\Git\FuzzyLab\images\src\horses.bmp ")

    handmade_canny = hc.HandmadeCanny(image, 10, 50)
    for title, image in handmade_canny.images.items():
        cv2.imshow(title, image)

    # TODO: Добавить возможность сохранения фото в систему
    # save_image(image_blur)
    cv2.waitKey(0)


path = r'numbers'


def extract_and_label_images(path_to_images: str) -> list[(str, list[float])]:
    files_list = []
    posibilities = []

    for root, dirs, files in os.walk(path_to_images):
        for file in files:
            if file.startswith('seven'):
                posibilities = [np.random.random()]
            elif file.startswith('two'):
                posibilities = [np.random.random()]
            elif file.startswith('zet'):
                posibilities = [np.random.random()]
            files_list.append((file, posibilities))
    # todo: Изменить заполнение массива с вероятностями для каждого изображения
    return files_list


def run_5():
    image = cv2.imread(r"numbers\seven_2.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 3 * 3 фильтр Гаусса ядра
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.Canny(gray, 100, 300)

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    cv2.imshow("orig", image)
    cv2.imshow("thresh", thresh)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0, 0, 255), 1, cv2.LINE_AA, hierarchy, 1)
    cv2.imshow("contours", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    p = extract_and_label_images(path)
    print(len(p))
