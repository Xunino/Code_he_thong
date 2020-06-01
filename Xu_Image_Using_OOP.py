import cv2
import numpy as np
import time
import imutils


class yolov3(object):

    def __init__(self, weights, config, classes_path, frame, height, width):
        self.weights = weights
        self.config = config
        self.classes_path = classes_path
        self.frame = frame
        self.height = height
        self.width = width
        self.confidences = []
        self.class_ids = []
        self.boxes = []
        self.classes = []
        self.colors = []
        self.scale = 0.00392
        self.input_shape = 608
        self.processing_image()
        self.load_classes()


    def load_classes(self):
        with open(self.classes_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def processing_image(self):
        print("[INFO] Processing image....")

        net = cv2.dnn.readNet(self.weights, self.config)
        layer_names = net.getLayerNames()
        outputLayers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]

        blod = cv2.dnn.blobFromImage(self.frame, self.scale, (self.input_shape, self.input_shape), (0, 0, 0), True, crop=False)
        net.setInput(blod)
        # print(net)
        outs = net.forward(outputLayers)
        # print(outs)

        class_ids = self.class_ids
        confidences = self.confidences
        boxes = self.boxes
        for out in outs:
            # print(out)
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                # print(class_id)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0]*self.width)
                    center_y = int(detection[1]*self.height)
                    w = int(detection[2]*self.width)
                    h = int(detection[3]*self.height)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        self.indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)


    def draw_boxes(self):
        for i in range(len(self.boxes)):
            if i in self.indexes:
                x, y, w, h = self.boxes[i]
                label = self.classes[self.class_ids[i]]
                confidence = self.confidences[i]
                color = self.colors[self.class_ids[i]]

                cv2.rectangle(self.frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(self.frame, label + " " + str(round(confidence, 2)), (x + 1, y + 1), cv2.FONT_HERSHEY_PLAIN, 1,
                            (255, 255, 255), 2)
        return self.frame


if __name__ == "__main__":
    weights = "./models/weights/yolov3.weights"
    config = "./models/configs/yolov3-spp3_608.cfg"
    classes_path = "./data/labels/classes_full.names"
    video_path = "./data/videos/test1.mp4"
    image_path = "data\\images\\test10.jpg"

    image = cv2.imread(image_path)

    height, width, channels = image.shape
    check = yolov3(frame=image, weights=weights, config=config, classes_path=classes_path, height=height, width=width)

    frame = check.draw_boxes()
    # frame = cv2.resize(frame, (480, 720))
    # cv2.imshow("image", frame)
    cv2.imwrite("Detected_image.jpg", frame)
    # cv2.waitKey(0)