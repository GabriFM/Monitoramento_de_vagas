import cv2
import numpy as np

#cap = cv2.VideoCapture("http://192.168.0.184:81/stream")


# while(True):
#     ret, frame = cap.read()
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


vagal = [1, 89, 150, 150]


vagas = [vagal]

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)


while True:
    check,img = video.read()
    imgCinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgBlur = cv2.medianBlur(imgTh,5)
    kernel = np.ones((3,3),np.int8)
    imgDil = cv2.dilate(imgBlur,kernel)

    qtVagasAbertas = 0
    for x, y, w, h in vagas:
        recorte = imgDil[y:y + h, x:x + w]
        qtPxBranco = cv2.countNonZero(recorte)
        cv2.putText(img,str(qtPxBranco),(x,y + h - 10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255),1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if qtPxBranco > 1000:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            qtVagasAbertas += 1



    cv2.imshow('video', img)
    cv2.imshow('video TH', imgDil)
    cv2.waitKey(100),