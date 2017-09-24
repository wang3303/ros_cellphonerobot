#!/usr/bin/env python

import rospy
import actionlib
import time
from beginner_tutorials.msg import TimerAction, TimerGoal, TimerFeedback, TimerResult

class forward(object):
    _feedback = TimerFeedback()
    _result = TimerResult()
    t0 = time.time()

    def __init__(self, name):
        self.actionname = name
        self.act_server = actionlib.SimpleActionServer('timer', TimerAction, execute_cb = self.cb, auto_start = False)
        self.act_server.start()

    def cb(self, goal):
        self.t0 = time.time()

        rate = rospy.Rate(2)
        # if goal does not conform to requirements
        self._result.update = 0
        if goal.time_to_wait.to_sec() > 10:
            self._result.time_elapsed = rospy.Duration.from_sec(time.time() - self.t0)
            self.update = 0
            self.act_server.set_aborted(self._result, 'Abort')
            return

        while ((time.time()-self.t0) < goal.time_to_wait.to_sec()):
            if self.act_server.is_preempt_requested():
                self._result.time_elapsed = rospy.Duration.from_sec(time.time() - self.t0)
                self.act_server.set_preempted(self._result, "Preempted")
                return

            self._feedback.time_elapsed = rospy.Duration.from_sec(time.time() - self.t0)
            self._feedback.time_remain = goal.time_to_wait - self._feedback.time_elapsed
            self._result.update +=1
            self.act_server.publish_feedback(self._feedback)

            rate.sleep()

        self._result.time_elapsed = rospy.Duration.from_sec(time.time() - self.t0)
        self.act_server.set_succeeded(self._result,'Succeed')


if __name__ == '__main__':
    try:
        rospy.init_node('forward_server')
        server = forward(rospy.get_name())
        rospy.spin()
    except rospy.ROSInterruptException:
        pass