#!/usr/bin/env python

import rospy
import actionlib
import time
from ros_cellphonerobot.msg import ExecutionResult,ExecutionFeedback,ExecutionGoal,ExecutionAction
from hardware import DCmotor

class Execution(object):
    _feedback = ExecutionFeedback()
    _result = ExecutionResult()
    t0 = time.time()
    motor_l = DCmotor(3,4,2) 
    motor_r = DCmotor(17,27,22)

    def forward(self,):
        self.motor_l.forward(20)
        self.motor_r.forward(20)
    def stop(self,):
        self.motor_l.close_channel()
        self.motor_r.close_channel()

    def left(self,):
        self.motor_l.reverse(20)
        self.motor_r.forward(20)

    def right(self,):
        self.motor_l.forward(20)
        self.motor_r.reverse(20)

    def __init__(self, name):
        self.actionname = name
        self.act_server = actionlib.SimpleActionServer('robot', ExecutionAction, execute_cb = self.cb, auto_start = False)
        self.act_server.start()
        self.actiondic = {
            'w': self.forward,
            's': self.stop,
            'a': self.left,
            'd': self.right
        }

    def cb(self, goal):
        self.t0 = time.time()

        rate = rospy.Rate(2)
        # if goal does not conform to requirements
        if not goal.action in ['w','a','s','d']:
            self._result.flag = 0
            self.act_server.set_aborted(self._result, 'Abort')
            return
        self.actiondic[goal.action]() # Execute the code

        while ((time.time()-self.t0) < goal.time_to_wait.to_sec()):
            if self.act_server.is_preempt_requested():
                self._result.flag = 0
                self.stop()
                self.act_server.set_preempted(self._result, "Preempted")
                return

            self._feedback.time_elapsed = rospy.Duration.from_sec(time.time() - self.t0)
            self._feedback.time_remain = goal.time_to_wait - self._feedback.time_elapsed
            self.act_server.publish_feedback(self._feedback)

            rate.sleep()

        self.stop()
        self._result.flag = 1
        self.act_server.set_succeeded(self._result,'Succeed')


if __name__ == '__main__':
    try:
        rospy.init_node('exe_server')
        server = Execution(rospy.get_name())
        rospy.spin()
    except rospy.ROSInterruptException:
        pass