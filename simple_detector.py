import numpy as np
import argparse
import time
import cv2
import os,sys
import json
from gtts import gTTS
import vlc

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

if len(sys.argv) < 2:
    image = cv2.imread("./images/teste2.jpg")
else:
    image = cv2.imread(sys.argv[1])

(H, W) = image.shape[:2]

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
	swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
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

objects_list = {}

def count_object(object_name):
    global objects_list
    if object_name in objects_list:
        counter = objects_list.get(object_name)
        counter = counter + 1
        objects_list[object_name] = counter
    else:
        objects_list[object_name] = 1


if len(idxs) > 0:
    for i in idxs.flatten():
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        color = [int(c) for c in COLORS[classIDs[i]]]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 4)
        text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.8, color, 3)
        count_object(LABELS[classIDs[i]])

cv2.imshow("Image", image)
texto = "encontrei "
for i, (nome, contagem) in enumerate(objects_list.items()):
    print(nome,contagem)
    texto = texto + " " + str(contagem) + " "
    obj = dicionario[nome]
    if contagem < 2: 
        texto = texto + obj[0]
    else:
        texto = texto + obj[1]
print(texto)
tts = gTTS(texto, lang='pt')
tts.save("text.mp3")
p = vlc.MediaPlayer("./text.mp3")
p.play()
cv2.waitKey(0)