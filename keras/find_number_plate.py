import sys

import cv2
import imutils
from keras.models import load_model
import numpy as np
from tensorflow import keras

cascade = cv2.CascadeClassifier("haarcascade_rus_plate.xml")

num_classes = 10
input_shape = (28, 28, 1)
model = load_model('model_number')

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])


def extract_num(path):
    video = cv2.VideoCapture(path)
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
    ret, frame = video.read()
    if not ret:
        print('Cannot read video file')
        sys.exit()

    while video.isOpened():
        ret, frame = video.read()
        frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        nplate = cascade.detectMultiScale(gray, 1.1, 5)
        letters = []
        for (x, y, w, h) in nplate:
            a, b = (int(0.01 * frame.shape[0]), int(0.015 * frame.shape[1]))
            plate = frame[y + a:y + h - a, x + b: x + w - b, :]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            kernel = np.ones((1, 1), np.uint8)
            # преобравзоние в серый
            plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

            plate = cv2.GaussianBlur(plate, (11, 11), 0)

            ret, tresh = cv2.threshold(plate, 128, 255, cv2.THRESH_BINARY)

            plate_erode = cv2.erode(tresh, kernel, iterations=1)

            plate_dilate = cv2.dilate(plate_erode, kernel, iterations=1)

            contours_cropped, hierarchy = cv2.findContours(plate_dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            for idx, countour in enumerate(contours_cropped):
                (x1, y1, w1, h1) = cv2.boundingRect(countour)
                if (hierarchy[0][idx][3] == 0) and (1200 > cv2.contourArea(countour) > 100):
                    letter_crop = plate[y1:y1 + h1, x1:x1 + w1]
                    _, crop_tresh = cv2.threshold(letter_crop, 128, 255, cv2.THRESH_BINARY)
                    letters.append((x1, w1, cv2.resize(crop_tresh, (28, 28), interpolation=cv2.INTER_AREA)))
                    cv2.rectangle(plate, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 1)
                cv2.imshow('plate', plate)
            letters.sort(key=lambda x2: x2[0], reverse=False)
        cv2.imshow('frame', frame)
        result = [let[2] for let in letters]

        # Запись цифр в строку
        if result:
            number = ""
            for i in result:
                number += str(np.argmax(model.predict(np.expand_dims(i, axis=0))))

            print("Номер: " + number)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    video.release()
    cv2.destroyAllWindows()


# Переделать для видео
if __name__ == '__main__':
    extract_num("videoCars3.mp4")
