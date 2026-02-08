# Gesture Control System

A high-performance, real-time hand gesture recognition system for hands-free computer interaction. This project transforms a standard webcam into a sophisticated input device, allowing for seamless mouse navigation, media control, and system automation.

---

## Table of Contents
1. [Key Features](#key-features)
2. [Detailed Architecture](#detailed-architecture)
3. [The Remote Control Guide (Gesture Mappings)](#the-remote-control-guide)
4. [Deep Learning Model: InceptionV3 + LSTM](#deep-learning-model)
5. [Legacy Methods and Comparative Analysis](#legacy-methods)
6. [Workflow and Data Pipeline](#workflow-and-data-pipeline)
7. [Installation and Requirements](#installation)
8. [Usage and Configuration](#usage)

---

## Key Features

*   **Real-Time Responsiveness**: Optimized to run at 60+ FPS on standard CPUs by utilizing a lightweight heuristic engine.
*   **Dual-Mode Contextual Logic**: Uses the presence of a second hand as a "modifier" to switch between system navigation and media control.
*   **Geometric Precision**: Calculates exact finger angles and palm rotation for fine-tuned controls like volume and scrolling.
*   **Hybrid Intelligence**: Combines skeletal tracking with a custom state machine for immediate feedback, plus an InceptionV3-LSTM backend for complex gesture learning.

---

## Detailed Architecture

The project is structured to separate data acquisition, logic processing, and system execution:

### 1. Hand Tracking Module (src/hand_tracking)
*   **Detector**: Uses high-precision skeletal tracking to identify 21 specific points (knuckles, tips, palm) for up to two hands. These raw points are the foundation for all gesture calculations.
*   **Visualizer**: Provides a real-time HUD (Heads-Up Display) that draws skeletal connections and labels the current detected state on the video feed.

### 2. Core Processor (src/core/processor.py)
This is the "Brain" of the live application. It operates as a **Heuristic State Machine**:
*   **Finger Counting**: Uses the relative positions of finger tips and PIP joints to determine which fingers are extended.
*   **Geometry Calculation**: Measures the Euclidean distance between landmarks (e.g., Index Tip to Thumb Tip for clicks) and trigonometric angles (for rotation-based volume control).
*   **Context Switching**: Dynamically shifts the active "Controller" based on whether the Left Hand is raised in a specific posture (fist).

### 3. Controllers (src/controllers)
*   **MouseController**: Interface for `pynput` to control cursor position, clicks, and drags. It includes a sensitivity multiplier to map webcam coordinates to screen resolution.
*   **MediaController**: Maps gestures to system media keys (Volume Up/Down, Play/Pause, Next/Prev Track).

---

## The Remote Control Guide

The system uses a contextual approach where the **Left Hand** acts as a mode-switcher.

### Mouse Mode (Default)
Active when only the Right Hand is visible or the Left Hand is down.

*   **Cursor Movement**: Index finger extended. The system tracks the Tip of the index finger and maps its movement to the screen.
*   **Left Click**: A quick "pinch" gesture where the Index Tip and Thumb Tip touch (distance falls below a calibrated threshold).
*   **Drag and Drop**: Maintain the pinch gesture while moving the hand. Releasing the pinch "drops" the item.

### Media Mode (2-Hand Gestures)
Active when the **Left Hand is in a Fist** (0 to 1 fingers extended).

*   **Volume Control**: With the Left Hand in a fist, "twist" your Right Hand (using the Index and Thumb as a reference). The system calculates the change in angle to increase or decrease system volume.
*   **Scrolling**: With the Left Hand in a fist, extend the Index and Middle fingers on the Right Hand. Moving the hand vertically scrolls the active window.
*   **Play/Pause**: Thumb up for Play; Open Palm (5 fingers) for Pause.
*   **Navigation**: Swipe the Right Hand horizontally (3 fingers extended) to go to the Next or Previous track.

---

## Deep Learning Model

For scenarios requiring recognition of dynamic motions that simple rules cannot capture, the project includes a powerful neural network:

*   **Visual Backbone (InceptionV3)**: A pre-trained convolutional neural network (CNN) that extracts 2,048 visual features from every frame. This allows the model to "see" hand shapes and orientations.
*   **Temporal Processor (LSTM)**: A Long Short-Term Memory network that processes sequences of 16 frames at a time. This allows the system to recognize gestures that are defined by movement over time (e.g., waving or drawing in the air).
*   **Training Pipeline**: Includes data augmentation (brightness adjustment, mirroring) to ensure the model works in various lighting conditions.

---

## Legacy Methods and Comparative Analysis

We explored several architectures before settling on the current Hybrid system. These experiments represent discontinued approaches:

| Architecture | Outcome | Conclusion |
| :--- | :--- | :--- |
| **3D CNN + LSTM** | 93.35% Accuracy | **Outcome**: Excellent at recognizing motion but required 1.5+ seconds per frame on a CPU. **Conclusion**: Too slow for real-time mouse control where millisecond latency is critical. |
| **Static Gesture Model** | 94.33% Accuracy | **Outcome**: Fast and reliable at recognizing fixed hand signs. **Conclusion**: Abandoned because it lacked flexibility. It could not handle custom 2-hand interactions or the continuous math needed for volume/scrolling. |
| **Landmarks Only (LSTM)** | 82.66% Accuracy | **Outcome**: Very lightweight and fast. **Conclusion**: Inaccurate. Without original image pixels, the model struggled to distinguish between similar poses when tracking points jittered. |

---

## Workflow and Data Pipeline

![Hand Tracking Flow](OpenCV%20Hand%20Tracking%20Flow-2026-02-07-225947.png)

1.  **Frame Capture**: OpenCV captures raw frames at 30-60 FPS.
2.  **Tracking**: Identify 21 landmarks per hand using skeletal detection.
3.  **Heuristic Analysis**:
    *   Calculate finger states (Up/Down).
    *   Calculate hand orientation (Roll/Pitch/Yaw).
    *   Calculate distance deltas for pinch detection.
4.  **Action Dispatch**: The `GestureProcessor` sends an abstract command (e.g., `SCROLL_UP`) to the appropriate Controller.
5.  **OS Execution**: `pynput` or OS-specific APIs execute the final command on the host machine.

**Note on 2-Hand Accuracy**: 
Volume and Scroll gestures require both hands. Accuracy may drop due to occlusion (one hand blocking another), tracking jitter in low light, or shadows interfering with the sensor.

---

## Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd Gesture_control
    ```

2.  **Environment Setup**:
    It is recommended to use Python 3.9 or higher.
    ```bash
    pip install -r requirements.txt
    ```

3.  **OS Specifics**:
    *   **Linux**: Ensure `libcanberra-gtk-module` is installed for OpenCV.
    *   **Permissions**: Grant camera and accessibility (Input Monitoring) permissions to your terminal/IDE.

---

## Usage

### Run the Main Application
```bash
python scripts/run_mouse.py
```

### Configuration
Adjust parameters in `src/config.py` to match your hardware:
*   `SEQ_LENGTH`: Number of frames to group for the DL model.
*   `IMG_SIZE`: Resolution for the CNN input.
*   `sensitivity`: Change this in `run_mouse.py` to speed up or slow down the cursor.

---
*Created as part of a Deep Learning Gesture Recognition Project.*