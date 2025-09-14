from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
import cv2
from camera import check_camera, get_camFrameData
from landmarks import get_landmarks
from eyeboxes import drawBoxes
from ear_detector import calculateEAR, isDrowsy
from awakestats import save_driver_name

# Camera thread
class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.camera = check_camera()  # existing function
        self.awake = 0
        self.asleep = 0

    def run(self):
        while self._run_flag:
            arrFrames = get_camFrameData(self.camera)
            if arrFrames is not None:
                landmarks = get_landmarks(arrFrames)
                if landmarks == None:
                    continue
                avgEAR = calculateEAR(landmarks[0], landmarks[1])
                eyesClosed = isDrowsy(avgEAR, 5)
                if eyesClosed:
                    arrFrames = drawBoxes(arrFrames, landmarks, eyesClosed)
                    self.asleep += 1
                else:
                    arrFrames = drawBoxes(arrFrames, landmarks, eyesClosed)
                    self.awake += 1

                # Convert frame to QImage
                rgb_image = cv2.cvtColor(arrFrames, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.change_pixmap_signal.emit(qt_image)
            else:
                print("Error: Can't read frame")
                break
        save_driver_name("Default user",self.asleep, self.awake,"driver.txt")

    def stop(self):
        self._run_flag = False
        self.camera.release()
        # self.wait()

# Main GUI function
def run_camera_gui():
    app = QApplication([])

    # Main window
    window = QWidget()
    window.setWindowTitle("Drowsiness Detection")
    window.setGeometry(100, 100, 1280, 720)

    # Layout
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)

    # Camera feed label
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("background-color: none;")  # remove black background
    layout.addWidget(label)
    window.setLayout(layout)

    # End Session button overlaid on bottom-left
    btn = QPushButton("End Session", label)
    btn.setStyleSheet("background-color: rgba(255,0,0,150); color: white; font-size: 18px;")
    btn.setFixedSize(150, 50)

    # Function to position button bottom-left
    def update_button_position():
        btn.move(20, label.height() - btn.height() - 20)

    # Connect resize event of label to reposition button
    old_resize_event = label.resizeEvent
    def new_resize_event(event):
        update_button_position()
        if old_resize_event:
            old_resize_event(event)
    label.resizeEvent = new_resize_event

    # Initial positioning
    update_button_position()

    # Start camera thread
    cam_thread = CameraThread()
    cam_thread.change_pixmap_signal.connect(
        lambda img: label.setPixmap(QPixmap.fromImage(img).scaled(
            label.width(), label.height(), Qt.AspectRatioMode.IgnoreAspectRatio
        ))
    )

    # Stop camera and close GUI when button clicked
    def handle_end_session():
        btn.setEnabled(False)  # prevent double clicks
        cam_thread.finished.connect(app.quit)  # quit AFTER thread ends
        cam_thread.stop()      # set _run_flag = False

    btn.clicked.connect(handle_end_session)

    cam_thread.start()
    window.show()
    app.exec()
