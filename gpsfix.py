#!/usr/bin/python3
import rospy

from sensor_msgs.msg import NavSatFix,Imu
from nav_msgs.msg import Odometry
import copy

pub = None
ipub = None
opub = None
o_init = None

def callback(msg):
    global pub
    msg.header.frame_id = "utm_ned"
    pub.publish(msg)

def imucallback(msg):
    global ipub
    msg.header.frame_id = "vnav_link"
    ipub.publish(msg)

def odomcallback(msg):
    global opub, o_init
    msg.header.frame_id = "utm_zero_ned"
    msg.child_frame_id = "base_link"
    if o_init is None:
        o_init = copy.deepcopy(msg.pose.pose.position)
        rospy.loginfo("odomfix initialised to "+str(o_init))
    msg.pose.pose.position.x -= o_init.x
    msg.pose.pose.position.y -= o_init.y
    msg.pose.pose.position.z -= o_init.z
    opub.publish(msg)




if __name__ == '__main__':

    rospy.init_node('gps2odom')

    pub = rospy.Publisher('/vectornav/xGPSfix',NavSatFix, queue_size=1)
    sub = rospy.Subscriber('/vectornav/GPS', NavSatFix, callback, queue_size=1)

    ipub = rospy.Publisher('/vectornav/xIMUfix',Imu, queue_size=1)
    isub = rospy.Subscriber('/vectornav/IMU', Imu, imucallback, queue_size=1)

    opub = rospy.Publisher('/vectornav/Odomfix',Odometry, queue_size=1)
    #osub = rospy.Subscriber('/warthog_velocity_controller/odom', Odometry, odomcallback, queue_size=1)
    osub = rospy.Subscriber('/vectornav/odom', Odometry, odomcallback, queue_size=1)

    rospy.spin()

