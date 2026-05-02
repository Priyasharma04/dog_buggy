class OwnerManager:
    def __init__(self):
        self.owner_id = None
        self.current_tracks = {}
        self.last_owner_center = None
        self.last_seen_time = None
        self.stationary_start = None

    def update_tracks(self, detections, current_time):
        self.current_tracks = {i: d for i, d in enumerate(detections)}

        owner = self.get_owner_detection()

        if owner:
            self.last_seen_time = current_time

            if self.last_owner_center is None:
                self.last_owner_center = owner["center"]
                self.stationary_start = current_time
            else:
                dx = abs(owner["center"][0] - self.last_owner_center[0])
                dy = abs(owner["center"][1] - self.last_owner_center[1])

                if dx < 20 and dy < 20:
                    pass
                else:
                    self.stationary_start = current_time

                self.last_owner_center = owner["center"]

    def select_closest(self, w, h):
        cx, cy = w // 2, h // 2

        best = None
        best_dist = 1e9

        for d in self.current_tracks.values():
            dx = d["center"][0] - cx
            dy = d["center"][1] - cy
            dist = dx*dx + dy*dy

            if dist < best_dist:
                best = d
                best_dist = dist

        if best:
            self.owner_id = 0
            self.last_owner_center = best["center"]

    def get_owner_detection(self):
        if self.owner_id is None or self.last_owner_center is None:
            return None

        best = None
        best_dist = 1e9

        for d in self.current_tracks.values():
            dx = d["center"][0] - self.last_owner_center[0]
            dy = d["center"][1] - self.last_owner_center[1]
            dist = dx*dx + dy*dy

            if dist < best_dist:
                best = d
                best_dist = dist

        return best

    def stationary_time(self, current_time):
        if self.stationary_start is None:
            return 0
        return current_time - self.stationary_start