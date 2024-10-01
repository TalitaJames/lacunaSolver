function filteredImg = ColourFiltering(img, hueRange, saturation, value)
    % filters an image by a hue range [min, max] to return

    % Convert the image from RGB to HSV color space
    hsvImage = rgb2hsv(img);
    
    % Extract the Hue, Saturation, and Value channels
    hueChannel = hsvImage(:, :, 1);        % Hue channel (0 to 1)
    saturationChannel = hsvImage(:, :, 2); % Saturation channel
    valueChannel = hsvImage(:, :, 3);      % Value channel
    
    % Create masks for the colors
    colourMask = (hueChannel >= hueRange(1)) & (hueChannel <= hueRange(2)) & ...
                 (saturationChannel >= saturation) & (valueChannel >= value);
             
    % Apply the masks to the original image
    filteredImg = img;
    
    % Set pixels not corresponding to the desired color ranges to black
    filteredImg(repmat(~colourMask, [1 1 3])) = 0;

end
