import cv2
import numpy as np
import time
# import imutils


class yolov3(object):

    def __init__(self, weights, config, classes_path):
        self.weights = weights
        self.config = config
        self.classes_path = classes_path
        self.count = 0
        self.scale = 0.00392
        self.input_shape = 416
        self.score_threshold = 0.3
        self.nms_threshold = 0.3
        self.load_classes()


    def load_classes(self):
        with open(self.classes_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))


    def processing_image(self, frame):
        print("[INFO] Processing....")
        time_start = time.time()
        count = self.count + 1

        height, width = frame.shape[:2]

        net = cv2.dnn.readNet(self.weights, self.config)
        layer_names = net.getLayerNames()
        outputLayers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]

        blod = cv2.dnn.blobFromImage(frame, self.scale, (self.input_shape, self.input_shape), (0, 0, 0), True, crop=False)
        net.setInput(blod)
        outs = net.forward(outputLayers)

        self.class_ids = []
        self.confidences = []
        self.boxes = []
        for out in outs:
            # print(out)
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                # print(class_id)
                confidence = scores[class_id]
                if confidence > 0.2:
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    self.boxes.append([x, y, w, h])
                    self.confidences.append(float(confidence))
                    self.class_ids.append(class_id)
        end_time = time.time() - time_start
        self.FPS = count/end_time
        self.indexes = cv2.dnn.NMSBoxes(self.boxes, self.confidences, score_threshold=self.score_threshold, nms_threshold=self.nms_threshold)


    def draw_boxes(self, frame):
        colors = self.colors
        for i in range(len(self.boxes)):
            if i in self.indexes:
                x, y, w, h = self.boxes[i]
                label = self.classes[self.class_ids[i]]
                confidence = self.confidences[i]
                color = colors[self.class_ids[i]]
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x + 1, y + 1), cv2.FONT_HERSHEY_PLAIN, 1,
                            (255, 255, 255), 2)
                cv2.putText(frame, "FPS: " + str(round(self.FPS, 2)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 255, 255), 2)
        return frame


if __name__ == "__main__":
    weights = "models/weights/yolov3-spp3_95_50.weights"
    config = "models/configs/prune_95_50.cfg"
    classes_path = "data/classes/classes_full.names"
    # video_path = "data/videos/test1.mp4"
    image_path = "data/images/test7.jpg"
    video_path = 0

    start = yolov3(weights=weights, config=config, classes_path=classes_path)
    cap = cv2.VideoCapture(video_path)


    if video_path != 0:
        while True:
            ret, frame = cap.read()
            if ret:
                start.processing_image(frame)
                frame = start.draw_boxes(frame)
                frame = cv2.resize(frame, (480, 720))
                cv2.imshow("Detected", frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

    else:
        image = cv2.imread(image_path)
        start.processing_image(image)
        image = start.draw_boxes(image)
        cv2.imwrite("Detected_image.jpg", image)
        image = cv2.resize(image, (480, 720))
        cv2.imshow("Detected", image)
        cv2.waitKey(0)
