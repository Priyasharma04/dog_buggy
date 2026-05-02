class SimpleTracker:
    def __init__(self):
        self.next_id = 0

    def assign_ids(self, detections):
        for d in detections:
            d["id"] = self.next_id
            self.next_id += 1
        return detections