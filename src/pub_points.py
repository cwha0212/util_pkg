#!/usr/bin/env python

import rospy
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from util_pkg.msg import Point_Array

def publish_points():
    rospy.init_node('parking_lots_points', anonymous=True)
    pub = rospy.Publisher('parking_lots_points', Point_Array, queue_size=10)
    rate = rospy.Rate(10)  # 10hz
    points = [[[12.5733,-0.837072,-0.482983],[12.7407,-2.138,-0.667137],[15.3831,-2.05285,-0.549528],[15.2886,-0.593477,-0.574932]],
              [[42.8409,-10.6282,0.326171],[45.0764,-9.11807,0.347502],[44.2742,-8.09621,0.300291],[42.0251,-9.6498,0.332064]]]
    # points = [[[0,0,0],[10,0,0],[10,10,0],[0,10,0]]]
    point_array = Point_Array()
    for point in points:
        print(point)
        for p in point:
            _p = Point()
            _p.x = p[0]
            _p.y = p[1]
            _p.z = p[2]
            point_array.points.append(_p)

    while not rospy.is_shutdown():
        pub.publish(point_array)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_points()
    except rospy.ROSInterruptException:
        pass
