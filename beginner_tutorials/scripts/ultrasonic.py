#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Range
from random import random

def get_distance():
    return random()

def publish():
    while not rospy.is_shutdown():
        pub = rospy.Publisher("distance", Range, queue_size=10)
        rospy.init_node("ultrasonic", anonymous=True)

        rate = rospy.Rate(10) #10Hz
        msg = Range(radiation_type = 0)
        ## ULTRASOUND = 0
        ## IR = 1
        msg.range = get_distance()
        msg.min_range = 0
        msg.max_range = 30
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo("%.2f" % (msg.range))


if __name__ == '__main__':
    try:
        publish()
    except rospy.ROSInterruptException:
        rospy.logerr("Interrupted")
