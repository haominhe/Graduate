'''
CS 410/510: Introduction to Computer Vision
Final Project: License Plate Blurring, Deblurring and Recognition
Haomin He & Boxuan Zhang
'''

import cv2
import numpy as np
import sys

#function to make picture become sharpness and increase the contrast
def picture_sharpen(new_img,param):
    #the filter to use in filter2d function
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    kernel1 = np.array([[-1,-1,-1], [-1,9,-1],[-1,-1,-1]],np.float32)
    #use opencv function to find differences between build by self and opencv result.
    #dst = cv2.filter2D(img, -1, kernel=kernel)
    
    #make a copy of orignal img
    img = new_img.copy()
    #size of image shape
    h,w,c = img.shape
    #check the filter equal to 3
    if param == "3":
        #for loop with 3 * 3 filter
        for y in range(1,h-1):
            for x in range(1,w-1):
                for z in range(0,c):
                    #get the sharpen value with image and then replace the value
                    sharpen_value = 5* new_img[y][x][z] - new_img[y-1][x][z] - new_img[y][x-1][z] - new_img[y+1][x][z] - new_img[y][x+1][z]
                    #image clip between 0 and 255 because bgr channel from 0 to 255
                    img[y][x][z] = sharpen_value.clip(0.0,255.0)
                    
    #check the filter equal to 5                
    elif param == "5":
        #use kernel1 as the filter to compute the result.
        for y in range(1,h-1):
            for x in range(1,w-1):
                for z in range(0,c):
                    #get the sharpen value with image and then replace the value
                    sharpen_value = 9* new_img[y][x][z] - new_img[y-1][x][z] - new_img[y][x-1][z] - new_img[y+1][x][z] - new_img[y][x+1][z] - new_img[y-1][x-1][z] - new_img[y-1][x+1][z] - new_img[y+1][x-1][z] - new_img[y+1][x+1][z]
                    #image clip between 0 and 255 because bgr channel from 0 to 255
                    img[y][x][z] = sharpen_value.clip(0.0,255.0)
    #return the final result.
    return img

#function of picture sharpenning, with current pixel minus the pixel value around the current pixel and then get result.
def detect_and_deblur_plate(img,param):
    #cv2 function cascade classifier to read in Russian number plate .xml file
    plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
    #make a copy
    plate_img = img.copy()
    #make a new copy to keep image and then make the picture sharpning
    roi = img.copy()
    #read in the size of number plate, and then make detection with scale factor is 1.2 and min neighbor equals to 3
    plate_rects = plate_cascade.detectMultiScale(plate_img,scaleFactor=1.2, minNeighbors=3) 
    #for loop to suit the number plate and then run the sharpen function with number plate that finded by Haar Cascade
    for (x,y,w,h) in plate_rects:         
        roi = roi[y:y+h,x:x+w]
        #run picture sharpen function and then get the sharpen picture
        sharpen_roi = picture_sharpen(roi,param)
        #copy the result replace orignal pixels
        plate_img[y:y+h,x:x+w] = sharpen_roi        
    return plate_img
    
#median blur function replace current pixel with neighborhoob and self values exchange to the meidan values
def median_blur(new_img,param):
    #Copy the current image
    img = new_img.copy()
    #find the size of image
    h,w,c = new_img.shape
    #check the filter should be used in the call
    if param == "5":
        #filter size is 5, I dont write corners exchange, because it will make code become long and long, I can show you what I did, but I dont want to add.
        for y in range(2, h-2):
            for x in range(2,w-2):
                for z in range(0,c):
                    #make list of 5 * 5 image filter and put them in a list
                    list_temp = [new_img[y-2][x-2][z],new_img[y-1][x-2][z],new_img[y][x-2][z],new_img[y+1][x-2][z],new_img[y+2][x-2][z],
                         new_img[y-2][x-1][z], new_img[y-1][x-1][z],new_img[y][x-1][z],new_img[y+1][x-1][z],new_img[y+2][x-1][z],
                         new_img[y-2][x][z],new_img[y-1][x][z], new_img[y][x][z],new_img[y+1][x][z],new_img[y+2][x][z],
                         new_img[y-2][x+1][z],new_img[y-1][x+1][z],new_img[y][x+1][z],new_img[y+1][x+1][z],new_img[y+2][x+1][z],
                         new_img[y-2][x+2][z],new_img[y-1][x+2][z],new_img[y][x+2][z],new_img[y+1][x+2][z],new_img[y+2][x+2][z]]
                    #sort the list
                    list_temp.sort()
                    #find the 13(so 12) in the list is the median value
                    img[y][x][z] = list_temp[12]
    
    elif param == "3":
        #filter size is 3.
        for y in range(1,h-1):
            for x in range(1,w-1):
                for z in range(0,c):
                    #make list of 3 * 3 image filter and put them in a list
                    list_temp = [new_img[y][x][z],new_img[y-1][x][z],new_img[y-1][x+1][z],new_img[y][x+1][z],new_img[y+1][x+1][z],
                                 new_img[y+1][x][z],new_img[y+1][x-1][z],new_img[y][x-1][z],new_img[y-1][x-1][z]] 
                    #sort the list
                    list_temp.sort()
                    #find the 5(so 4) in the list
                    img[y][x][z] = list_temp[4]

    #return the final result.                
    return img

#detect function and blur function.
def detect_and_blur_plate(img,param):
    #cv2 function cascade classifier to read in Russian number plate .xml file
    plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
    #make a copy
    plate_img = img.copy()
    #make a new copy to keep image and then make the blur
    roi = img.copy()
    #read in the size of number plate, and then make detection with scale factor is 1.2 and min neighbor equals to 3
    plate_rects = plate_cascade.detectMultiScale(plate_img,scaleFactor=1.2, minNeighbors=3)     
    #for loop to suit the number plate and then run the blur function with number plate that finded by Haar Cascade
    for (x,y,w,h) in plate_rects:         
        roi = roi[y:y+h,x:x+w]
        #use medianBlur and detect the difference between self build algorithm and opencv function.
        #blurred_roi = cv2.medianBlur(roi,5) 
        blurred_roi = median_blur(roi,param)     
        plate_img[y:y+h,x:x+w] = blurred_roi        
    return plate_img
 
#function detection use Haar Cascades     
def detection(img):
    #cv2 function cascade classifier to read in Russian number plate .xml file
    plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
    #make a copy
    plate_img = img.copy()
    #read in the size of number plate, and then make detection with scale factor is 1.2 and min neighbor equals to 3
    plate_rects = plate_cascade.detectMultiScale(plate_img,scaleFactor=1.2, minNeighbors=3) 
    #for loop to suit the number plate and then build the rectangle with number plate that finded by Haar Cascade
    for (x,y,w,h) in plate_rects: 
        cv2.rectangle(plate_img, (x,y), (x+w,y+h), (0,0,255), 4)
    #Return result.
    return plate_img
    
if __name__ == "__main__":
    print('==================================================================')
    print('PSU CS 410/510, Winter 2019, Final Project: number plate operation')
    print('==================================================================')

    path_file_image_source = sys.argv[1]     #read in image
    param_command_blur = sys.argv[2]         #read in filter size of blur
    param_command_sharp = sys.argv[3]        #read in filter size of sharpening
    print("The blur filter you enter :",param_command_blur)
    print("The sharpen filter you enter : ",param_command_sharp)
    img = cv2.imread(path_file_image_source)
    
    result_detection = detection(img)                                     #Run function Haar Cascade
    result_blur = detect_and_blur_plate(img,param_command_blur)           #Run function median blur 
    result_shapren = detect_and_deblur_plate(img,param_command_sharp)     #Run function sharpen
    #result_recognize = detect_and_recognize(img)
    
    cv2.imwrite('result_detection.png',result_detection)
    cv2.imwrite('result_blur.png',result_blur)
    cv2.imwrite('result_sharpen.png',result_shapren)
    #cv2.imwrite('result_recognize.png',result_recognize)