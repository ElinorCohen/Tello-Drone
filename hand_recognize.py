import cv2
import mediapipe as mp
import time
import math

# This code captures video from the computer's camera using the OpenCV library,
# and uses the MediaPipe library to detect and track hand landmarks in real time.
# It then calculates the distance between different finger joints to determine whether a finger is raised or not.
# The code is limited to recognizing only one hand for improved safety and accuracy.
# The code also calculates the frames per second (FPS) of the video stream and displays it on the screen.
# Additionally, it draws the hand landmarks on the video frame and displays the result in a window named "Image".


# check the distance between 2 points will be used in the finger distance calculation
def distance(x1, y1, x2, y2):
    x = math.pow(x1 - x2, 2)
    y = math.pow(y1 - y2, 2)
    return math.sqrt(x + y)

# get the distance between 2 fingers to understand if the finger rise or not
def get_finger_dist(img, lm1, lm2):
    h, w, c = img.shape
    x1 = int(lm1.x * w)
    y1 = int(lm1.y * h)
    x2 = int(lm2.x * w)
    y2 = int(lm2.y * h)
    return distance(x1, y1, x2, y2)

# open the computer camera
cap = cv2.VideoCapture(0)

# recognize the hand mark points in real time, limited to recognize only one hand for safety and accuracy
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# parameters that will check the fps of the stream, and set the array of the hand
pTime = 0
cTime = 0
fingers = [0] * 5


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            dist = get_finger_dist(img, handLms.landmark[0], handLms.landmark[5])
            thumb = get_finger_dist(img, handLms.landmark[1], handLms.landmark[4]) / dist
            finger1 = get_finger_dist(img, handLms.landmark[5], handLms.landmark[8]) / dist
            finger2 = get_finger_dist(img, handLms.landmark[9], handLms.landmark[12]) / dist
            finger3 = get_finger_dist(img, handLms.landmark[13], handLms.landmark[16]) / dist
            finger4 = get_finger_dist(img, handLms.landmark[17], handLms.landmark[20]) / dist

            if thumb > 0.9:
                fingers[0] = 1
            else:
                fingers[0] = 0

            if finger1 > 0.5:
                fingers[1] = 1
            else:
                fingers[1] = 0

            if finger2 > 0.5:
                fingers[2] = 1
            else:
                fingers[2] = 0

            if finger3 > 0.5:
                fingers[3] = 1
            else:
                fingers[3] = 0

            if finger4 > 0.5:
                fingers[4] = 1
            else:
                fingers[4] = 0

            print(fingers)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)