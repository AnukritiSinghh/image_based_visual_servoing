function centre = find_centre(img)
%img = imread(img);
img1 = img;                                    
[m,n,~] = size(img); 
for i=1:m
    for j=1:n
        if img(i,j,1)>220 && img(i,j,3)>220 && img(i,j,2)<30
            img1(i,j,:)=255;
        elseif img(i,j,1)>220  && img(i,j,3)<30 && img(i,j,2)<30
                img1(i,j,:)=255;
        elseif img(i,j,2)>220  && img(i,j,3)<30 && img(i,j,1)<30
                img1(i,j,:)=255;
        elseif img(i,j,3)>220  && img(i,j,1)<30 && img(i,j,2)<30
                img1(i,j,:)=255;
        else
            img1(i,j,:)=0;
        end
    end
end
img2 = rgb2gray(img1);                           
img2 = imbinarize(img2,0.5);                    %%% img2 is binarize image
%imshow(img2);                              

%img2 = rgb2gray(img); 	
%img2 = imbinarize(img,0.5);
%img2 = 1-img2;
%img2 = bwareaopen(img2,50);
%img2 = imfill(img2,'holes');                   
%imshow(img2);

cx = zeros(1,4);
cy = zeros(1,4);
properties = regionprops(img2,'BoundingBox');    %%% Genrate four bounding box circles are present
if(length(properties)<4)
    disp(1);                                     %%% If number of circles less than 4 then stop the process and display 1
    return;
end

if(length(properties)>4)                         %%% If number of circles greater than 4 then stop the process and display 2
    sort(properties.BoundingBox(1)+properties.BoundingBox(2));
    disp(2);
end

for k=1:length(properties)
    thisBB = properties(k).BoundingBox;		%%% thisBB has four parameters thisBB(1)-- left colum of BB, thisBB(2)-- upper row of BB, thisBB(3)-- width of BB, thisBB(4)-- length of BB
    y=round(thisBB(1)+thisBB(3)/2);         %%% centre of Bounding Box (BB)
    x=round(thisBB(2)+thisBB(4)/2);
    if (img(x,y,1)>220 && img(x,y,3)>220)	%%% circle colour is pink
        cx(3)=x;
        cy(3)=y;
    elseif (img(x,y,1)>220)                 %%% circle colour is red
        cx(2)=x;
        cy(2)=y;
    elseif (img(x,y,2)>220)                 %%% circle colour is green
        cx(1)=x;
        cy(1)=y;
    elseif(img(x,y,3)>220)                  %%% circle colour is blue
        cx(4)=x;
        cy(4)=y;
    end
end
centre=[cy(1) cx(1) ; cy(2) cx(2) ; cy(3) cx(3) ; cy(4) cx(4)]';
end