#!/usr/bin/env python

import rospy
from beginner_tutorials.msg import Complex
from random import random

def publish():

    while not rospy.is_shutdown():
        pub = rospy.Publisher("cnumber", Complex,queue_size=10)
        rospy.init_node("pub", anonymous=True)

        rate = rospy.Rate(2) #2Hz
        msg = Complex(real = random(), img = random())

        pub.publish(msg)
        rate.sleep()
        rospy.loginfo("(%.2f, %.2f)" % (msg.real,msg.img))


if __name__ == '__main__':
    try:
        publish()
    except rospy.ROSInterruptException:
        rospy.logerr("Interrupted")
