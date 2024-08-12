import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]

while True:
    imgBG = cv2.imread(r'C:\Users\devve\PycharmProjects\OpencvPython\RockPaperSProject\BG.png')
    imgGameOver = cv2.imread(r'C:\Users\devve\PycharmProjects\OpencvPython\RockPaperSProject\GaameOver.png')
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (2, 5, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    if (randomNumber==1):
                        imgAI = cv2.imread(r'C:\Users\devve\PycharmProjects\OpencvPython\RockPaperSProject\1.png', cv2.IMREAD_UNCHANGED)
                    elif (randomNumber==2):
                        imgAI = cv2.imread(r'C:\Users\devve\PycharmProjects\OpencvPython\RockPaperSProject\2.png', cv2.IMREAD_UNCHANGED)
                    else:
                        imgAI = cv2.imread(r'C:\Users\devve\PycharmProjects\OpencvPython\RockPaperSProject\3.png', cv2.IMREAD_UNCHANGED)

                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # cv2.imshow("Image", img)
    # cv2.imshow("Scaled", imgScaled)
    # imgBGScaled = cv2.resize(imgBG, (0, 0), None, 0.75, 0.75)
    gameOver = False
    if scores[1] ==3 or scores[0] == 3:
        gameOver = True
    if gameOver:
        imgBG = imgGameOver
        if scores[1] > scores[0]:
            cv2.putText(imgBG, "YOU ARE THE WINNER", (265, 490), cv2.FONT_HERSHEY_COMPLEX,
                        2.5, (0, 250, 100), 7)
        else:
            cv2.putText(imgBG, "AI  IS THE  WINNER", (265, 490), cv2.FONT_HERSHEY_COMPLEX,
                        2.5, (0, 250, 100), 7)


    cv2.imshow("STONE PAPER SCISSOR", imgBG)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    if key == ord('r'):
        scores = [0, 0]
        gameOver = False
        startGame = True
        initialTime = time.time()
        stateResult = False
