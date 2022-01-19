import numpy as np
import cv2
import cv2.aruco as aruco
import time


def detect_Aruco(img, marker_id):  #returns the detected aruco list dictionary with id: corners
    corners = None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)   #creating aruco_dict with 5x5 bits with max 250 ids..so ids ranges from 0-249
    parameters = aruco.DetectorParameters_create()  #refer opencv page for clarification
    #lists of ids and the corners beloning to each id
    _corners, _ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
    if(_ids is not None):
  
        #corners is the list of corners(numpy array) of the detected markers. 
        #For each marker, its four corners are returned in their original order (which is clockwise starting with top left). 
        #So, the first corner is the top left corner, followed by the top right, bottom right and bottom left.
        _corners = np.asarray(_corners)
        corners = _corners[_ids == marker_id,...]
        corners = corners[0,...]

    return corners
     

def show_corners(img, corners):    #function to mark the centre and display the id
    print(corners.shape)
    cv2.circle(img,(corners[0,0],corners[0,1]),8, (0,0,255),-1)
    cv2.circle(img,(corners[1,0],corners[1,1]),8, (0,255,0),-1)    
    cv2.circle(img,(corners[2,0],corners[2,1]),8, (255,0,0),-1)    
    cv2.circle(img,(corners[3,0],corners[3,1]),8, (255,0,255),-1)    
    cv2.imshow('image',img)
    cv2.waitKey(0)
    
    

def do_affine_warp(img):
    rows,cols,ch = img.shape
    pts1 = np.float32([[50,50],[200,50],[50,200]])
    pts2 = np.float32([[10,100],[200,50],[100,250]])
    M = cv2.getAffineTransform(pts1,pts2)
    img = cv2.warpAffine(img,M,(cols,rows))
    return img
    
		
def getkeypts(img,marker_id):
    corners = detect_Aruco(img,marker_id)
    return corners


if __name__== "__main__":
    img = cv2.imread('test_marker.jpg')
    if(corners is not None):
        show_corners(img,corners)

