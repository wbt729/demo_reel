from PySide2.QtCore import QUrl, Qt, QSize, QObject, QTimer, Signal, Slot
import numpy as np
import threading

from src import opencv_import
cv2 = opencv_import.from_path()

class Grabber(QObject):
    image_received = Signal(np.ndarray)

    def __init__(self):
        super(Grabber, self).__init__()
        #self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture('pylonsrc user-set=UserSet1 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
        # self.cap = cv2.VideoCapture('pylonsrc ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
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