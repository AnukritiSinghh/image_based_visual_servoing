clear;
addpath('../interactions');
addpath('../gazebo_helper');
addpath('../util');

gazebo_handle  = gazebo_init();

Tinit = eye(4);
Tcurr=Tinit;

imdes = imread('outz.jpg');
gray_imdes = rgb2gray(imdes);
points2 = detectSURFFeatures(gray_imdes);
[f2,vpts2] = extractFeatures(gray_imdes,points2);
%ibvs tuning parameters
lambda=0.0002;
desired_depth=10;
iter = 1;

while(1)
    img = gazebo_getimage(gazebo_handle);
    %resize_img = imresize(img,1);
    gray_img = rgb2gray(img);
    points1 = detectSURFFeatures(gray_img);
    [f1,vpts1] = extractFeatures(gray_img,points1);
    indexPairs = matchFeatures(f1,f2);
    matchedPoints1 = vpts1(indexPairs(:,1));
    matchedPoints2 = vpts2(indexPairs(:,2));
    [tform,inlierpoints2,inlierpoints1] =estimateGeometricTransform(matchedPoints2,matchedPoints1,'similarity');
    n = length(inlierpoints1);

    %imshow(img);
    showMatchedFeatures(img,imdes,inlierpoints1,inlierpoints2);
    curr = inlierpoints1.Location;
    curr = curr';
    kp_curr = curr(:);
    des = inlierpoints2.Location;
    des = des';
    kp_des = des(:);
    
    Lsd=getinteraction_point(kp_des,gazebo_handle.cam,length(kp_des),desired_depth,0,desired_depth);
    
    error=kp_curr-kp_des;
    vc=-lambda*pinv(Lsd)*error;
    fprintf('error=%.2f, vc=%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n',norm(error),vc(1),vc(2),vc(3),vc(4),vc(5),vc(6));
    
    if(iter > 200 || sum(abs(error))<4) 
        fclose(fileID);
        break;
    end
    Rotd = eul2rotm([vc(4), vc(5), vc(6)]);%ZYX
    Td = [Rotd [vc(1);vc(2);vc(3)]];
    Tcurr=Tcurr*[Td;0 0 0 1];
    status = gazebo_movecam(gazebo_handle ,Tcurr);
    iter = iter +1;
    clearvars kp_des kp_curr 
end
