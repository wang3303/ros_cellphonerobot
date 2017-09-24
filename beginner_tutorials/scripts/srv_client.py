#!/usr/bin/env python

import sys
import rospy
from beginner_tutorials.srv import *

def cb():
    rospy.init_node('srv_client')
    rospy.wait_for_service('counter')
    try:
        srv = rospy.ServiceProxy('counter', Counter)
        request = CounterRequest(words = 'one two three')
        res = srv(request)
        print res.count
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


if __name__ == "__main__":
    cb()