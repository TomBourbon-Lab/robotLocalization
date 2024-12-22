#!/usr/bin/python3
import rosbag
import rospy
import sys
from tf2_msgs.msg import TFMessage
ibag = rosbag.Bag(sys.argv[1])
obag = rosbag.Bag(sys.argv[1][0:-4]+"_reproc.bag", 'w')
count = 0
for topic, msg, ts in ibag.read_messages():
    if (topic=="/tf") or (topic=="/static_tf"):
        for t in msg.transforms:
            if t.header.frame_id=="odom":
                t.child_frame_id="base_odom"
    obag.write(topic,msg,ts)
    count += 1
    if (count%500) == 0:
        print("Processed %d messages" % count)

ibag.close()
obag.close()

