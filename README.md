# 🤖 Tello Drone - Hand Gesture Control

## 🧭 Project Overview

This project demonstrates **gesture-based control of a DJI Tello drone** using computer vision. The drone’s onboard camera captures a live video stream, detects the user’s hand using **MediaPipe’s real-time tracking**, and interprets specific gestures to perform commands such as takeoff, landing, flips, and rotations.

The drone:
- Weighs under 100g
- Features a 5MP HD camera
- Operates up to 100 meters distance and 30 meters altitude
- Battery-powered (1100mAh), with ~13 minutes flight time
- Can be controlled manually or programmatically via SDK

> ![Drone Structure](slide-3.png)
> ![Drone Structure](slide-4.png)

---

## 🎯 Project Objective

Control the drone using **hand gestures** detected in real-time by its camera.

---

## 🧰 Technologies Used

| Tool         | Description                                                |
|--------------|------------------------------------------------------------|
| **Python**   | Main programming language                                  |
| **PyCharm**  | IDE used for development                                   |
| **DJITelloPy** | Python library to interface with the DJI Tello drone      |
| **MediaPipe** | Real-time hand tracking powered by Google’s ML models     |
| **OpenCV**   | For capturing and processing video streams                 |

---

## ✋ Hand Recognition and Landmark Detection

The system uses MediaPipe to detect 21 key hand landmarks. These are used to determine finger positions and directions.

> ![Hand Landmarks](slide-7.png)

To ensure gesture recognition works at different distances from the camera and with varying hand sizes, the system **normalizes distances** based on a fixed ratio between reference points (point 0 and point 5). This makes gesture detection more reliable.

> ![Hand Landmarks](slide-8.png)

---

## 🧠 Understanding Coordinates

MediaPipe returns each landmark as a tuple of `(x, y, z)`:
- `x` – normalized to image width
- `y` – normalized to image height
- `z` – relative to camera depth (not used)

To get actual pixel values:
```python
pixel_x = x * image_width
pixel_y = y * image_height
```
> ![X/Y Coordinate System](slide9.png)

> ![X/Y Coordinate System](slide-10.png)

---

## 🧠 How It Works

1. **Drone Connection:** The drone connects via Wi-Fi and starts streaming video.
2. **Hand Tracking:** MediaPipe identifies up to one hand and its landmarks in the video.
3. **Gesture Recognition:** Based on finger positions and directions, the code detects gestures.
4. **Command Execution:** The drone interprets each gesture and performs corresponding flight maneuvers.

---

## 🎮 Gesture Commands

| Gesture                         | Action                        |
|----------------------------------|-------------------------------|
| 👍 Thumb Up                      | Takeoff                       |
| ✋ All Fingers Up                | Land                          |
| 👉 Thumb + Index → Right        | Move Left 70cm & Flip Right   |
| 👈 Thumb + Index → Left         | Move Right 70cm & Flip Left   |
| 👉 Index Only → Right           | Rotate Counterclockwise 90°   |
| 👈 Index Only → Left            | Rotate Clockwise 90°          |
| ☝️ Index Up                     | Move Up 20cm                  |
| 👇 Index Down                   | Move Down 20cm                |
| ✌️ Index + Middle Up            | Flip Backward                 |
| 🤟 Index + Middle + Ring Up     | Flip Forward and Backward     |

---

## 🚀 Running the Project

### 🔧 Requirements

- Python 3.7+
- Tello drone connected via Wi-Fi
- Install dependencies:
```bash
pip install opencv-python mediapipe djitellopy
```

### ▶️ Launch Main Controller
```bash
python main.py
```
This code:
- Connects to the drone
- Starts live stream
- Recognizes hand gestures
- Sends commands accordingly

### 🧪 Test Hand Detection (No Drone Needed)
```bash
python hand_recognize.py
```
This code:
- Uses your webcam
- Tests MediaPipe hand tracking and gesture classification

---

## ⚠️ Limitations

- The drone stops after 15 seconds if it doesn't receive any commands (safety reasons).
- Drone pauses video processing during flight commands.
- Sensitivity may vary across different users.

---

## 👩‍💻 Authors

- Daniel Semarjian
- Shon Khundiashvili
- Chen Bello
- Elinor Cohen

 
