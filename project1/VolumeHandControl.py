import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

############################
wCam, hCam = 648, 480
############################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

detector = htm.handDetector(detectionCon = 0.7)

############################################ ***

devices = AudioUtilities.GetSpeakers()                                              #Lấy thông tin về thiết bị loa trên hệ thống và trả về một đối tượng
interface = devices.Activate( IAudioEndpointVolume._iid_ , CLSCTX_ALL, None)        #Kích hoạt đối tượng IAudioEndpointVolume để thực hiện các thao tác điều khiển âm lượng trên thiết bị đầu ra âm thanh
volume = cast(interface, POINTER(IAudioEndpointVolume))                             #Chuyển đổi đối tượng interface sang đối tượng POINTER(IAudioEndpointVolume) để có thể sử dụng các phương thức điều khiển âm lượng.
#volume.GetMute()                                                                    #Lấy trạng thái tắt/mở tiếng của thiết bị đầu ra âm thanh. Trả về True nếu tiếng bị tắt và False nếu tiếng đang được bật.
#volume.GetMasterVolumeLevel()                                                       #ấy mức âm lượng hiện tại của thiết bị đầu ra âm thanh, được tính bằng đơn vị decibel (dB).
volRange = volume.GetVolumeRange()                                                          #Lấy giới hạn mức âm lượng của thiết bị đầu ra âm thanh. Trả về một bộ ba (min_volume, max_volume, volume_step) trong đó min_volume và max_volume lần lượt là mức âm lượng tối thiểu và tối đa của thiết bị và volume_step là khoảng cách giữa các mức âm lượng có thể đặt được.
# volume.SetMasterVolumeLevel(0, None)                                            #Thiết lập mức âm lượng cho thiết bị đầu ra âm thanh. Trong đoạn code này, mức âm lượng được đặt là -20 dB, tức là mức âm lượng khá thấp. Tham số thứ hai là None để chỉ định không có đối tượng cập nhật trạng thái âm thanh được trả về.

############################################ ***

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
while True:
    success , img = cap.read()
    img = detector.findHand(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        cx,cy =(x1+x2)//2,(y1+y2) //2

        cv2.circle(img,(x1,y1), 5, (255,0,255), cv2.FILLED)
        cv2.circle(img,(x2,y2), 5, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy), 5,(255,0,255), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)                        #tính độ dài của một đoạn thẳng nối hai điểm (x1, y1) và (x2, y2) trong không gian hai chiều, dựa trên định lý Pythagoras trong tam giác vuông.
        print(length)

        # hand range 50 - 300
        #volume range -65 - 0

        vol = np.interp(length,[50,300], [minVol, maxVol])                  #np.interp(length,[50,300], [minVol, maxVol]): Chuyển đổi giá trị length sang giá trị âm lượng tương ứng trong khoảng giá trị [minVol, maxVol]. Hàm np.interp() sử dụng phương pháp tuyến tính để tính toán giá trị tương ứng. Trong đó, tham số đầu tiên length là giá trị cần chuyển đổi, tham số thứ hai [50,300] là khoảng giá trị đầu vào, trong đó 50 là giá trị nhỏ nhất và 300 là giá trị lớn nhất, tham số thứ ba [minVol, maxVol] là khoảng giá trị đầu ra, trong đó minVol là giá trị nhỏ nhất và maxVol là giá trị lớn nhất.
        volBar = np.interp(length, [50, 300], [400,150])
        volPer = np.interp(length, [50, 300], [0, 150])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx,cy), 15,(0,255,0), cv2.FILLED)

    cv2.rectangle(img,(50,150), (85,400),(0,255,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 250, 0), 3)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX,
                1,(255,0,0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)