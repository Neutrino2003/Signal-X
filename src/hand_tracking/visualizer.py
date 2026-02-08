
import cv2
import mediapipe as mp

class HandVisualizer:
    def __init__(self):
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        self.connection_spec = self.mp_styles.get_default_hand_connections_style()
        self.landmark_spec = self.mp_styles.get_default_hand_landmarks_style()

    def draw_hands(self, frame, hands_dict):
        for label, hand_data in hands_dict.items():
            if hand_data:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_data.landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    self.landmark_spec,
                    self.connection_spec
                )
                
                wrist = hand_data.landmarks.landmark[0]
                h, w, c = frame.shape
                cx, cy = int(wrist.x * w), int(wrist.y * h)
                
                color = (255, 0, 0) if label == "Left" else (0, 255, 0)
                cv2.putText(frame, label, (cx, cy - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        return frame

    def draw_stats(self, frame, fps):
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame
