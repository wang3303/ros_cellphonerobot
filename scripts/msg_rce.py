#!/usr/bin/env python

import rospy
from beginner_tutorials.msg import Complex

def cb(msg):
    rospy.loginfo("(%.2f, %.2f)" % (msg.real,msg.img))

if __name__ == '__main__':
    try:
        rospy.init_node("cnumber_listen", anonymous=True)
        rospy.Subscriber("cnumber",Complex,cb)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass