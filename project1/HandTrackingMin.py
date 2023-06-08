import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands            #khai báo biến mpHands để lưu trữ phương thức phát hiện các điểm đặc trưng trên tay từ thư viện Mediapipe.
hands = mpHands.Hands()                 #tạo đối tượng Hands từ biến mpHands đã khai báo. Đối tượng Hands này được sử dụng để phát hiện các điểm đặc trưng trên tay người.
mpDraw = mp.solutions.drawing_utils     #khai báo biến mpDraw để lưu trữ phương thức vẽ các đường bản đồ của các điểm đặc trưng trên tay từ thư viện Mediapipe. Biến này được sử dụng để vẽ các đường bản đồ của các điểm đặc trưng trênhình ảnh

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)                        #Kết quả trả về của phương thức process() là một đối tượng Results chứa thông tin về các bản đồ landmarks trên tay được phát hiện trong hình ảnh
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id,cx,cy)
                # if id==4:
                cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms , mpHands.HAND_CONNECTIONS)
    cTime = time.time()   # tính số khung hình trên giây
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,
    (255,0,255),3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)