import cv2

def get_jetson_camera():
    return cv2.VideoCapture(
        "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480 ! nvvidconv ! videoconvert ! appsink"
    )