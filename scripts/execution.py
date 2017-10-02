#!/usr/bin/env python

import rospy
import actionlib
from ros_cellphonerobot.msg import ExecutionResult,ExecutionFeedback,ExecutionGoal,ExecutionAction
import time
from std_msgs.msg import String
from ros_cellphonerobot.msg import Sensors
from std_msgs.msg import Int8
mindistance = 0.8

# uint8 PENDING=0
# uint8 ACTIVE=1
# uint8 PREEMPTED=2
# uint8 SUCCEEDED=3
# uint8 ABORTED=4
# uint8 REJECTED=5
# uint8 PREEMPTING=6
# uint8 RECALLING=7
# uint8 RECALLED=8
# uint8 LOST=9

state = 1
def actioncb(msg):
    global state
    pub.publish(0)# busy
    state = 0
    act_client.wait_for_server()
    rospy.loginfo('Find exe server')
    goal = ExecutionGoal(time_to_wait=rospy.Duration.from_sec(3))
    goal.action = str(msg.data)
    act_client.send_goal(goal, feedback_cb=feedback_cb)
    # time.sleep(2)
    # act_client.cancel_goal()
    act_client.wait_for_result()
    rospy.loginfo('%d: Flag: %.2f' % (act_client.get_state(), act_client.get_result().flag))
    pub.publish(1)  # free
    state = 1

def feedback_cb(feedback):
    rospy.loginfo('Motor:Time elapsed: %.2f' % (feedback.time_elapsed.to_sec()))

def abort(msg):
    global state
    if msg.distance.range < mindistance:
        if state == 0:
            act_client.cancel_goal()
            rospy.loginfo('Range alert')
            state = 1



if __name__ == '__main__':
    try:
        rospy.init_node('execution')
        act_client = actionlib.SimpleActionClient('robot', ExecutionAction)
        rospy.Subscriber('action', String, actioncb)
        rospy.Subscriber('sensor_reading', Sensors, abort)
        pub = rospy.Publisher("flag", Int8, queue_size=10)
        time.sleep(0.)
        rospy.spin()
    except rospy.ROSInterruptException,e:
        rospy.logerr(e)