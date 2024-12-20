#!/usr/bin/python3
import rospy

from nav_msgs.msg import Odometry	       

import tf



utmInit=None

broadcaster = tf.TransformBroadcaster()	



#This node takes the pose in utm from the imu (internal fusion of its gps and

#imu), and creates a new frame with the origin at the location of the robot when

#the node starts, it publishes the odometry and broadcasts the tf

def utmCallback(msg):

    global utmInit, broadcaster

    if utmInit is None:

        utmInit = msg.pose.pose

        rospy.loginfo("GPS2ODOM: GPS origin set from sensor to\n" + str(utmInit))

    

    #broadcast tf to the new odom_imu frame

    p = [-utmInit.position.x, -utmInit.position.y, -utmInit.position.z]

    q = [0, 0 , 0 , 1]

    broadcaster.sendTransform(p, q, msg.header.stamp, "utm", "odom_imu")



    p = [msg.pose.pose.position.x - utmInit.position.x, msg.pose.pose.position.y - utmInit.position.y, msg.pose.pose.position.z - utmInit.position.z]

    q = [msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]

    

    #broadcast the tf from this new frame to the robot

    broadcaster.sendTransform(p, q, msg.header.stamp, "odom_imu", "imu_link")





if __name__ == '__main__':

    rospy.init_node('gps2odom')

    utmSub = rospy.Subscriber('odom', Odometry, utmCallback, queue_size=1)

    rospy.spin()

