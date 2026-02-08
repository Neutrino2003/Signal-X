
import cv2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hand_tracking.detector import HandDetector
from src.hand_tracking.visualizer import HandVisualizer
from src.controllers.mouse import MouseController
from src.controllers.media import MediaController
from src.core.processor import GestureProcessor

def main():
    detector = HandDetector(max_hands=2, detection_conf=0.7)
    visualizer = HandVisualizer()
    processor = GestureProcessor()
    
    mouse = MouseController(sensitivity=1.2)
    media = MediaController()
    cap = cv2.VideoCapture(0)
    
    print(">>> Gesture System Active <<<")

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        frame, hands = detector.process(frame, flip=True)
        action, val, status = processor.process(hands.get('Left'), hands.get('Right'))
        
        if action == "MOUSE_MOVE":
            x, y, click = val
            mouse.move_relative(x, y)
            if click: 
                mouse.click()
                status = "CLICK"
            else:
                mouse.toggle_drag(False)

        elif action == "SCROLL":
            mouse.scroll(val)
        
        elif action == "VOLUME":
            if val == 1: media.volume_change(True)
            elif val == -1: media.volume_change(False)

        elif action == "MEDIA_PLAY":
            media.play()
        
        elif action == "MEDIA_PAUSE":
            media.pause()
            
        elif action == "SWIPE":
            if val == 1: media.next()
            elif val == -1: media.prev()

        elif action == "IDLE":
            mouse.reset()

        visualizer.draw_hands(frame, hands)
        cv2.putText(frame, f"State: {status}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Gesture Controller', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    detector.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
