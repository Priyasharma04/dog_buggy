from ultralytics import YOLO
from config import MODEL_PATH, TRACKER_CONFIG, PERSON_CLASS_ID, CONF_THRESHOLD


class PersonDetector:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)

    def track_people(self, frame):
        results = self.model.track(
            source=frame,
            persist=True,
            tracker=TRACKER_CONFIG,
            conf=CONF_THRESHOLD,
            verbose=False
        )

        detections = []

        if not results or len(results) == 0:
            return detections

        result = results[0]
        boxes = result.boxes

        if boxes is None:
            return detections

        xyxy = boxes.xyxy.cpu().numpy()
        cls = boxes.cls.cpu().numpy().astype(int)
        ids = boxes.id.cpu().numpy().astype(int) if boxes.id is not None else None
        confs = boxes.conf.cpu().numpy()

        for i, box in enumerate(xyxy):
            if cls[i] != PERSON_CLASS_ID:
                continue

            track_id = int(ids[i]) if ids is not None and i < len(ids) else -1

            x1, y1, x2, y2 = map(int, box)
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            detections.append({
                "id": track_id,   # ✅ REAL ID
                "bbox": (x1, y1, x2, y2),
                "center": (cx, cy),
                "area": (x2 - x1)*(y2 - y1),
                "conf": float(confs[i])
            })

        return detections