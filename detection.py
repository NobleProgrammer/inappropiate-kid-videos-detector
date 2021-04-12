# باسم الله، نتوكّل عليه
import cv2
import numpy as np
import os


def drawBox(img, boxes, confidences, class_ids, classes, colors, totalFrames, cwd):
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    counter = 0
    actual_boxes = []
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            actual_boxes.append([x, y, w, h])
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
            counter += 1

    if counter > 0:
        cv2.imwrite(cwd + "\\Output\\out_" + classes[0] + "/Image_" + str(totalFrames + 1) + ".jpg", img)
        return actual_boxes
    return []

def detectObject(frame, model, totalFrames):
    cwd = os.path.abspath(os.getcwd())
    net = cv2.dnn.readNet(cwd + "\\Models\\" + model + "_yolov3_training_final.weights",
                          cwd + "\\Models\\yolov3_testing.cfg")

    classes = [model]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    frame = cv2.resize(frame, None, fx=1, fy=1)
    height, width, channels = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    # End of outer for loop
    actual_boxes = drawBox(frame, boxes, confidences, class_ids, classes,
                           np.random.uniform(0, 255, size=(len(classes), 3)), totalFrames, cwd)
    if len(actual_boxes) > 0:
        return actual_boxes
    else:
        return []
