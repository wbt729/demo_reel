from PySide2.QtCore import QUrl, Qt, QSize, QObject, QTimer, Signal, Slot
import cv2
import numpy as np
import threading

class Grabber(QObject):
    image_received = Signal(np.ndarray)

    def __init__(self):
        super(Grabber, self).__init__()
        self.cap = cv2.VideoCapture(0)
        print(self.cap.isOpened())
        if not self.cap.isOpened():
            raise Exception("cap not open")
        else:
            self.thread = threading.Thread(target=self.thread_fct)
            self.thread.start()
        
    def thread_fct(self):
        while self.cap.isOpened():
            success, image = self.cap.read()
            if success:
                self.image_received.emit(image)