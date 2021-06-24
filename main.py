# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import *
from threading import Thread
import cv2
import random


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui")

        self.ui.btn_webcam.clicked.connect(self.webcam)

        self.ui.btn_stickers.clicked.connect(self.stickers)

        self.ui.btn_eye.clicked.connect(self.eye_1)

        self.ui.btn_video.clicked.connect(self.video)

        self.ui.btn_faces.clicked.connect(self.face)

        self.ui.show()

    def face(self):
        thread = Thread(target=self.faces)
        thread.start()

    def faces(self):
        my_webcam = cv2.VideoCapture(0)
        while True:
            validation, frame = my_webcam.read()

            if validation is not True:
                break

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rows, columns = frame_gray.shape

            half_frame = frame_gray[0:rows, 0:columns // 2]
            flip_frame = cv2.flip(half_frame, 1)
            frame_gray[:, columns // 2:] = flip_frame

            cv2.imwrite('faces.jpg', frame_gray)
            self.ui.lbl_show.setPixmap(QPixmap('faces.jpg'))

    def video(self):
        video = QFileDialog.getOpenFileName(self, 'Choose Video')
        self.video_path = video[0]
        self.ui.lbl_show.setPixmap(QPixmap(self.video_path))

    def eye_1(self):
        thread = Thread(target=self.eye)
        thread.start()

    def eye(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

        my_webcam = cv2.VideoCapture(0)
        while True:
            validation, frame = my_webcam.read()

            if validation is not True:
                break

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
            for (x, y, w, h) in faces:
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)

                eye_gray = frame_gray[y:y + h, x:x + w]
                eye_color = frame[y:y + h, x:x + w]
                eyes = eye_cascade.detectMultiScale(eye_gray)
                sticker = cv2.imread('pic/sticker_eyes.png')
                for (ex, ey, ew, eh) in eyes:
                    # cv2.rectangle(eye_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                    resize_sticker = cv2.resize(sticker, (ew, eh))
                    eye_color[ey:ey + eh, ex:ex + ew] = resize_sticker

                smile_gray = frame_gray[y:y + h, x:x + w]
                smile_color = frame[y:y + h, x:x + w]
                smile = smile_cascade.detectMultiScale(smile_gray)
                sticker_flip = cv2.imread('pic/sticker_flip.png')
                for (sx, sy, sw, sh) in smile:
                    # cv2.rectangle(smile_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)
                    resize_sticker_flip = cv2.resize(sticker_flip, (sw, sh))
                    smile_color[sy:sy + sh, sx:sx + sw] = resize_sticker_flip
            cv2.imwrite('eyes.jpg', frame)
            self.ui.lbl_show.setPixmap(QPixmap('eyes.jpg'))

    def stickers(self):
        thread = Thread(target=self.sticker)
        thread.start()

    def sticker(self):
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        my_webcam = cv2.VideoCapture(0)
        while True:
            validation, frame = my_webcam.read()

            if validation is not True:
                break

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(frame_gray, 1.3)
            # stickers = []
            # for i in range(1, 7):
            #     img = cv2.imread(f'pic/stickers/stickers_{i}.png')
            #     stickers.append(img)
            sticker_1 = cv2.imread('pic/stickers/stickers_1.png')
            sticker_2 = cv2.imread('pic/stickers/stickers_2.png')
            sticker_3 = cv2.imread('pic/stickers/stickers_3.png')
            sticker_4 = cv2.imread('pic/stickers/stickers_4.png')
            sticker_5 = cv2.imread('pic/stickers/stickers_5.png')
            sticker_6 = cv2.imread('pic/stickers/stickers_6.png')
            for (x, y, w, h) in faces:
                stickers = random.choice([sticker_1, sticker_2, sticker_3, sticker_4, sticker_5, sticker_6])
                resize_sticker = cv2.resize(stickers, (w, h))
                frame[y:y + h, x:x + w] = resize_sticker
            cv2.imwrite('face_sticker.jpg', frame)
            self.ui.lbl_show.setPixmap(QPixmap('face_sticker.jpg'))

    def webcam(self):
        thread = Thread(target=self.start_webcam)
        thread.start()

    def start_webcam(self):
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        my_webcam = cv2.VideoCapture(0)
        while True:
            validation, frame = my_webcam.read()
            if validation is not True:
                break
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(frame_gray, 1.3)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
                # cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1, 20, None, (x, y), (x + w, y + h), 10)
            cv2.imwrite('face.jpg', frame)
            self.ui.lbl_show.setPixmap(QPixmap('face.jpg'))


if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    sys.exit(app.exec_())
