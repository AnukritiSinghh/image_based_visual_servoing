'''using aruco markers for visual servoing, we will get the image from gazebo camera
   then aruco detection from opencv is used to get 4 corners of the marker
   the desired pose is in for of image  in utils.
   We assume that the camera parameters is known and images are rectifed of distortion.
   We will assign a generic depth to the marker and try to move the robot to attain that depth.
   for issues mail to haritpandya@gmail.com

   note the suffix <.>d is used to represent the desired configuration
   and <.>cur and <.>init configuration 
''' 

import sys
import numpy as np
import cv2
import time
from geometry_msgs.msg import Wrench, Pose, Twist

# Add the utils folder path to the sys.path list
sys.path.append('../utils')
sys.path.append('../features')
sys.path.append('../interactions')

from get_aruco_keypoints import getkeypts
import get_interaction_point as interaction_mat
from gazebo_handler import Gazebo_handler


handle = Gazebo_handler()        
K = handle.kinect_subs.K

#robot name for moving it to a desired pose
rob_name = 'mrm'


#Setting the initial initial camera pose
#The object is assumed to be at world origin.

init_pose = Pose()
init_pose.position.x = 3
init_pose.position.y = 0
init_pose.position.z = 0
init_pose.orientation.x = 0
init_pose.orientation.y = 0
init_pose.orientation.z = 0
init_pose.orientation.w = 1
handle.move_object_to(rob_name,init_pose)

#desired pose could be given in form of xy coordinates 
ydes = np.array([[50, 50], [250, 50], [250, 250], [50, 250]])

#Alternatively, desired pose could be given in form of image
# uncomment following lines for this approach. 
'''d = cv2.imread('../utils/test_marker.jpg')
xydes = getkeypts(imgd,11) #we are detecting marker 11'''


#Another option is to move the camera to a desired pose and get image.
# uncomment following lines for this approach.
'''des_pose = Pose()
des_pose.position.x = init_pose.position.x+0.5
des_pose.position.y = init_pose.position.y+1
handle.move_object_to(rob_name,des_pose)
imgd = handle.kinect_subs.image
#move the camera back to initial pose
handle.move_object_to(rob_name,init_pose)
xydes = getkeypts(imgd,11) #we are detecting marker 11'''



try:
    kp_des=xydes.flatten()
except:
    print('unable to detect marker for desired image. Either features out of field of view or wrong marker id.')
    sys.exit()

#ibvs tuning parameters
mu = 0.008
desired_depth=np.array([1])



if __name__== "__main__":
    
    cnt = 1
    while(1):
        img = handle.kinect_subs.image
        try:
            xy_curr = getkeypts(img,11) #we are detecting marker 11
            kp_curr = xy_curr.flatten()
        except:
            print('unable to detect marker. Either features out of field of view or wrong marker id.')
            sys.exit()

        
        #displaying detected centeres
        cv2.circle(img,(xy_curr[0,0],xy_curr[0,1]),5, (255,0,0),-1)
        cv2.circle(img,(xy_curr[1,0],xy_curr[1,1]),5, (0,255,0),-1)    
        cv2.circle(img,(xy_curr[2,0],xy_curr[2,1]),5, (0,0,255),-1)    
        cv2.circle(img,(xy_curr[3,0],xy_curr[3,1]),5, (255,0,255),-1)    


        #displaying desired centeres
        cv2.circle(img,(xydes[0,0],xydes[0,1]),5, (255,0,0),-1)
        cv2.circle(img,(xydes[1,0],xydes[1,1]),5, (0,255,0),-1)    
        cv2.circle(img,(xydes[2,0],xydes[2,1]),5, (0,0,255),-1)    
        cv2.circle(img,(xydes[3,0],xydes[3,1]),5, (255,0,255),-1)    

        cv2.imshow('image',img)
        cv2.waitKey(1)
    
    
        #getinteraction_intensity(<current keypoints>,<camera.intensic>,<length
        #of featurevector>,<estimate of camera depth if true depth not available>,
        #<flag to use true depth (1) or estmiate(0)>,<true depth of every keypoint>);
        Lsd=interaction_mat.get_interaction_point(kp_des,K,desired_depth)
        

    
        #control loop
        error=kp_curr-kp_des
        vc=-mu*np.matmul(np.linalg.pinv(Lsd),error)
        print('iteration=%d,error=%.2f, vc=%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n'%(cnt,np.linalg.norm(error),vc[0],vc[1],vc[2],vc[3],vc[4],vc[5]))
        #For testing the camera velocity along an axis. 
        #vc= np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.1])
        if(cnt > 200 or np.linalg.norm(error) <3):
            break; 
        #Rotd = Rotation.from(np.vstack([vc(4), vc(5), vc(6)])) #%ZYX
        #Td = np.hstack([Rotd, np.vstack([vc(1),vc(2),vc(3)])])
        #Tcurr=np.matmul(Tcurr,np.vstack([Td;0 0 0 1]))
        #status = handle.(gazebo_handle ,Tcurr)
  
        #here we are using delta pose but you can change to velocity dircty using twist messages.
        cmd = Twist()
        #converting to ros coordinate syaytem from image coodrdinate system.
        #Thanks ayush gaud for this.
        cmd.linear.x =  vc[2]
        cmd.linear.y = -vc[0]
        cmd.linear.z = -vc[1]

        cmd.angular.x = vc[5]
        cmd.angular.y = -vc[3]
        cmd.angular.z = -vc[4]
        handle.set_object_vel(rob_name,cmd)

        cnt = cnt +1
    cv2.imshow('image',img)
    cv2.waitKey(5)
