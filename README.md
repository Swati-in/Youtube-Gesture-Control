# YouTube Gesture Control 🎥✋

Control YouTube videos and system volume using hand gestures! This Python application uses your webcam and computer vision to detect hand gestures and map them to YouTube controls and volume adjustments.

## Features

- **Dual-hand control**: Right hand for YouTube, left hand for volume
- **Real-time gesture detection** using MediaPipe
- **Visual feedback** showing detected gestures and actions
- **Stable gesture recognition** with hold time and cooldown to prevent false triggers

## Demo

The application opens a webcam window showing:
- Live hand tracking with skeletal overlay
- Current gesture being detected
- Visual feedback when actions are triggered
- Distance indicator for volume control

## Gesture Controls

### Right Hand - YouTube Controls

| Gesture | Action | Description |
|---------|--------|-------------|
| ✊ **Fist** | Play/Pause | Close all fingers including thumb |
| ✌️ **Two Fingers** | Next Video | Index and middle fingers up, others down |
| 🤟 **Three Fingers** | Enter Fullscreen | Index, middle, and ring fingers up |
| 🖐️ **Four Fingers** | Exit Fullscreen | All four fingers up (except thumb) |

### Left Hand - Volume Control

| Gesture | Action | Description |
|---------|--------|-------------|
| 🤏 **Pinch (Close)** | Volume Down | Thumb and index finger close together (dist < 0.05) |
| 👌 **Spread (Wide)** | Volume Up | Thumb and index finger far apart (dist > 0.12) |

## Requirements

- Python 3.7+
- Webcam
- Windows/Mac/Linux

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/youtube-gesture-control.git
cd youtube-gesture-control
```

2. **Install dependencies**
```bash
pip install opencv-python mediapipe pyautogui
```

Or using a requirements file:
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
opencv-python>=4.5.0
mediapipe>=0.10.0
PyAutoGUI>=0.9.50
```

## Usage

1. **Open YouTube** in your web browser
2. **Run the script**
```bash
python youtube_gesture_control.py
```
3. **Position yourself** so your hands are visible in the webcam
4. **Make gestures** with your right hand for YouTube controls or left hand for volume
5. **Hold gestures** for 0.5 seconds to trigger actions
6. **Press ESC** to exit the application

## Configuration

You can adjust these settings at the top of the script:

```python
HOLD_TIME = 0.5              # Seconds to hold gesture before triggering
ACTION_COOLDOWN = 0.3        # Seconds between consecutive actions
VOLUME_THRESHOLD_UP = 0.12   # Distance threshold for volume up
VOLUME_THRESHOLD_DOWN = 0.05 # Distance threshold for volume down
```

## Tips for Best Results

- **Good lighting**: Ensure your hands are well-lit
- **Solid background**: Plain backgrounds work best for hand detection
- **Camera position**: Position camera to capture both hands comfortably
- **Deliberate gestures**: Hold gestures steady for the configured hold time
- **One hand at a time**: While dual-hand detection works, controlling one function at a time is more reliable

## Troubleshooting

**Camera not opening:**
- Check if another application is using the webcam
- Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` for a different camera

**Gestures not detected:**
- Ensure your hands are fully visible in the frame
- Improve lighting conditions
- Adjust gesture thresholds in the settings

**Actions triggering multiple times:**
- Increase `HOLD_TIME` for more stable detection
- Increase `ACTION_COOLDOWN` to add more delay between actions

## How It Works

1. **Hand Detection**: MediaPipe detects hand landmarks in real-time
2. **Gesture Recognition**: Finger positions are analyzed to identify specific gestures
3. **Stability Control**: Gestures must be held for a minimum time to prevent false triggers
4. **Action Execution**: PyAutoGUI simulates keyboard presses to control YouTube/system

## Keyboard Shortcuts Used

- `Space`: Play/Pause
- `Shift + N`: Next video
- `F`: Enter fullscreen
- `Esc`: Exit fullscreen
- `VolumeUp`: Increase system volume
- `VolumeDown`: Decrease system volume

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new gestures or features
- Submit pull requests

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking
- [OpenCV](https://opencv.org/) for computer vision
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for keyboard control

## Author

Your Name - [@Swati-in](https://github.com/Swati-in)

---

**Note**: This application simulates keyboard presses and works with YouTube in a web browser. Make sure YouTube is the active window when using the controls.
