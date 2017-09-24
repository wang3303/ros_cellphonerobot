#!/usr/bin/env python

import rospy
import actionlib
from beginner_tutorials.msg import TimerResult, TimerFeedback, TimerAction, TimerGoal
import time

def client():
    act_client = actionlib.SimpleActionClient('timer', TimerAction)
    act_client.wait_for_server()
    goal = TimerGoal(time_to_wait = rospy.Duration.from_sec(9))
    act_client.send_goal(goal)
    # time.sleep(2)
    # act_client.cancel_goal()
    act_client.wait_for_result()

    rospy.loginfo('%d: Time elapsed: %.2f' % (act_client.get_state(),act_client.get_result().time_elapsed.to_sec()))

if __name__ == '__main__':
    try:
        rospy.init_node('execution')
        client()
    except rospy.ROSInterruptException,e:
        rospy.logerr(e)