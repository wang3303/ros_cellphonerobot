#! /usr/bin/env python

"""
This node is created to translate cmd_vel commands into motor commands.
"""

import rospy
import time
from hardware import DCmotor

if __name__ == '__main__':
	rospy.init_node('base_controller')
	
	motor = rospy.get_param("/motor")
	motor_rf_pin = motor['motor_rf']#rospy.get_param('/execution/'+motor[0])
    motor_lf_pin = motor['motor_lf']#rospy.get_param('/execution/'+motor[1])
    motor_rb_pin = motor['motor_rb']#rospy.get_param('/execution/'+motor[2])
    motor_lb_pin = motor['motor_lb']#rospy.get_param('/execution/'+motor[3])  
    motor_rf = DCmotor(motor_rf_pin[0],motor_rf_pin[1],motor_rf_pin[2])
    motor_lf = DCmotor(motor_lf_pin[0],motor_lf_pin[1],motor_lf_pin[2])
    motor_rb = DCmotor(motor_rb_pin[0],motor_rb_pin[1],motor_rb_pin[2])
    motor_lb = DCmotor(motor_lb_pin[0],motor_lb_pin[1],motor_lb_pin[2])
	
	self.motor_rf.forward(70)
    self.motor_lf.reverse(70)
    self.motor_rb.forward(70)
    self.motor_lb.reverse(70)
    
    rospy.spin()
