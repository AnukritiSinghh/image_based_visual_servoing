''' returns the interaction matrix of 2D point as features
    for 2n features Lsd =2n X 6 matrix as defined in:
    Chaumette, F., & Hutchinson, S. (2006). Visual servo control. I. Basic approaches. IEEE Robotics & Automation Magazine, 13(4), 82-90.

    s -> input feature vector 2n X 1
    cam -> a structure with K as 3X3 interinsic matrix and T as tranform if known
    Z -> is the depth of feature vectors if known then it is 2nX1 
    else if it a scalar then same depth is assumed for all features
    ibvs is robust to depth errors for planar scenes
    author email: haritpandya@gmail.com

''' 
import numpy as np	

def get_interaction_point(s,KK,Z):
    px = KK[0,0]
    py = KK[1,1]
    v0=KK[0,2]
    u0=KK[0,2]
     
    if(len(Z.shape) == 1):
        Zarr=Z*np.ones_like(s)
    else:
        Zarr=Z

    Lsd=np.zeros((s.shape[0],6),dtype=np.float32)

    for m in range (0,Lsd.shape[0],2):
        x = (s[m] - u0)/px 
        y = (s[m+1] - v0)/py 
    
        Zinv =  1/Zarr[m]
        Lsd[m,:] =  np.array([-Zinv, 0, x*Zinv, x*y, -(1+x**2), y])

        Zinv =  1/Zarr[m+1]
        Lsd[m+1,:] =  np.array([0, -Zinv, y*Zinv, 1+y**2, -x*y, -x])
    
    
    return Lsd


