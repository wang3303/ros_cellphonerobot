#!/usr/bin/env python

"""
This node is created to translate cmd_vel commands into motor commands.
"""

import rospy
from hardware import DCmotor
from std_msgs.msg import Float32

def leftcallback(data):
    motor_l.reverse(100)
    rospy.loginfo("Left motor reading: %s", data.data)

def rightcallback(data):
    motor_r.forward(100)
    rospy.loginfo("Right motor reading: %s", data.data)

def listener():
	rospy.init_node('motor_controller')
	rospy.Subscriber("lmotor_cmd", Float32, leftcallback)
	rospy.Subscriber("rmotor_cmd", Float32, rightcallback)
	rospy.spin()
	
if __name__ == '__main__':
	motor = rospy.get_param("/motor")
	motor_r_pin = motor['motor_r'] #rospy.get_param('/execution/'+motor[0])
	motor_l_pin = motor['motor_l'] #rospy.get_param('/execution/'+motor[1])
	motor_r = DCmotor(motor_r_pin[0],motor_r_pin[1],motor_r_pin[2],motor_r_pin[3],motor_r_pin[4])
	motor_l = DCmotor(motor_l_pin[0],motor_l_pin[1],motor_l_pin[2],motor_l_pin[3],motor_l_pin[4])

	try:
		listener()
	except rospy.ROSInterruptException:
		pass
