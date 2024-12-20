#!/usr/bin/env python3  

import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('fixed_tf_broadcaster')

    listener = tf.TransformListener()

    rate = rospy.Rate(1.0)
    rospy.loginfo("Waiting for initial utm to odom transform")
    while not rospy.is_shutdown():        
        try:
            try:
                    (trans,rot) = listener.lookupTransform("utm", "odom", rospy.Time(0))
                    break
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            rate.sleep()
        except rospy.exceptions.ROSTimeMovedBackwardsException:
            pass
        
        

    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    tlast = rospy.Time.now()
    rospy.loginfo("Initial offset: %f,%f,%f"%(trans[0],trans[1],trans[2]))

    while not rospy.is_shutdown():
        try:
            t = rospy.Time.now()
            if t != tlast:
                br.sendTransform((trans[0],trans[1],trans[2]),
                                (0.0, 0.0, 0.0, 1.0),
                                t,"utm_zero","utm")
                tlast = t
            rate.sleep()
        except rospy.exceptions.ROSTimeMovedBackwardsException:
            pass