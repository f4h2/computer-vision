import cv2
import numpy as np
import time
import PoseModule as pm

wCam , hCam = 640, 480

cap = cv2.VideoCapture("AiTrainer/2.mp4")

detector = pm.poseDetector()
count = 0
dir = 0
pTime =0
while True:
    success, img = cap.read()
    img = cv2.resize(img,(1280,720))
    #img = cv2.imread("AiTrainer/23.jpg")
    #img = cv2.resize(img, (wCam, hCam))
    img = detector.findPose(img)
    lmList = detector.findPosition(img,False)
    #print(lmList)
    if len(lmList) !=0:
        # Right arm
        detector.findAngle(img,12,14,16)
        # left arm
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle,(210,310),(0,100))          #Hàm np.interp sẽ giúp ta ánh xạ giá trị góc nằm trong khoảng từ 210 đến 310 độ sang giá trị phần trăm trong khoảng từ 0 đến 100%. Cụ thể, giá trị đầu tiên (210, 310) là khoảng giá trị của góc đầu vào, và giá trị thứ hai (0, 100) là khoảng giá trị của giá trị phần trăm đầu ra tương ứng
        bar = np.interp(angle,(220,310), (650,100))
        print(angle,per)

        if per == 100:
            if dir == 0 :
                count +=0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)
        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (1100,75), cv2.FONT_HERSHEY_PLAIN, 4,
                    (255, 0, 0), 4)

        cv2.rectangle(img, (0,450), (250,720), (0,255,0), cv2.FILLED)
        cv2.putText(img,str(int(count)), (45,670), cv2.FONT_HERSHEY_PLAIN,15,
                     (255,0,0),5)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)