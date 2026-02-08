
import cv2
import time
import sys
import os

# Add project root to python path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hand_tracking.detector import HandDetector
from src.hand_tracking.visualizer import HandVisualizer

def run_pipeline():
    # Initialize Pipeline
    # detection_conf=0.7 is robust. Lower it if hands are lost easily in bad lighting.
    detector = HandDetector(max_hands=2, detection_conf=0.7)
    visualizer = HandVisualizer()

    # Start Camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Gesture Control Pipeline Started.")
    print("Press 'q' to exit.")

    prev_time = 0

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Warning: Empty frame.")
                break

            # 1. Process Frame (Core Pipeline)
            # We flip internally in the detector, so 'frame' returned is the flipped one
            frame, hands = detector.process(frame, flip=True)

            # 2. Logic Placeholder
            # This is where we will eventually add: 
            # if hands['Right']: move_mouse(hands['Right'])
            
            # Simple debug print to prove pipeline works
            if hands['Left'] and hands['Right']:
                status = "Both Hands"
            elif hands['Left']:
                status = "Left Only"
            elif hands['Right']:
                status = "Right Only"
            else:
                status = "No Hands"

            # 3. Visualization
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
            prev_time = current_time

            visualizer.draw_hands(frame, hands)
            visualizer.draw_stats(frame, fps)
            
            # Add status text
            cv2.putText(frame, f"Status: {status}", (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            # 4. Display
            cv2.imshow('Gesture Pipeline Test', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        detector.close()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_pipeline()
