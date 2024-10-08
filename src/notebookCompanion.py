import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

def showImage(img):
    # Convert color from BGR (OpenCV default) to RGB (Matplotlib default)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    # Display the image using Matplotlib
    plt.figure(figsize=(6, 12))  # Adjust the size
    plt.imshow(img_rgb)
    plt.axis('off')  # Hide axis
    plt.show()