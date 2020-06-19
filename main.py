"""
Import backage
"""
import cv2
import numpy as np
import time
import imutils
# from Connect_Ardruino import Connect

# path to file yolo
weights = "./models/weights/yolov3-spp3_95_50.weights"
config = "./models/configs/prune_95_50.cfg"
input_shape = 416
scale = 0.00392
# scale = 0.00432

print("[INFO] Check webcam/video...")
cap = cv2.VideoCapture('./data/videos/test1.mp4')
# cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("[INFO] Loading video/webcam ===>> Ok...!")
    # Connect(user_input="w")
else:
    print("[INFO] Fail to load webcam/video...")

print("[INFO] Loading model...")
# Load YOLO files
net = cv2.dnn.readNet(weights, config)
# net = cv2.dnn.readNet("./models/yolov3.models", "./models/yolov3.cfg")

layer_names = net.getLayerNames()
# print(layer_names)
outputLayers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
# print(outputLayers)


total_cham = 8
total_congvao = 1
total_congra = 1
total_ic = 1
total_eoi = 1
total_nutbam = 4
total_tu = 4
total_adap = 1
total_chipdan = 8

def check_link_kien(dem_cham, dem_congvao, dem_congra, dem_ic, dem_eoi, dem_nutbam, dem_tu, dem_adap, dem_chipdan):
    print("[INFO] Check link kiện...")
    count = 0
    if int(dem_cham) == total_cham:
        print("Đủ")
        count +=1
    else:
        print("Thiếu {} cham".format(total_cham - int(dem_cham)))

    if int(dem_congvao) == total_congvao:
        print("Đủ")
        count +=1
    else:
        print("Thiếu {} cổng vào".format(total_congvao - int(dem_congvao)))

    if int(dem_congra) == total_congra:
        print("Đủ")
        count +=1
    else:
        print("Thiếu {} cổng ra".format(total_congra - int(dem_congra)))

    if int(dem_ic) == total_ic:
        print("Đủ")
        count +=1
    else:
        print("Thiếu {} ic".format(total_ic - int(dem_ic)))

    if int(dem_eoi) == total_eoi:
        print("Đủ")
        count +=1
    else:
        print("Thiếu {} eoi".format(total_eoi - int(dem_eoi)))

    if int(dem_nutbam) == total_nutbam:
        print("Đủ")
        count +=1
    else:
        print("Thiếu {} nút bấm".format(total_nutbam - int(dem_nutbam)))

    if int(dem_tu) == total_tu:
        print("Đủ")
        count +=1
    else:
        print("Thiếu {} tụ".format(total_tu - int(dem_tu)))

    if int(dem_adap) == total_adap:
        print("Đủ")
        count +=1
    else:
        print("Thiếu {} adap".format(total_adap - int(dem_adap)))

    if int(dem_chipdan) == total_chipdan:
        print("Đủ")
        count +=1
    else:
        print("Thiêu {} chipdan".format(total_chipdan - int(dem_chipdan)))
    return count


def check_connect(count):
    total = 7
    if count >= total:
        print("[INFO] ===>>> PASS <<<===\n")
        # Connect(user_input="f")
    else:
        print("[INFO] ===>>> FAIL <<<===\n")
        # Connect(user_input="p")

# classes="./data/labels/classes_full.names"
classes_path = "./data/labels/classes_full.names"
def load_classes():
    classes = []
    with open(classes_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    return classes, colors
classes, colors = load_classes()
# print(classes[0])


def processing_image(frame, outputLayers, height, width):
    print("[INFO] Proccessing...")

    blob = cv2.dnn.blobFromImage(frame, scale, (input_shape, input_shape), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    # print(net)
    outs = net.forward(outputLayers)
    # print(outs)
    
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                centre_x = int(detection[0]*width)
                centre_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(centre_x - w/2)
                y = int(centre_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

    return indexes, boxes, confidences, class_ids


def draw_boxes(boxes, classes, confidences, colors):
    # print("[INFO] Drawing boxes...")
    dem_cham = 0
    dem_congvao = 0
    dem_congra = 0
    dem_ic = 0
    dem_eoi = 0
    dem_nutbam = 0
    dem_tu = 0
    dem_adap = 0
    dem_chipdan = 0
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            # print(class_ids[i])
            label = classes[class_ids[i]]
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label+" "+str(round(confidence, 2)), (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
            # cv2.putText(frame, label, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
            
            if label == ".":
                dem_cham +=1
            elif label == "congvao":
                dem_congvao +=1
            elif label == "congra":
                dem_congra +=1
            elif label == "ic":
                dem_ic +=1
            elif label == "eoi":
                dem_eoi +=1
            elif label == "nutbam":
                dem_nutbam +=1
            elif label == "tu":
                dem_tu +=1
            elif label == "adap":
                dem_adap +=1
            elif label == "chipdan":
                dem_chipdan += 1
            # print("-------")
    # print(dem_tu)
    return frame, dem_cham, dem_congvao, dem_congra, dem_ic, dem_eoi, dem_nutbam, dem_tu, dem_adap, dem_chipdan


# def counter_frame():
#     # check total frames
#     prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
#         else cv2.CAP_PROP_FRAME_COUNT
#     total_frame = int(cap.get(prop))
#     print("[INFO] {} total frames in video".format(total_frame))
# counter_frame()

frame_id = 0
start = time.time()

ratio_rotate = 0
ret = True
while ret:
    ret, frame = cap.read()
    frame_id +=1

    # time.sleep(5)
    if ret:
        if ratio_rotate == 0:
            frame = imutils.rotate(frame, ratio_rotate)
        elif ratio_rotate == 90:
            frame = imutils.rotate(frame, ratio_rotate)
        elif ratio_rotate == -90:
            frame = imutils.rotate(frame, ratio_rotate)

        height,width,channels = frame.shape
        indexes, boxes, confidences, class_ids = processing_image(frame, outputLayers, height, width)
        frame, dem_cham, dem_congvao, dem_congra, dem_ic, dem_eoi,\
        dem_nutbam, dem_tu, dem_adap, dem_chipdan = draw_boxes(\
            boxes, classes, confidences, colors)

        count = check_link_kien(dem_cham, dem_congvao, dem_congra, dem_ic, dem_eoi, dem_nutbam, dem_tu, dem_adap, dem_chipdan)
        check_connect(count)

        elapsed_time = time.time() - start
        # print(elapsed_time)
        fps = frame_id/elapsed_time
        cv2.putText(frame, "FPS:"+str(round(fps, 2)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2)
        frame = cv2.resize(frame, (480, 720))
        cv2.imshow("Detect", frame)


    key = cv2.waitKey(1)
    if key == 27 or key == ord("q"): # esc or 'q' to stop
        break
    elif key == ord('a'):
        ratio_rotate = 90
    elif key == ord('d'):
        ratio_rotate = -90
    elif key == ord('s'):
        ratio_rotate = 0

cap.release()
cv2.destroyAllWindows()
