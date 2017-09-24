#! /usr/bin/env python

import rospy
from beginner_tutorials.srv import Counter,CounterResponse

def count_words(request):
    return CounterResponse(len(request.words.split()))

rospy.init_node('srv_server')

service = rospy.Service('counter',Counter,count_words)

rospy.spin()