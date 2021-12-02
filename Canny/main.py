import cv2
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def open_file():
    filename = askopenfilename()
    if filename:
        # just formatting the path from "C:/Dev/images/horses.bmp" to "C:\\Dev\\images\\horses.bmp"
        path_to_file = str(filename).replace('/', r'\\')
    return path_to_file


def save_image(image):
    filename = asksaveasfilename(filetypes=(("BMP files", "*.bmp"),
                                            ("TXT files", "*.txt"),
                                            ("HTML files", "*.html;*.htm"),
                                            ("All files", "*.*")))
    if filename:
        reformated_filename = str(filename).replace('/', r'\\') + ".bmp"
        print(reformated_filename)
        cv2.imwrite(reformated_filename, image)


def gaussian_blur(image, size, sigma):
    image_blur = cv2.GaussianBlur(image, (size, size), sigma)
    return image_blur


def run():
    # path_to_file = open_file()
    image = cv2.imread(r"C:\Dev\Fuzzy\images\src\fonts-3229.jpg", 1)
    scale = 1
    cv2.imshow("original", image)
    image_blur = gaussian_blur(image, 11, 0)

    cv2.imshow("Image after blur", image_blur)
    # save_image(image_blur)

    # Оператор Собеля
    scale = 1
    delta = 0
    ddepth = cv2.CV_16S
    gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)

    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    Sobel = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    cv2.imshow("After Sobel", Sobel)

    # Оператор Робертса
    kernelx = np.array([[-1, 0], [0, 1]], dtype=int)
    kernely = np.array([[0, -1], [1, 0]], dtype=int)
    x = cv2.filter2D(gray, ddepth, kernelx)
    y = cv2.filter2D(gray, ddepth, kernely)

    abs_x = cv2.convertScaleAbs(x)
    abs_y = cv2.convertScaleAbs(y)

    Roberts = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    cv2.imshow("After Roberts", Sobel)

    # Оператор Превитта
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=int)
    x = cv2.filter2D(gray, cv2.CV_16S, kernelx)
    y = cv2.filter2D(gray, cv2.CV_16S, kernely)

    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Prewitt = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    cv2.imshow("After Prewitt", Prewitt)

    th, dst = cv2.threshold(Sobel, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("After thresholding", dst)

    cv2.waitKey(0)


if __name__ == '__main__':
    run()
