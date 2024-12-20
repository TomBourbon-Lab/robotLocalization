#!/usr/bin/python3
import rospy

from sensor_msgs.msg import NavSatFix,Imu

pub = None
ipub = None

def callback(msg):
    global pub
    msg.header.frame_id = "utm"
    pub.publish(msg)

def imucallback(msg):
    global ipub
    msg.header.frame_id = "vnav_link"
    ipub.publish(msg)




if __name__ == '__main__':

    rospy.init_node('gps2odom')

    pub = rospy.Publisher('/vectornav/GPSfix',NavSatFix, queue_size=1)
    sub = rospy.Subscriber('/vectornav/GPS', NavSatFix, callback, queue_size=1)

    ipub = rospy.Publisher('/vectornav/IMUfix',Imu, queue_size=1)
    isub = rospy.Subscriber('/vectornav/IMU', Imu, imucallback, queue_size=1)

    rospy.spin()

