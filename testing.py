import cv2
import mediapipe as mp
import pyautogui
import time

# -------------------------
# SETTINGS
# -------------------------
HOLD_TIME = 0.5
ACTION_COOLDOWN = 0.3
VOLUME_DIST_DIV = 4
VOLUME_THRESHOLD_UP = 0.12
VOLUME_THRESHOLD_DOWN = 0.05

# -------------------------
# HELPER: YouTube functions
# -------------------------
def yt_play_pause(): pyautogui.press("space")
def yt_next_video(): pyautogui.hotkey("shift", "n")
def yt_fullscreen(): pyautogui.press("f")
def yt_exit_fullscreen(): pyautogui.press("esc")

# -------------------------
# GESTURE DETECTION HELPERS
# -------------------------
def fingers_status(hand):
    tips = [8, 12, 16, 20]  # index, middle, ring, pinky
    return [hand.landmark[tip].y < hand.landmark[tip - 2].y for tip in tips]

def is_fist(hand):
    fingers_folded = all(hand.landmark[tip].y > hand.landmark[tip - 2].y for tip in [8,12,16,20])
    thumb_tip = hand.landmark[4]
    thumb_mcp = hand.landmark[2]
    thumb_folded = thumb_tip.y > thumb_mcp.y - 0.1
    return fingers_folded and thumb_folded

def is_two_fingers(hand):
    idx, mid, ring, pinky = fingers_status(hand)
    return idx and mid and not ring and not pinky

def is_three_fingers(hand):
    idx, mid, ring, pinky = fingers_status(hand)
    return idx and mid and ring and not pinky

def is_four_fingers(hand):
    idx, mid, ring, pinky = fingers_status(hand)
    return idx and mid and ring and pinky

# -------------------------
# STABILITY / STATE TRACKER
# -------------------------
class GestureState:
    def __init__(self):
        self.current = None
        self.start_time = 0.0
        self.last_action_time = 0.0

    def update(self, gesture_name):
        now = time.time()
        if gesture_name != self.current:
            self.current = gesture_name
            self.start_time = now

    def held_long_enough(self):
        return (time.time() - self.start_time) >= HOLD_TIME

    def can_trigger(self):
        return (time.time() - self.last_action_time) >= ACTION_COOLDOWN

    def mark_triggered(self):
        self.last_action_time = time.time()

# -------------------------
# MAIN PROGRAM
# -------------------------
webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mp_hands = mp.solutions.hands
my_hands = mp_hands.Hands(max_num_hands=2)
drawing_utils = mp.solutions.drawing_utils

gesture_state = GestureState()

while True:
    ret, image = webcam.read()
    if not ret or image is None:
        time.sleep(0.1)
        continue

    image = cv2.flip(image, 1)
    h, w, _ = image.shape
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = my_hands.process(rgb)
    hands = results.multi_hand_landmarks
    handedness = results.multi_handedness

    cv2.putText(image, "YouTube Gesture Control", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    if hands and handedness:
        for i, hand in enumerate(hands):
            label = handedness[i].classification[0].label  # 'Left' or 'Right'
            drawing_utils.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

            # ---------------------
            # Right Hand → YouTube Gestures
            # ---------------------
            if label == "Right":
                detected_gesture = "none"
                if is_fist(hand):
                    detected_gesture = "fist"
                elif is_two_fingers(hand):
                    detected_gesture = "two_fingers"
                elif is_three_fingers(hand):
                    detected_gesture = "three_fingers"
                elif is_four_fingers(hand):
                    detected_gesture = "four_fingers"

                gesture_state.update(detected_gesture)

                if detected_gesture == "fist" and gesture_state.held_long_enough() and gesture_state.can_trigger():
                    gesture_state.mark_triggered()
                    yt_play_pause()
                    cv2.putText(image, "YT: Play/Pause", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                elif detected_gesture == "two_fingers" and gesture_state.held_long_enough() and gesture_state.can_trigger():
                    gesture_state.mark_triggered()
                    yt_next_video()
                    cv2.putText(image, "YT: Next", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                elif detected_gesture == "three_fingers" and gesture_state.held_long_enough() and gesture_state.can_trigger():
                    gesture_state.mark_triggered()
                    yt_fullscreen()
                    cv2.putText(image,"YT: Fullscreen",(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

                elif detected_gesture == "four_fingers" and gesture_state.held_long_enough() and gesture_state.can_trigger():
                    gesture_state.mark_triggered()
                    yt_exit_fullscreen()
                    cv2.putText(image,"YT: Exit Fullscreen",(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

            # ---------------------
            # Left Hand → Volume Control
            # ---------------------
            elif label == "Left":
                thumb_tip = hand.landmark[4]
                index_tip = hand.landmark[8]
                dist = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5

                cv2.line(image,
                         (int(thumb_tip.x*w), int(thumb_tip.y*h)),
                         (int(index_tip.x*w), int(index_tip.y*h)),
                         (0, 255, 0), 3)
                cv2.putText(image, f"Dist:{dist:.2f}", (w-160,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200),2)

                if dist > VOLUME_THRESHOLD_UP and gesture_state.can_trigger():
                    pyautogui.press("volumeup")
                    gesture_state.mark_triggered()
                    cv2.putText(image, "SYS: Vol Up", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                elif dist < VOLUME_THRESHOLD_DOWN and gesture_state.can_trigger():
                    pyautogui.press("volumedown")
                    gesture_state.mark_triggered()
                    cv2.putText(image, "SYS: Vol Down", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    else:
        gesture_state.update("none")

    cv2.putText(image, f"Gesture: {gesture_state.current}", (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("YouTube Hand Control", image)
    if cv2.waitKey(10) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
