#!/usr/bin/env python

import rospy
from ros_cellphonerobot.msg import Sensors
from sensor_msgs.msg import Range

def cb(msg):
    global sensor_readings
    message = Sensors()
    message = sensor_readings
    message.distance = msg
    pub.publish(message)
    rospy.loginfo("Update distance")

# def cb1(msg):
#     global sensor_readings
#     message = Sensors()
#     message = sensor_readings
#     message.distance = msg
#     message.distance.radiation_type = 1
#     pub.publish(message)
#     rospy.loginfo("Update distance11")

if __name__ == '__main__':
    try:
        sensor_readings = Sensors()
        rospy.init_node("sensor_hub", anonymous=True)
        rospy.Subscriber("distance", Range ,cb)
        # rospy.Subscriber("distance1", Range, cb1)
        pub = rospy.Publisher("sensor_reading", Sensors, queue_size=10)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass
