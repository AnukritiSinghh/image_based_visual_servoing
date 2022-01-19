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

#import roslib; roslib.load_manifest('rbx1_vision')
import rospy
import sys
import cv2
from sensor_msgs.msg import Image, CameraInfo, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class Img_subs():
    image = None
    	
    def __init__(self):
        self.node_name = "image_subscriber"
        
        rospy.init_node(self.node_name)
        
        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)
        
        # Create the OpenCV display window for the RGB image
        #self.cv_window_name = self.node_name
        #cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        #cv2.moveWindow("image", 25, 75)
        
        # And one for the depth image
        #cv2.namedWindow("depth", cv2.WINDOW_NORMAL)
        #cv2.moveWindow("depth", 25, 350)
        
        # Create the cv_bridge object
        self.bridge = CvBridge()
        
        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        self.image_sub = rospy.Subscriber("/kinect_camera/depth/image_raw", Image, self.image_callback)
        #self.depth_sub = rospy.Subscriber("/kinect_camera/depth/depth_image_raw", Image, self.depth_callback)
        
        #return()
        #rospy.loginfo("Waiting for image topics...")

    def image_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        #print 'image_callback'
        
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
            self.image = frame
            #cv2.imshow("image", frame)
            #self.keystroke = cv2.waitKey(500)
            #cv2.destroyAllWindows()   
            #self.image_sub.unregister()
            
            
        except CvBridgeError, e:
            print e
          
    
    def cleanup(self):
        print "Shutting down vision node."
        cv2.destroyAllWindows()   



    
def main(args):       
    try:
        
        Img_subs()
        rospy.spin()
        print "image callback"
    except KeyboardInterrupt:
        print "Shutting down vision node."
        DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
