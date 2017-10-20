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
    motor = rospy.get_param("/motor")
    # TODO This is based on the assumption that there are two wheels
    motor_l_pin = motor['motor_l']#rospy.get_param('/execution/'+motor[0])
    motor_r_pin = motor['motor_r']#rospy.get_param('/execution/'+motor[1])
    motor_l = DCmotor(motor_l_pin[0],motor_l_pin[1],motor_l_pin[2])
    motor_r = DCmotor(motor_r_pin[0],motor_r_pin[1],motor_r_pin[2])
        

    def forward(self,):
        self.motor_l.forward(self.dutycycle)
        self.motor_r.forward(self.dutycycle)
        rospy.loginfo('set dutycycle of +20 for both motors')

    def stop(self,):
        self.motor_l.close_channel()
        self.motor_r.close_channel()

    def left(self,):
        self.motor_l.reverse(self.dutycycle)
        self.motor_r.forward(self.dutycycle)

    def right(self,):
        self.motor_l.forward(self.dutycycle)
        self.motor_r.reverse(self.dutycycle)

    def __init__(self, name, dutycycle):
        self.dutycycle = dutycycle
        self.actionname = name
        self.act_server = actionlib.SimpleActionServer('robot', ExecutionAction, execute_cb = self.cb, auto_start = False)
        self.act_server.start()
        self.actiondic = rospy.get_param("/actiondic")
        self.functiondic = {
            'forward': self.forward,
            'stop': self.stop,
            'left': self.left,
            'right': self.right
        }
        for k, v in self.actiondic.iteritems():
            self.actiondic[k] = self.functiondic[v]
        rospy.loginfo(self.actiondic)
        rospy.loginfo('set pin number for motors'+str(self.motor_l_pin)+str(self.motor_r_pin))

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
        dutycycle = rospy.get_param('/motor/dutycycle')

        
        server = Execution(rospy.get_name(),dutycycle)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass