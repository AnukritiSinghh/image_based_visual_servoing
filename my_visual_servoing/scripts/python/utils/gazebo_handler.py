#! /usr/bin/env python
import rospy
from std_srvs.srv import Empty
from gazebo_msgs.srv import GetModelProperties, GetWorldProperties, GetModelState, SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Wrench, Pose, Twist
import cv2
import numpy as np
from demo_kinect_subscriber import Kinect_subs
import time

class Block:
    def __init__(self, name, relative_entity_name):
        self._name = name
        self._relative_entity_name = relative_entity_name

class Gazebo_handler:

    def __init__(self):

            self.kinect_subs = self.get_kinect_subs()
            depthmap_init = self.kinect_subs.depth
            image_init = self.kinect_subs.image
            #depthmap_init_normalized = cv2.normalize(depthmap_init, None , 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)         


    def pause_gazebo_physics(self):
		pause=rospy.ServiceProxy('/gazebo/pause_physics',Empty)
		pause()
		print('gazebo paused')
		time.sleep(0.1)
	
    def unpause_gazebo_physics(self):
		unpause=rospy.ServiceProxy('/gazebo/unpause_physics',Empty)
		unpause()
		print('gazebo unpaused')
		time.sleep(0.1)
	
    def get_kinect_subs(self):
        subs_obj = Kinect_subs()
        while not rospy.is_shutdown():
            time.sleep(0.1)
            if subs_obj.depth is not None:
                time.sleep(0.1)
                break;
        
        return subs_obj
    
    		
    def get_model_names(self):
        get_world_prop=rospy.ServiceProxy('/gazebo/get_world_properties',GetWorldProperties)
        try:
            world_prop = get_world_prop()
            print('object names:', world_prop.model_names)
            object_names = world_prop.model_names
        except rospy.ServiceException as e:
            rospy.loginfo("Get World Properties service call failed:  {0}".format(e))
		
    
    def get_pose(self,model_name):
        original_state = None
        try:
            get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            original_state = get_model_state(model_name, 'world')
            time.sleep(0.1)
            
        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))    
        
        return original_state.pose
	
    def move_object_to(self,model_name,pose):
        try:
            #displace model
            set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            new_state = ModelState()
            new_state.model_name = model_name
            new_state.pose = Pose()
            new_state.twist = Twist()
            new_state.reference_frame = 'world'
        
            
            new_state.pose.position.x = pose.position.x
            new_state.pose.position.y = pose.position.y
            new_state.pose.position.z = pose.position.z
            
            new_state.pose.orientation.x = pose.orientation.x
            new_state.pose.orientation.y = pose.orientation.y
            new_state.pose.orientation.z = pose.orientation.z
            new_state.pose.orientation.w = pose.orientation.w
            
            
            resp1 = set_model_state(new_state)
            time.sleep(0.1)
            
        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))

    def set_object_vel(self,model_name,vel):
        try:
            #displace model
            set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            new_state = ModelState()
            new_state.model_name = model_name
            new_state.pose = self.get_pose(model_name)
            new_state.twist = Twist()
            new_state.reference_frame = 'world'
        
            
            new_state.twist.linear.x = vel.linear.x
            new_state.twist.linear.y = vel.linear.y
            new_state.twist.linear.z = vel.linear.z
            
            new_state.twist.angular.x = vel.angular.x
            new_state.twist.angular.y = vel.angular.y
            new_state.twist.angular.z = vel.angular.z

            
            
            resp1 = set_model_state(new_state)
            time.sleep(0.1)
            
        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
	
	
if __name__ == '__main__':
    handle = Gazebo_handler()
    object_names = handle.get_model_names()
    print(object_names)
    #handle.pause_gazebo_physics()
    #handle.get_object_gt_depth()
    #handle.unpause_gazebo_physics()
    #pose = handle.get_pose(model_name)
    #handle.move_object(model_name,pose,True)

    depthmap = handle.kinect_subs.depth
    image = handle.kinect_subs.image
    K = handle.kinect_subs.K
    #depthmap_normalized = cv2.normalize(depthmap, None , 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    print(K)
    
    cv2.imshow("depth_in_main", depthmap)
    keystroke = cv2.waitKey(0)
    cv2.imwrite('depthmap.png',depthmap)
    cv2.imwrite('image.png',image)
