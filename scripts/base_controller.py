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
    
    motor_rf.forward(70)
    motor_lf.reverse(70)
    motor_rb.forward(70)
    motor_lb.reverse(70)

def listener():
	rospy.init_node('base_controller')
	rospy.Subscriber("cmd_vel", Twist, callback)
	rospy.spin()
	
if __name__ == '__main__':
	motor = rospy.get_param("/motor")
	motor_rf_pin = motor['motor_rf'] #rospy.get_param('/execution/'+motor[0])
	motor_lf_pin = motor['motor_lf'] #rospy.get_param('/execution/'+motor[1])
	motor_rb_pin = motor['motor_rb'] #rospy.get_param('/execution/'+motor[2])
	motor_lb_pin = motor['motor_lb'] #rospy.get_param('/execution/'+motor[3])
	motor_rf = DCmotor(motor_rf_pin[0],motor_rf_pin[1],motor_rf_pin[2])
	motor_lf = DCmotor(motor_lf_pin[0],motor_lf_pin[1],motor_lf_pin[2])
	motor_rb = DCmotor(motor_rb_pin[0],motor_rb_pin[1],motor_rb_pin[2])
	motor_lb = DCmotor(motor_lb_pin[0],motor_lb_pin[1],motor_lb_pin[2])
	
	listener()
