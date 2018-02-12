#!/usr/bin/env python
"""
This node is for reading encoder ticks and publishes them to /ticks.
"""
import rospy
from std_msgs.msg import Bool
from std_msgs.msg import Int32
from random import random
from hardware import DCmotor

def get_right_ticks():
	return motor_r.request_encoder_ticks()

def get_left_ticks():
	return motor_l.request_encoder_ticks()

def publish():
    while not rospy.is_shutdown():
		rospy.init_node("encoders", anonymous=True)
		pub_tick = rospy.Publisher('ticks', Int32, queue_size=10)
		
		rate = rospy.Rate(4) #4Hz
		right_ticks = Int32()
		left_ticks = Int32()
		right_ticks.data = get_right_ticks()
		left_ticks.data = get_left_ticks()
		
		pub_tick.publish(left_ticks)
		pub_tick.publish(right_ticks)
		
		rate.sleep()
		rospy.loginfo("Left encoder A = %s", left_ticks.data)
		rospy.loginfo("Right encoder A = %s", right_ticks.data)

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
