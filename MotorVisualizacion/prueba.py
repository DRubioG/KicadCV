import cv2

cap = cv2.VideoCapture(0)

while 1:
    ret, img=cap.read()
    cv2.rectangle(img, (0,0), (100, 100), (255,0,0), 3)
    cv2.circle(img, (50, 50), 20, (255,0,0))
    cv2.line(img, (100, 100), (200, 200), (0,255,0),1)
    cv2.imshow("prueba", img)

    k=cv2.waitKey(30)
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()