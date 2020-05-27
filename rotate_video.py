import cv2
import imutils


path_video = './data/videos/test1.mp4'
video = cv2.VideoCapture(0)


def processing_image(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10)

    contours = cv2.findContours(thres, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=False)

    # print(contours)
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        # print(cv2.boundingRect(c))
        if 50<w<150 and 100<h<200 and 1.6 < h/w < 1.8:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 100, 0), thickness=2)
        elif 100<w<200 and 50<h<150 and 1.6 < w/h < 1.8:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 100, 255), thickness=2)


    return thres



ratio_rotate = 0
ret = True
while ret:
    ret, frame = video.read()

    if ret:
        # if ratio_rotate == 0:
        #     frame = imutils.rotate(frame, ratio_rotate)
        # elif ratio_rotate == 90:
        #     frame = imutils.rotate(frame, ratio_rotate)
        # elif ratio_rotate == -90:
        #     frame = imutils.rotate(frame, ratio_rotate)

        frame = processing_image(frame)
        # frame = cv2.resize(frame, (480, 720))
        cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break
    # elif key == ord('a'):
    #     ratio_rotate = 90
    # elif key == ord('d'):
    #     ratio_rotate = -90
    # elif key == ord('s'):
    #     ratio_rotate = 0
    elif key == ord("s"):
        cv2.imwrite("image.jpg", frame)

video.release()
cv2.destroyAllWindows()