import sys
import torch
import cv2
import numpy as np

# Add local yolov5 folder to path
sys.path.append('yolov5')

from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_boxes
from config import PERSON_CLASS_ID, CONF_THRESHOLD


class PersonDetector:
    def __init__(self):
        self.device = 'cpu'
        self.model = DetectMultiBackend('yolov5n.pt', device=self.device)
        self.model.eval()

    def track_people(self, frame):
        img = cv2.resize(frame, (640, 640))
        img = img[:, :, ::-1]  # BGR → RGB
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).float()
        img = img.permute(2, 0, 1) / 255.0
        img = img.unsqueeze(0)

        pred = self.model(img)
        pred = non_max_suppression(pred, CONF_THRESHOLD)

        detections = []

        if len(pred[0]) == 0:
            return detections

        # scale boxes back to original frame
        pred[0][:, :4] = scale_boxes(img.shape[2:], pred[0][:, :4], frame.shape).round()

        for i, det in enumerate(pred[0]):
            x1, y1, x2, y2, conf, cls = det

            if int(cls) != PERSON_CLASS_ID:
                continue

            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            detections.append({
                "id": i,
                "bbox": (x1, y1, x2, y2),
                "center": (cx, cy),
                "area": (x2 - x1) * (y2 - y1),
                "conf": float(conf)
            })

        return detections