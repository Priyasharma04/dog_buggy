import cv2
import time
from core.detector import PersonDetector
from core.owner_manager import OwnerManager
from core.behavior import BehaviorManager
from core.motion_controller import MotionController
from core.utils import draw
USE_JETSON = False
if USE_JETSON:
    from hardware.camera import get_jetson_camera
    cap = get_jetson_camera()
else:
    cap = cv2.VideoCapture(0)
detector = PersonDetector()
owner_manager = OwnerManager()
motion = MotionController(simulation_mode=not USE_JETSON)
behavior = BehaviorManager(motion, owner_manager)
selected_point = None

def mouse_callback(event, x, y, flags, param):
    global selected_point
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_point = (x, y)

cv2.namedWindow("Buggy")
cv2.setMouseCallback("Buggy", mouse_callback)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()

    detections = detector.track_people(frame)
    print("Detections:", len(detections))

    
    if selected_point is not None and owner_manager.owner_id is None:
        x_click, y_click = selected_point

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]

            if x1 <= x_click <= x2 and y1 <= y_click <= y2:
                owner_manager.owner_id = det["id"]
                owner_manager.last_owner_center = det["center"]

                print("OWNER LOCKED ID:", owner_manager.owner_id)
                break

        selected_point = None
    owner_manager.update_tracks(detections, current_time)
    behavior.update(frame, current_time)

    print("Mode:", behavior.mode)

    owner = owner_manager.get_owner_detection()
    frame = draw(frame, detections, owner)

    cv2.imshow("Buggy", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()