import sys
from PySide2.QtCore import QUrl, Qt, QSize, QObject, QTimer, Signal, Slot
from PySide2.QtGui import QGuiApplication, QImage, QColor, QPixmap
from PySide2.QtQuick import QQuickImageProvider
from PySide2.QtQml import QQmlApplicationEngine
import resources
import cv2
from ultralytics import YOLO
import supervision as sv

#from src import opencv_import
#cv2 = opencv_import.from_path()

import mediapipe as mp
import threading
import numpy as np
from src import grabber
from src import image_provider
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
screw_model = YOLO("screw_nuts.pt")

box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )


class ImageProcessing(QObject):
    def __init__(self):
        super().__init__()
        self.input_img = None
        self.output_img = None
        self.hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        # self._thread = threading.Thread(target=self.detect_hands)
        self._thread = None
        self._run = False

        self.start_processing_thread(self.detect_hands)

    def start_processing_thread(self, target_fct):
        if self._thread is not None:
            print("thread exists, not starting a new thread")
        else:
            self._run = True
            self._thread = threading.Thread(target=target_fct)
            self._thread.start()

    def stop_processing_thread(self):
        if self._thread is None:
            return
        else:
            self._run = False
            self._thread.join()
            self._thread = None


    def detect_hands(self):
        print("start detect hands")
        while self._run:
            if self.input_img is not None:
                image = self.input_img
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = self.hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                self.output_img = image
                self.input_img = None
        print("run not set, exit thread")

    def detect_pose(self):
        print("start detect pose")
        while self._run:
            if self.input_img is not None:
                image = self.input_img
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = self.pose.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                self.output_img = image
                self.input_img = None
        print("run not set, exit thread")

    def detect_screws(self):
        print("start detect screws")
        while self._run:
            if self.input_img is not None:
                image = self.input_img
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                result = screw_model(image, agnostic_nms=True)[0]
                detections = sv.Detections.from_yolov8(result)
                # labels = [
                #     f"{screw_model.model.names[class_id]} {confidence:0.2f}"
                #     for _, confidence, class_id, _
                #     in detections
                # ]
                self.output_img = box_annotator.annotate(
                    scene=self.input_img, 
                    detections=detections
                )
                self.input_img = None

    @Slot()
    def start_pose(self):
        print("start pose")
        self.stop_processing_thread()
        self.start_processing_thread(self.detect_pose)

    @Slot()
    def start_hands(self):
        print("start hands")
        self.stop_processing_thread()
        self.start_processing_thread(self.detect_hands)

    @Slot()
    def start_screws(self):
        print("start hands")
        self.stop_processing_thread()
        self.start_processing_thread(self.detect_screws)



    @Slot(np.ndarray)
    def set_image(self, img):
        if self.input_img is None:
            self.input_img = img

# Main application
sys.argv += ['--style', 'material']
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
img_proc = ImageProcessing()
grabber = grabber.Grabber()

grabber.image_received.connect(img_proc.set_image)

# Register the image provider with the engine
provider = image_provider.CustomImageProvider(img_proc)
engine.addImageProvider("customImageProvider", provider)
engine.rootContext().setContextProperty("imgproc", img_proc)

# Load the QML file
engine.load("./qml/main.qml")
engine.quit.connect(QGuiApplication.quit)  

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec_())