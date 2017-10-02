import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

pwm = GPIO.PWM(03, 50)  # pin #3 at 50Hz
pwm.start(0)


def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(03, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(03, False)
    pwm.ChangeDutyCycle(0)


SetAngle(90)
pwm.stop()
GPIO.cleanup()
