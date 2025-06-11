import RPi.GPIO as GPIO
import time

GPIO_NUM=17


# IF NEEDED THIS HAS TO BE INSTALLED
# sudo apt-get install python3-rpi.gpio

#TO TEST
def turn_on_via_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_NUM, GPIO.OUT)

    GPIO.output(GPIO_NUM, GPIO.HIGH)
    time.sleep(1/2)
    GPIO.output(GPIO_NUM, GPIO.LOW)

    GPIO.cleanup()
