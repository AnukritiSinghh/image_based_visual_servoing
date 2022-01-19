# visual-servoing-toolkit

Visual servoing codes for matlab and python.
Includes gazebo integration.


* note: Currently only Python scipts are supported.

### Requires:
1. libgazebo_ros_openni_kinect
2. opencv-contrib (pip2 install opencv-contrib-python==3.3.1.11, Note: uninstall existing opencv-python first.)

### Installation:
* just copy the floder in your catkin workspace, do catkin_make and source devel/setup.bash

### Demo:

#### IBVS with Aruco marker:
  1. 'roslaunch visual_servoing free_cam_aruco_marker.launch'
  2. in another terminal: 'roscd visual_servoing/scripts/python/examples/'
  3. 'python2 ibvs_aruco.py'

### Tested with:
1. Ubuntu 16.04
2. ROS Kinetic
3. Gazebo 7.0.0
4. Python 2.7 
5. opencv-contrib-python 3.3.1.11
