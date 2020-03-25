import RPi.GPIO as GPIO
import time
import picamera
from picamera.array import PiRGBArray
import libdetect
from gtts import gTTS
import vlc

# Set the GPIOS
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO_TRIGGER = 17
GPIO_ECHO = 27
GPIO.setup(25,GPIO.IN, pull_up_down=GPIO.PUD_UP) # Switch da câmera
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
camera = picamera.PiCamera()
rawCapture = PiRGBArray(camera)

def calc_distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        #print(GPIO.input(GPIO_ECHO))
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


def wait_photo(d):
    # Check button:
    input_state = GPIO.input(25)
    if input_state == 0:
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        print("Photo! Distance:",d)
        texto = libdetect.detect(image) + " distância: " + str(d) + " centímetros."
        tts = gTTS(texto, lang='pt')
        tts.save("text.mp3")
        p = vlc.MediaPlayer("./text.mp3")
        p.play()
        time.sleep(0.2)

while (True):
    dist = calc_distance()
    #print ("Measured Distance = %.1f cm" % dist)  
    wait_photo(dist)        