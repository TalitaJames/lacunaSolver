function [croppedImg] = CircleCrop(img)
    
    imgGS = im2gray(img);
    imgBW = imbinarize(imgGS, 0.5);
    %imshowpair(imgGS,imgBW,"montage");

    structureElement = strel('disk', 100);  % Structuring element (circle)
    closedImg = imclose(imgBW, structureElement);
    %imshow(closedImg)
    
    largestBlob = bwareafilt(closedImg, 1);  % get only the largest blob (circle)
    %imshowpair(img,largestBlob,'falsecolor');
    
    % Step 6: Create a mask for the circular region
    [rows, cols] = size(imgGS);
    [xx, yy] = ndgrid((1:rows), (1:cols));
    
    % Find the region's bounding box to extract the circular area
    props = regionprops(largestBlob, 'Centroid', 'EquivDiameter');
    center = props.Centroid;
    radius = props.EquivDiameter / 2;
    
    % Create a circular mask and apply it to the coloured image
    mask = sqrt((xx - center(2)).^2 + (yy - center(1)).^2) <= radius;
    %BUG: only applies it to the center of the img not to 
    % the center of circle origin
    
    croppedImg = img;
    croppedImg(repmat(~mask, [1 1 3])) = 0; % Set pixels outside the mask to 0 (black)

end