import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode =  mode                           # chương trình sẽ sử dụng mô hình phân đoạn bán nguyên tố để tối ưu hóa việc phát hiện các điểm đặc trưng trên tay
        self.maxHands = maxHands
        self.detectionCon = int(detectionCon)       #Ngưỡng xác suất tối thiểu để xác định một điểm đặc trưng trên tay là đúng
        self.trackCon = int(trackCon)               # Ngưỡng xác suất tối thiểu để theo dõi một điểm đặc trưng trên tay khi tay đã được phát hiện.

        self.mpHands = mp.solutions.hands           # khai báo biến mpHands để lưu trữ phương thức phát hiện các điểm đặc trưng trên tay từ thư viện Mediapipe.
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)  # tạo đối tượng Hands từ biến mpHands đã khai báo. Đối tượng Hands này được sử dụng để phát hiện các điểm đặc trưng trên tay người.
        self.mpDraw = mp.solutions.drawing_utils    #khai báo biến mpDraw để lưu trữ phương thức vẽ các đường bản đồ của các điểm đặc trưng trên tay từ thư viện Mediapipe. Biến này được sử dụng để vẽ các đường bản đồ của các điểm đặc trưng trênhình ảnh

    def findHand(self,img,draw=True):


        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                    #chuyển đổi hình ảnh đầu vào từ định dạng màu BGR sang định dạng màu RGB để sử dụng với thư viện Mediapipe
        self.results = self.hands.process(imgRGB)                        #Kết quả trả về của phương thức process() là một đối tượng Results chứa thông tin về các bản đồ landmarks trên tay được phát hiện trong hình ảnh
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:              #vẽ các đường bản đồ của các điểm đặc trưng trên tay lên hình ảnh img. Tham số thứ hai của phương thức draw_landmarks là bản đồ landmarks của tay được phát hiện, tham số thứ ba là self.mpHands.HAND_CONNECTIONS để chỉ định rằng chương trình cần vẽ các đoạn thẳng nối các điểm đặc trưng trên tay để tạo thành các đường bản đồ.
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms , self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        #handNo: Nếu có nhiều tay trong hình ảnh, handNo được sử dụng để chỉ định tay nào trong danh sách các tay được phát hiện sẽ được sử dụng để tìm vị trí của các điểm đặc trưng trên tay.


        lmList = []                                                 #lưu trữ vị trí của các điểm đặc trưng trên tay
        if self.results.multi_hand_landmarks:                       #Trên nguyên tắc, trong Python, biến được khai báo trong một phương thức của một lớp có thể được sử dụng bởi các phương thức khác trong cùng lớp đó, bằng cách sử dụng self.ten_bien.
            myHand = self.results.multi_hand_landmarks[handNo]      #lấy ra tay được chỉ định bởi handNo trong danh sách các tay được phát hiện.
            for id, lm in enumerate(myHand.landmark):               #duyệt qua danh sách các điểm đặc trưng trên tay trong myHand.
                #print(id, lm)
                h, w, c = img.shape                                 #lấy chiều cao, chiều rộng và số kênh màu của hình ảnh đầu vào img.
                cx, cy = int(lm.x * w), int(lm.y * h)               #tính toán vị trí của điểm đặc trưng trên tay theo tọa độ x và y trên hình ảnh
                # print(id, cx, cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 200), cv2.FILLED)
                    # Tham số thứ hai là tọa độ của điểm trung tâm của hình tròn, tham số thứ ba là đường kính của hình tròn,
                    # tham số thứ tư là màu sắc của hình tròn và tham số thứ năm là kiểu vẽ

        return lmList

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHand(img)
        lmList = detector.findPosition(img)
        if len (lmList) !=0:
            print(lmList[4])

        cTime = time.time()  # tính số khung hình trên giây
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()