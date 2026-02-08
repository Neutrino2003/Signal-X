
import cv2
import mediapipe as mp
from collections import namedtuple

HandData = namedtuple('HandData', ['landmarks', 'world_landmarks', 'label'])

class HandDetector:
    def __init__(self, static_mode=False, max_hands=2, model_complexity=1, detection_conf=0.7, tracking_conf=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            model_complexity=model_complexity,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.results = None

    def process(self, frame, flip=True):
        if flip:
            frame = cv2.flip(frame, 1)

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_rgb.flags.writeable = False
        self.results = self.hands.process(img_rgb)
        img_rgb.flags.writeable = True

        hands_dict = {'Left': None, 'Right': None}

        if self.results.multi_hand_landmarks and self.results.multi_handedness:
            for idx, hand_type in enumerate(self.results.multi_handedness):
                label = hand_type.classification[0].label
                landmarks = self.results.multi_hand_landmarks[idx]
                world_landmarks = None
                
                if self.results.multi_hand_world_landmarks:
                    world_landmarks = self.results.multi_hand_world_landmarks[idx]

                hands_dict[label] = HandData(landmarks, world_landmarks, label)

        return frame, hands_dict

    def close(self):
        self.hands.close()
