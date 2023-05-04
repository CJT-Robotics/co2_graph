cmake_minimum_required(VERSION 3.0.2)
project(co2_graph)

find_package(catkin REQUIRED COMPONENTS
  joy_relay
  roscpp
  rospy
  std_msgs
)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)