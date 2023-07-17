import rospy
import struct
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
from util_pkg.msg import Point_Array
from nav_msgs.msg import Odometry
import numpy as np

rospy.init_node('parking_detection')
pub1 = rospy.Publisher('/legal',PointCloud2, queue_size=100)
pub2 = rospy.Publisher('/illegal',PointCloud2, queue_size=100)
# points_of_parking_lots = [[[0,0],[10,0],[10,10],[0,10],[0,0]]]
points_of_parking_lots = []
parking_lots_is = 0
R = [[1,0,0,0],
     [0,1,0,0],
     [0,0,1,0],
     [0,0,0,1]]

fields = [PointField('x', 0, PointField.FLOAT32, 1),
          PointField('y', 4, PointField.FLOAT32, 1),
          PointField('z', 8, PointField.FLOAT32, 1),
          PointField('rgba', 16, PointField.UINT32, 1),
          ]

def inside_or_outside(polygon, point):
    N = len(polygon)-1
    counter = 0
    p1 = polygon[0]
    for i in range(1, N+1):
        p2 = polygon[i%N]
        if point[1] > min(p1[1], p2[1]) and point[1] <= max(p1[1], p2[1]) and point[0] <= max(p1[0], p2[0]) and p1[1] != p2[1]:
            xinters = (point[1]-p1[1])*(p2[0]-p1[0])/(p2[1]-p1[1]) + p1[0]
            if(p1[0]==p2[0] or point[0]<=xinters):
                counter += 1
        p1 = p2 
    if counter % 2 == 0:
        res = False
    else:
        res = True
    return res

def point_array_callback(msg):
    global parking_lots_is
    i = 0
    _p_array = []
    if parking_lots_is == 0:
      for point in msg.points:
          _p = []
          _p.append(point.x)
          _p.append(point.y)
          _p.append(point.z)
          _p_array.append(_p)
          i += 1
          if i == 4 :
              _p_array.append(_p_array[0])
              points_of_parking_lots.append(_p_array)
              _p_array = []
              i = 0
      parking_lots_is = 1

def pointcloud_callback(msg):
    xyz = []
    legal_boards = []
    illegal_boards = []
    for data in pc2.read_points(msg, field_names=("x","y","z",), skip_nans=True):
        xyz.append([data[0], data[1], data[2], 1])
    # for polygon in points_of_parking_lots:
    #     for i,_point in enumerate(xyz):
    #       cloud_x = xyz[i][0]
    #       cloud_y = xyz[i][1]
    #       cloud_z = xyz[i][2]
    #       a = 255
    #       if inside_or_outside(polygon, _point):
    #         cloud_r = 100
    #         cloud_g = 255
    #         cloud_b = 0
    #         rgb = struct.unpack('I', struct.pack('BBBB', cloud_b, cloud_g, cloud_r, a))[0]
    #         pt = [cloud_x, cloud_y, cloud_z, rgb]
    #         legal_boards.append(pt)
    #       else :
    #         cloud_r = 255
    #         cloud_g = 0
    #         cloud_b = 0
    #         rgb = struct.unpack('I', struct.pack('BBBB', cloud_b, cloud_g, cloud_r, a))[0]
    #         pt = [cloud_x, cloud_y, cloud_z, rgb]
    #         illegal_boards.append(pt)
    for i,_point in enumerate(xyz):
        cloud_x = xyz[i][0]
        cloud_y = xyz[i][1]
        cloud_z = xyz[i][2]
        cloud_r = 255
        cloud_g = 0
        cloud_b = 0
        a = 255
        for polygon in points_of_parking_lots:
            if inside_or_outside(polygon, _point):
                cloud_r = 100
                cloud_g = 255
                cloud_b = 0
                rgb = struct.unpack('I', struct.pack('BBBB', cloud_b, cloud_g, cloud_r, a))[0]
                pt = [cloud_x, cloud_y, cloud_z, rgb]
                legal_boards.append(pt)
                break
            else :
                continue
        if cloud_r == 255 :
            rgb = struct.unpack('I', struct.pack('BBBB', cloud_b, cloud_g, cloud_r, a))[0]
            pt = [cloud_x, cloud_y, cloud_z, rgb]
            illegal_boards.append(pt)
    header = Header()
    header.frame_id = "map"
    legal = pc2.create_cloud(header, fields, legal_boards)
    illegal = pc2.create_cloud(header, fields, illegal_boards)
    pub1.publish(legal)
    pub2.publish(illegal)

sub1 = rospy.Subscriber('/parking_lots_points',Point_Array, point_array_callback)
sub2 = rospy.Subscriber('/kickboard', PointCloud2, pointcloud_callback)
rospy.spin()
