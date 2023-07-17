#!/usr/bin/env python2

import rospy
import numpy as np
from nav_msgs.msg import Odometry
pose_data = []
def callback(data):
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    z = data.pose.pose.position.z
    q_w = data.pose.pose.orientation.w
    q_x = data.pose.pose.orientation.x
    q_y = data.pose.pose.orientation.y
    q_z = data.pose.pose.orientation.z
    r00 = 2 * (q_w * q_w + q_x * q_x) - 1
    r01 = 2 * (q_x * q_y - q_w * q_z)
    r02 = 2 * (q_x * q_z + q_w * q_y)
    r03 = x

    r10 = 2 * (q_x * q_y + q_w * q_z)
    r11 = 2 * (q_w * q_w + q_y * q_y) - 1
    r12 = 2 * (q_y * q_z - q_w * q_x)
    r13 = y

    r20 = 2 * (q_x * q_z - q_w * q_y)
    r21 = 2 * (q_y * q_z + q_w * q_x)
    r22 = 2 * (q_w * q_w + q_z * q_z) - 1
    r23 = z
    pose_data.append(str(r00)+" "+str(r01)+" "+str(r02)+" "+str(r03)+" "+str(r10)+" "+str(r11)+" "+str(r12)+" "+str(r13)+" "+str(r20)+" "+str(r21)+" "+str(r22)+" "+str(r23))
    print(r13)

rospy.init_node("pose_extraction")
pub = rospy.Subscriber("/Odometry", Odometry, callback)

rospy.spin()
f = open("/home/chang/poses.txt","w")

for i in pose_data:
    f.write(i)
    f.write("\n")
