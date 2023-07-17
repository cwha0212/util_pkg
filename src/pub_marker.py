#!/usr/bin/env python

import rospy
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from util_pkg.msg import Point_Array

def publish_markers(data):
    pub = rospy.Publisher('parking_lots', MarkerArray, queue_size=10)
    rate = rospy.Rate(10)  # 10hz
    i = 0
    points=[]
    _p_array = []
    for point in data.points:
        _p = []
        _p.append(point.x)
        _p.append(point.y)
        _p.append(point.z)
        _p_array.append(_p)
        i += 1
        if i == 4 :
            points.append(_p_array)
            _p_array = []
            i = 0
    markers = MarkerArray()
    i = 0
    for point in points:
        marker = Marker()
        marker.header.frame_id = "map"
        marker.type = marker.LINE_LIST
        marker.action = marker.ADD
        marker.id = i
        i = i+1
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 0.0
        marker.color.b = 1.0
        p_list = []
        for p in point:
            _p = Point()
            _p.x = p[0]
            _p.y = p[1]
            _p.z = p[2]
            p_list.append(_p)
        marker.points.append(p_list[0])
        marker.points.append(p_list[1])
        marker.points.append(p_list[1])
        marker.points.append(p_list[2])
        marker.points.append(p_list[2])
        marker.points.append(p_list[3])
        marker.points.append(p_list[3])
        marker.points.append(p_list[0])
        markers.markers.append(marker)
        pub.publish(markers)



if __name__ == '__main__':
    try:
        rospy.init_node('parking_lots', anonymous=True)
        sub = rospy.Subscriber('/parking_lots_points', Point_Array, publish_markers)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
