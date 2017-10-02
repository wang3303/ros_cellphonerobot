import sys
import time
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
from gpiozero import AngularServo
GPIO.setmode(GPIO.BCM)

class DCmotor:
	def __init__(self,INA1,INA2,EN):
		self._INA1 = INA1
		self._INA2 = INA2
		self._EN = EN
		GPIO.setup(self._EN, GPIO.OUT)
		GPIO.setup(self._INA1, GPIO.OUT)
		GPIO.setup(self._INA2, GPIO.OUT)
		self.sleeptime=1
		self.pwm = GPIO.PWM(self._EN, 50) #50Hz
		self.pwm.start(0)
		
	def change_duty_cycle(self,duty=0):
		GPIO.output(self._EN, True)
		self.pwm.ChangeDutyCycle(duty)
		
	def close_channel(self):
		GPIO.output(self._INA1, False)
		GPIO.output(self._INA2, False)
		GPIO.output(self._EN, False)
		self.pwm.ChangeDutyCycle(0)
		
	def forward(self,dutycycle,):
		
		GPIO.output(self._INA1, True)
		GPIO.output(self._INA2, False)
		GPIO.output(self._EN, True)
		self.change_duty_cycle(dutycycle)
		
	def reverse(self,dutycycle,):
		
		GPIO.output(self._EN, True)
		GPIO.output(self._INA1, False)
		GPIO.output(self._INA2, True)
		self.change_duty_cycle(dutycycle)


	def cleanup(self):
		self.pwm.stop()
		GPIO.cleanup([self._INA2,self._INA1,self._EN])
		
class Ultrasonic():
	def __init__(self,max_distance=1, threshold_distance =0.01, echo=17, trigger=18):
		self._echo = echo
		self._trigger = trigger
		self.ultrasonic = DistanceSensor(
							echo=self._echo, 
							trigger=self._trigger,
							max_distance = max_distance,
							threshold_distance = threshold_distance
							)
	
	def request_distance(self):
		# self.ultrasonic.wait_for_in_range()
		return self.ultrasonic.distance
		
class Servo():
	def __init__(self,pin = 17, min_angle=-42, max_angle=44):
		self.servo = AngularServo(pin, min_angle, max_angle)
	
	def right(self):
		self.servo = 90
		
	def forward():
		self.servo = 0
		
	def left():
		self.servo = -90
	
def main():
	# sensor = Ultrasonic()
	# i = 0
	# while i < 100:
	# 	time.sleep(1)
	# 	print sensor.request_distance()*100
	# 	i+=1
	# GPIO.cleanup()
	motor = DCmotor(3,4,2)
	motor.reverse(0,1)
	motor.close_channel()
	try:
		while 1:
			pass
	except:
		GPIO.cleanup()
if __name__ == '__main__':
	main()
	
	
		