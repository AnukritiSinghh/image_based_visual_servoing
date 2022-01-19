#!/usr/bin/env python

""" cv_bridge_demo.py - Version 0.1 2011-05-29
    A ROS-to-OpenCV node that uses cv_bridge to map a ROS image topic and optionally a ROS
    depth image topic to the equivalent OpenCV image stream(s).
    
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2011 Patrick Goebel.  All rights reserved.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html
      
"""

import rospy
import sys
import cv2
from sensor_msgs.msg import Image, CameraInfo, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import numpy as np


class Kinect_subs():
    depth = None
    image = None
    K = None
    
    def __init__(self):
        self.node_name = "depth_subscriber"
        
        rospy.init_node(self.node_name)
        
        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)
        
        # Create the cv_bridge object
        self.bridge = CvBridge()
        self.depth = None
        
        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        #self.image_sub = rospy.Subscriber("/kinect_camera/depth/image_raw", Image, self.image_callback)
        self.depth_sub = rospy.Subscriber("/kinect_camera/depth/depth_image_raw", Image, self.depth_callback)
        self.image_sub = rospy.Subscriber("/kinect_camera/depth/image_raw", Image, self.image_callback)
        self.caminfo_sub = rospy.Subscriber("/kinect_camera/depth/camera_info", CameraInfo, self.caminfo_callback)
        
        rospy.loginfo("Waiting for image topics...")



    def depth_callback(self, ros_image):
        rate = rospy.Rate(10) # 10hz
        
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            # The depth image is a single-channel float32 image
            
            depth_image = self.bridge.imgmsg_to_cv2(ros_image, "passthrough")
            #depth_image_normalized = cv2.normalize(depth_image, None , 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
            self.depth = depth_image
            
            
            #delete node and give control back to main
            #rospy.signal_shutdown('done')
            
        except CvBridgeError, e:
            print e
        
    def image_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        #print 'image_callback'
        
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
            self.image = frame
        except CvBridgeError, e:
            print e
    

    def caminfo_callback(self, caminfo):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        #print 'caminfo_callback'
        
        try:
            self.K = caminfo.K
            self.K = np.reshape(self.K,[3,3])
        except CvBridgeError, e:
            print e

    def cleanup(self):
        print "Shutting down vision node."
        #cv2.destroyAllWindows()          
    
    
def main(args):       
    try:
        subs_obj = Depth_subs()
        rospy.spin()
        print "depth callback."
        print subs_obj.depth
        cv2.imshow("depth_in_main", subs_obj.depth)
        keystroke = cv2.waitKey(0)
    except KeyboardInterrupt:
        print "Shutting down vision node."
        DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
