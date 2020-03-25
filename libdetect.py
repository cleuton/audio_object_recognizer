import numpy as np
import os,sys
import json
from gtts import gTTS
import vlc
import cv2


## I know... it's hardcoded!
yolo_files = "./yolo"

confidence_threshold = 0.5
threshold = 0.3

with open('./trad.json') as f:
  dicionario = json.load(f)

labelsPath = os.path.join(yolo_files, "coco.names")
LABELS = open(labelsPath).read().strip().split("\n")

np.random.seed(87)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), \
	dtype="uint8")

weightsPath = os.path.join(yolo_files, "yolov3.weights")
configPath = os.path.join(yolo_files, "yolov3.cfg")

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

def count_object(object_name,objects_list):
    if object_name in objects_list:
        counter = objects_list.get(object_name)
        counter = counter + 1
        objects_list[object_name] = counter
    else:
        objects_list[object_name] = 1

# Receive an OpenCV image and return the text of the object's list
def detect(image):
    objects_list = {}
    (H, W) = image.shape[:2]

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidence_threshold:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, threshold)

    

    if len(idxs) > 0:
        for i in idxs.flatten():
            count_object(LABELS[classIDs[i]], objects_list)

    texto = "encontrei "
    for i, (nome, contagem) in enumerate(objects_list.items()):
        print(nome,contagem)
        texto = texto + " " + str(contagem) + " "
        obj = dicionario[nome]
        if contagem < 2: 
            texto = texto + obj[0]
        else:
            texto = texto + obj[1]
    return texto
