
import time
from src.utils.geometry import HandUtils

class GestureProcessor:
    def __init__(self):
        self.prev_angle = None
        self.prev_swipe_x = None
        self.swipe_cooldown = 0
        self.scroll_y = None

    def process(self, lh, rh):
        if not rh: return ("IDLE", None, "No Hand")

        rh_lm = rh.landmarks.landmark
        rh_fingers = HandUtils.get_finger_state(rh.landmarks)
        rh_count = sum(rh_fingers)
        is_context = lh and sum(HandUtils.get_finger_state(lh.landmarks)) < 2

        if is_context:
            if rh_count == 1 and rh_fingers[0]:
                return ("MEDIA_PLAY", None, "PLAY")
            
            if rh_count == 5:
                return ("MEDIA_PAUSE", None, "PAUSE")

            if rh_count == 2 and rh_fingers[0] and rh_fingers[1]:
                curr_angle = HandUtils.angle(rh_lm[0], rh_lm[8])
                val = 0
                if self.prev_angle:
                    delta = curr_angle - self.prev_angle
                    if delta > 2: val = 1
                    elif delta < -2: val = -1
                self.prev_angle = curr_angle
                return ("VOLUME", val, "Volume")

            if rh_count == 2 and rh_fingers[1] and rh_fingers[2]:
                curr_y = rh_lm[8].y
                scroll_val = 0
                if self.scroll_y:
                    dy = curr_y - self.scroll_y
                    if abs(dy) > 0.05:
                        scroll_val = 3 if dy < 0 else -3
                self.scroll_y = curr_y
                self.prev_angle = None
                return ("SCROLL", scroll_val, "Scroll")

            if rh_count == 3 and rh_fingers[1] and rh_fingers[2] and rh_fingers[3]:
                curr_x = rh_lm[9].x
                val = 0
                if self.prev_swipe_x and (time.time() - self.swipe_cooldown > 0.5):
                    dx = curr_x - self.prev_swipe_x
                    if abs(dx) > 0.08:
                        val = 1 if dx > 0 else -1
                        self.swipe_cooldown = time.time()
                self.prev_swipe_x = curr_x
                return ("SWIPE", val, "Next/Prev" if val else "Ready Swipe")

            self._reset_states()
            return ("IDLE", None, "Ctx Idle")

        else:
            self._reset_states()
            
            if rh_count == 1 and rh_fingers[1]:
                dist = HandUtils.distance(rh_lm[4], rh_lm[8])
                return ("MOUSE_MOVE", (rh_lm[8].x, rh_lm[8].y, dist < 0.05), "Mouse")
            
            return ("IDLE", None, "Idle")

    def _reset_states(self):
        self.prev_angle = None
        self.scroll_y = None
        self.prev_swipe_x = None
