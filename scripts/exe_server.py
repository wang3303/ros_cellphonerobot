#!/usr/bin/env python
"""
This is the execution server waiting for the execution.py
sending execution requests. It will handle all kinds of situation
including wrong commands, client abortion, executing correct commands.
The list of executable commands is read from parameter server and then
matched to defined member functions.
"""

import rospy
import actionlib
import time
from ros_cellphonerobot.msg import ExecutionResult,ExecutionFeedback,ExecutionGoal,ExecutionAction
from hardware import DCmotor
from random import randint

class Execution(object):
    _feedback = ExecutionFeedback()
    _result = ExecutionResult()
    t0 = time.time()
    motor = rospy.get_param("/motor")
    # TODO This is based on the assumption that there are two wheels
    motor_rf_pin = motor['motor_rf']#rospy.get_param('/execution/'+motor[0])
    motor_lf_pin = motor['motor_lf']#rospy.get_param('/execution/'+motor[1])
    motor_rb_pin = motor['motor_rb']#rospy.get_param('/execution/'+motor[2])
    motor_lb_pin = motor['motor_lb']#rospy.get_param('/execution/'+motor[3])
    
    motor_rf = DCmotor(motor_rf_pin[0],motor_rf_pin[1],motor_rf_pin[2])
    motor_lf = DCmotor(motor_lf_pin[0],motor_lf_pin[1],motor_lf_pin[2])
    motor_rb = DCmotor(motor_rb_pin[0],motor_rb_pin[1],motor_rb_pin[2])
    motor_lb = DCmotor(motor_lb_pin[0],motor_lb_pin[1],motor_lb_pin[2])

        
    # TODO Define the self defined functions mentioned in profile.yaml as below
    def freestyle(self,):
        i = randint(0,1)
        rospy.loginfo('selection is '+str(i))
        motion = [
            self.left,
            self.right
        ]
        motion[i]()
        self.forward()

    def forward(self,):
        self.motor_rf.forward(self.dutycycle)
        self.motor_lf.reverse(self.dutycycle)
        
        self.motor_rb.forward(self.dutycycle)
        self.motor_lb.reverse(self.dutycycle)
        
        rospy.loginfo('set dutycycle of +20 for both motors')

    def stop(self,):
        self.motor_rf.close_channel()
        self.motor_lf.close_channel()
        
        self.motor_rb.close_channel()
        self.motor_lb.close_channel()

    def left(self,):
        self.motor_rf.forward(self.dutycycle)
        self.motor_lf.forward(self.dutycycle)
        
        self.motor_rb.forward(self.dutycycle)
        self.motor_lb.forward(self.dutycycle)
        
        time.sleep(randint(0,2))

    def right(self,):
        self.motor_rf.reverse(self.dutycycle)
        self.motor_lf.reverse(self.dutycycle)
        
        self.motor_rb.reverse(self.dutycycle)
        self.motor_lb.reverse(self.dutycycle)
        
        time.sleep(randint(0,2))

    def __init__(self, name, dutycycle):
        self.dutycycle = dutycycle
        self.actionname = name
        self.act_server = actionlib.SimpleActionServer('robot', ExecutionAction, execute_cb = self.cb, auto_start = False)
        self.act_server.start()
        self.actiondic = rospy.get_param("/actiondic")
        self.command = []
        # Put your defined function names in the functiondic in the format
        # {'name'(in the profile.yaml): self.function_name,...}
        self.functiondic = {
            'forward': self.forward,
            'stop': self.stop,
            'left': self.left,
            'right': self.right,
            'freestyle': self.freestyle
        }
        # Then we will match member function with the commands published on Topic "/action"
        for k, v in self.actiondic.iteritems():
            self.actiondic[k] = self.functiondic[v]
            self.command.append(k)
        rospy.loginfo(self.actiondic)
        #rospy.loginfo('set pin number for motors'+str(self.motor_l_pin)+str(self.motor_r_pin))

    def cb(self, goal):
        self.t0 = time.time()

        rate = rospy.Rate(2)
        # if goal does not conform to requirements
        if not goal.action in self.command:
            self._result.flag = 0
            self.act_server.set_aborted(self._result, 'Abort')
            return
        self.actiondic[goal.action]() # Execute the code

        update_counter = 0
        update_period = 3 #update state every 3 seconds

        while ((time.time()-self.t0) < goal.time_to_wait.to_sec()):
            
            if self.act_server.is_preempt_requested():
                self._result.flag = 0
                self.stop()
                self.act_server.set_preempted(self._result, "Preempted")
                return
            if int((time.time()-self.t0) / update_period) > update_counter: #update state every 3 seconds
                self.actiondic[goal.action]()
                update_counter +=1
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
        # Get parameters from profile.yaml
        dutycycle = rospy.get_param('/motor/dutycycle')
        server = Execution(rospy.get_name(),dutycycle)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
