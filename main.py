import cv2
import mediapipe as mp
from djitellopy import tello
import time
import math

# This code captures video from a drone's camera using the TelloPy library,
# and uses the MediaPipe library to detect and track hand landmarks in real time.
# It then calculates the distance between different finger joints and
# the direction of each finger to control the drone's movements.
# The code is limited to recognizing only one hand for improved safety and accuracy.
# It also connects to the drone, gets the battery level and starts the video stream from the drone's camera.
# The code then calculates the distance between different finger joints,
# checks if the finger is pointing up or down,
# and checks the direction of the finger (left or right) to control the drone's movement.
# Then it uses the results of the hand detection
# to send commands to the drone based on the results of the hand detection.


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


# check if the finger is pointed to top or to bot, if the finger is pointed to top the function will return true
def fingerIsUp(img, edge, root):
    threshold_up = -80
    h, w, c = img.shape
    dist = edge.y * h - root.y * h
    if dist <= threshold_up:
        return True
    else:
        return False


# get the finger direction, check if the finger points to right or left
def fingerDirection(img, edge, root):
    threshold_left = -80
    threshold_right = 80
    h, w, c = img.shape
    dist = edge.x * w - root.x * w
    if dist <= threshold_left:
        return "left"
    elif dist >= threshold_right:
        return "right"


# connection to the tello drone, first we connect then get the battery and start the stream from the drone camera
me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()


# recognize the hand mark points in real time, limited to recognize only one hand for safety and accuracy
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils


# parameters that will check the fps of the stream
pTime = 0
cTime = 0


# set the hand array, size of 5, for every finger, and set the drone status to be down
fingers = [0] * 5
is_down = True


# while the drone is connected the code will run
while True:

    # store the frame the drone camera see in real time in the img variable
    img = me.get_frame_read().frame

    # process the image with mediapipe library, and get result from the camera
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # check if the camera recognized hand, if yes for loop will be started
    # the loop will run on the result we got from the result, and check what fingers we got and the directions
    # with the results we got we can send commands to the drone based on the results of the hand

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            # get the relation of the hand, to make the model more accurate, make it work with big/small hands
            # and with different distance from the camera
            dist = get_finger_dist(
                img, handLms.landmark[0], handLms.landmark[5])

            # set the edge and root points values of each finger, for the distance calculation
            thumb_edge = handLms.landmark[4]
            thumb_root = handLms.landmark[1]

            finger1_edge = handLms.landmark[8]
            finger1_root = handLms.landmark[5]

            finger2_edge = handLms.landmark[12]
            finger2_root = handLms.landmark[9]

            finger3_edge = handLms.landmark[16]
            finger3_root = handLms.landmark[13]

            finger4_edge = handLms.landmark[17]
            finger4_root = handLms.landmark[20]

            # calculate the distance of each finger, and divide with the relation for the accuracy
            thumb = get_finger_dist(
                img, thumb_root, thumb_edge) / dist

            finger1 = get_finger_dist(
                img, finger1_root, finger1_edge) / dist

            finger2 = get_finger_dist(
                img, finger2_root, finger2_edge) / dist

            finger3 = get_finger_dist(
                img, finger3_root, finger3_edge) / dist

            finger4 = get_finger_dist(
                img, finger4_root, finger4_edge) / dist

            # check by the distance between the root and the edge of each finger, if the finger is raised or not
            # and set the value in the hand array to 1 or 0, 1 for raised and 0 for not
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

            # The drone commands that will execute by the result from the hand recognize results

            # move up the drone (thumb raised)
            if fingers == [1, 0, 0, 0, 0] and fingerIsUp(img, thumb_edge, thumb_root) and is_down:
                me.takeoff()
                is_down = False

            # stop the drone and land him (5 fingers raised)
            elif fingers == [1, 1, 1, 1, 1] and not is_down:
                me.land()
                is_down = True

            # make the drone move right and make flip to left (finger pointed to right with thumb up )
            elif fingers == [1, 1, 0, 0, 0] and\
                    fingerDirection(img, finger1_edge, finger1_root) == "right" and not is_down:
                me.move_right(70)
                me.flip_left()

            # make the drone move left and make flip to right (finger pointed to left with thumb up)
            elif fingers == [1, 1, 0, 0, 0] and \
                    fingerDirection(img, finger1_edge, finger1_root) == "left" and not is_down:
                me.move_left(70)
                me.flip_right()

            # make the drone make clockwise rotate (finger pointed to right without thumb up )
            elif fingers == [0, 1, 0, 0, 0] and \
                    fingerDirection(img, finger1_edge, finger1_root) == "right" and not is_down:
                me.rotate_clockwise(90)

            # make the drone counterclockwise rotate  (finger pointed to left without thumb up)
            elif fingers == [0, 1, 0, 0, 0] and \
                    fingerDirection(img, finger1_edge, finger1_root) == "left" and not is_down:
                me.rotate_counter_clockwise(90)

            # make the drone ascend 20 cm (finger raised)
            elif fingers == [0, 1, 0, 0, 0] and\
                    fingerIsUp(img, finger1_edge, finger1_root) and not is_down:
                me.move_up(20)

            # make the drone descend 20 cm (finger pointed down)
            elif fingers == [0, 1, 0, 0, 0] and \
                    not fingerIsUp(img, finger1_edge, finger1_root) and not is_down:
                me.move_down(20)

            # make a flip backwards (by 2 fingers ( finger1 and finger2 ) raised)
            elif fingers == [0, 1, 1, 0, 0] and \
                    fingerIsUp(img, finger1_edge, finger1_root) and not is_down:
                me.flip_back()

            # make a flip backwards and then forward(by 3 fingers ( finger1, finger2 and finger3 ) raised)
            elif fingers == [0, 1, 1, 1, 0] and \
                    fingerIsUp(img, finger1_edge, finger1_root) and not is_down:
                me.flip_forward()
                me.flip_back()

            # draw the vectors and the points on the hand while it recognized
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # get the current time
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # put the fps on the video
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    # display the camera result from the drone on the computer
    cv2.imshow("Image", img)
    cv2.waitKey(1)
