#!/usr/bin/python3
import rospy

from nav_msgs.msg import Odometry	       
from sensor_msgs.msg import Imu

import tf



utmInit=None
imuQ=None

broadcaster = tf.TransformBroadcaster()	

def imuCallback(msg):
    global imuQ
    imuQ = msg.orientation


def utmCallback(msg):

    global utmInit, broadcaster

    if utmInit is None:

        utmInit = msg.pose.pose

        rospy.loginfo("GPS2ODOM: GPS origin set from sensor to\n" + str(utmInit))

    

    #broadcast tf to the new odom_imu frame

    p = [-utmInit.position.x, -utmInit.position.y, -utmInit.position.z]

    q = [0, 0 , 0 , 1]

    broadcaster.sendTransform(p, q, msg.header.stamp, "utm", "utm_zero")



    p = [msg.pose.pose.position.x - utmInit.position.x, msg.pose.pose.position.y - utmInit.position.y, msg.pose.pose.position.z - utmInit.position.z]

    q = [imuQ.x, imuQ.y, imuQ.z, imuQ.w]

    #broadcast the tf from this new frame to the robot

    broadcaster.sendTransform(p, q, msg.header.stamp, "utm_zero", "odom")





if __name__ == '__main__':

    rospy.init_node('gps2odom')

    utmSub = rospy.Subscriber('/utm/odom', Odometry, utmCallback, queue_size=1)
    imuSub = rospy.Subscriber('/vectornav/IMU', Imu, imuCallback, queue_size=1)

    rospy.spin()

