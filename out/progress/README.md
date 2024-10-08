# Images and their context, descriptions
> Details about images taken to record progress

**`initialSuccsessCircleCrop.jpg`**
Taken on 15/09/2024, in matlab

Circle crop algorithm using a largest blob of black and assuming a circle is there
- Errors happened when board wasn't centered

**`pythonCircleCrop.jpg`**
Taken on 30/09/2024, in python

Circle crop from commit `5c56dd2`  


**`hsv_image_purple`**
Taken on 01/10/2024, in python
Filtering on image `006.jpg` using 
```py
hueRangePurple = [0.95, 1]
saturation = 20/255
value = 0.5

lacunaFilteredOne = IP.hsvColorFilter(lacunaCircle, hueRangePurple, saturation, value)
```
