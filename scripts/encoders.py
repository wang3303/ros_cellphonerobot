#!/usr/bin/env python
"""
This node is for reading encoder ticks and publishes them to /ticks.
"""
import rospy
from std_msgs.msg import Bool
from random import random
from hardware import DCmotor

def get_left_ticks():
    return motor_l.request_encoder_readings()

def get_right_ticks():
    return motor_r.request_encoder_readings()

def publish():
    while not rospy.is_shutdown():
		rospy.init_node("encoders", anonymous=True)
		pub = rospy.Publisher('ticks', Bool, queue_size=10)
		
		rate = rospy.Rate(4) #4Hz
		ticks_left = Bool()
		ticks_right = Bool()
		ticks_left.data = get_left_ticks()
		ticks_right.data = get_right_ticks()
		pub.publish(ticks_left)
		pub.publish(ticks_right)
		rate.sleep()
		rospy.loginfo("Left encoder %s", ticks_left.data)
		rospy.loginfo("Right encoder %s", ticks_right.data)


if __name__ == '__main__':
    try:
        rospy.init_node('encoders', anonymous=True)
        motor = rospy.get_param("/motor")
        motor_r_pin = motor['motor_r']#rospy.get_param('/execution/'+motor[0])
        motor_l_pin = motor['motor_l']#rospy.get_param('/execution/'+motor[1])
        motor_r = DCmotor(motor_r_pin[0],motor_r_pin[1],motor_r_pin[2],motor_r_pin[3],motor_r_pin[4])
        motor_l = DCmotor(motor_l_pin[0],motor_l_pin[1],motor_l_pin[2],motor_l_pin[3],motor_l_pin[4])
        publish()
    except rospy.ROSInterruptException:
        rospy.logerr("Interrupted")
