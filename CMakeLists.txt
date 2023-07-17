cmake_minimum_required(VERSION 3.0.2)
project(util_pkg)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
  geometry_msgs
)

add_message_files(
  FILES
  Point_Array.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs  # Or other packages containing msgs
  geometry_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES project
#  CATKIN_DEPENDS rospy
#  DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  src/pose_extraction.py
  src/pub_marker.py
  src/pub_points.py
  src/parking_detection.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)