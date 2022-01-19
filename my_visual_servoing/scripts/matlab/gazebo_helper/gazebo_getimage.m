function img = gazebo_getimage(handle)
    img=readImage(receive(handle.img_sub));
end