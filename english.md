# Object recognizer

[**Cleuton Sampaio**](https://github.com/cleuton)

[![](./banner_livros2.png)](https://www.lcm.com.br/site/#livros/busca?term=cleuton)

Click on the image for a video presentation:

[![](./results.jpg)](https://youtu.be/eVmNh9URYuU)

I am developing a device to recognize objects ahead, say their names and also inform the distance to the nearest object. The idea is to create something that works for people with visual difficulties.

Whether it's going to be an embedded device (a Raspberry etc) or just a mobile app, I still don't know. But I am selecting and testing several models. In this demo, I'm using Yolo (You Only Look Once), with python and OpenCV. I was inspired by the article by [**Adrian Rosebrock**](https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/) to create this PoC.

I've tested with CNN models in Keras, using banks like [**CIFAR**](https://www.cs.toronto.edu/~kriz/cifar.html) and [**COCODataset**](http : //cocodataset.org/#home), but Yolo's performance is better, although less accurate.

It is still an unfinished project, but I decided to share it for you to help me and develop your own solutions.

I'm using Google's [**gTTS**](https://gtts.readthedocs.io/en/latest/) library to transcribe text to audio.

## Setup

Clone the Darknet project (git clone https://github.com/pjreddie/darknet) and copy following files to  **yolo** folder: 
- darknet/cfg/yolov3.cfg
- darknet/data/coco.names

Click [**on this link**](https://pjreddie.com/media/files/yolov3.weights) and download the yolov3.weights file and save it in the  **yolo** folder.

Install [**VLC**](https://www.videolan.org/vlc/). It is better if you have [**Anaconda**](https://anaconda.org/) also installed, just create a virtual environment with the command:

```
conda env create -f ./env.yml
conda activate object
```

To execute, just run the script [**simple_detector.py**]:

```
python simple_detector.py
```

If you want, you can pass the path of an image file to test. I attached 2 images for you to test.

Oh, and I created a JSON Dictionary to translate the names of the objects found (to Portuguese), but if you are an english speaker, just use the original names.




