#! /usr/bin/env python

"""
This node is created to translate cmd_vel commands into motor commands.
"""

import rospy
import time
from hardware import DCmotor
from geometry_msgs.msg import Twist

def callback(data):
    vx = data.linear.x
    vy = data.linear.y
    th = data.angular.z
    
    rospy.loginfo("I heard %s", data)
    
    # TODO Convert Twist data to motor commands after encoders are installed 
    
    motor_r.forward(70)
    motor_l.reverse(70)

def listener():
	rospy.init_node('base_controller')
	rospy.Subscriber("cmd_vel", Twist, callback)
	rospy.spin()
	
if __name__ == '__main__':
	motor = rospy.get_param("/motor")
	motor_r_pin = motor['motor_r'] #rospy.get_param('/execution/'+motor[0])
	motor_l_pin = motor['motor_l'] #rospy.get_param('/execution/'+motor[1])
	motor_r = DCmotor(motor_r_pin[0],motor_r_pin[1],motor_r_pin[2],motor_r_pin[3],motor_r_pin[4])
	motor_l = DCmotor(motor_l_pin[0],motor_l_pin[1],motor_l_pin[2],motor_l_pin[3],motor_l_pin[4])

	rospy.loginfo("Right EncoderA reading %s", motor_r_pin[3])

	listener()
