
import math

class HandUtils:
    
    @staticmethod
    def distance(p1, p2) -> float:
        return math.hypot(p2.x - p1.x, p2.y - p1.y)

    @staticmethod
    def angle(p1, p2) -> float:
        return math.degrees(math.atan2(p2.y - p1.y, p2.x - p1.x))

    @staticmethod
    def get_finger_state(landmarks) -> list:
        tips = [4, 8, 12, 16, 20]
        pips = [3, 6, 10, 14, 18]

        fingers = []
        lm = landmarks.landmark

        fingers.append(
            HandUtils.distance(lm[4], lm[17]) > HandUtils.distance(lm[3], lm[17])
        )

        for tip, pip in zip(tips[1:], pips[1:]):
            fingers.append(lm[tip].y < lm[pip].y)

        return fingers

    @staticmethod
    def count_fingers(landmarks) -> int:
        return sum(HandUtils.get_finger_state(landmarks))