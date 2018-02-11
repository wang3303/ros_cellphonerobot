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
		ticks_left_A = Bool()
		ticks_left_B = Bool()
		ticks_right_A = Bool()
		ticks_right_B = Bool()
		ticks_left_A.data, ticks_left_B.data = get_left_ticks()
		ticks_right_A.data, ticks_right_B.data = get_right_ticks()
		pub.publish(ticks_left_A)
		pub.publish(ticks_left_B)
		pub.publish(ticks_right_A)
		pub.publish(ticks_right_B)
		rate.sleep()
		rospy.loginfo("Left encoder A = %s", ticks_left_A.data)
		rospy.loginfo("Left encoder B = %s", ticks_left_B.data)
		rospy.loginfo("Right encoder A = %s", ticks_right_A.data)
		rospy.loginfo("Right encoder B = %s", ticks_right_B.data)


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
