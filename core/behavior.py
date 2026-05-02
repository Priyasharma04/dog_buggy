from config import *

class BehaviorManager:
    def __init__(self, motion, owner_manager):
        self.motion = motion
        self.owner_manager = owner_manager
        self.mode = "IDLE"

    def update(self, frame, current_time):
        owner = self.owner_manager.get_owner_detection()

        if owner is None:
            if self.owner_manager.last_seen_time and \
               current_time - self.owner_manager.last_seen_time > LOST_TIMEOUT:
                self.mode = "SEARCH"
                self.motion.left()
            else:
                self.motion.stop()
            return

        if self.owner_manager.stationary_time(current_time) > STATIONARY_TIME_THRESHOLD:
            self.mode = "IDLE_SPIN"
            self.motion.left()
            return

        self.mode = "FOLLOW"

        cx = owner["center"][0]
        frame_center = frame.shape[1] // 2

        if cx < frame_center - CENTER_TOLERANCE:
            self.motion.left()
        elif cx > frame_center + CENTER_TOLERANCE:
            self.motion.right()
        else:
            if owner["area"] < TARGET_BOX_AREA_MIN:
                self.motion.forward()
            elif owner["area"] > TARGET_BOX_AREA_MAX:
                self.motion.backward()
            else:
                self.motion.stop()