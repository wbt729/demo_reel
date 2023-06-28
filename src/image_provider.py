import sys
from PySide2.QtCore import QUrl, Qt, QSize, QObject, QTimer, Signal, Slot
from PySide2.QtGui import QGuiApplication, QImage, QColor, QPixmap
from PySide2.QtQuick import QQuickImageProvider
from PySide2.QtQml import QQmlApplicationEngine
import resources
#import cv2
import mediapipe as mp
import threading
import numpy as np

# Custom Image Provider
class CustomImageProvider(QQuickImageProvider):
    def __init__(self, img_proc):
        super().__init__(QQuickImageProvider.Image)
        self._img_proc = img_proc

    def requestImage(self, id, size, requestedSize):
        img = self._img_proc.output_img
        if img is not None:
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            return qImg
        else:
            return QImage()