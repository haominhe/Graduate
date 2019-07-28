'''
CS 410/510: Introduction to Computer Vision
Final Project: License Plate Blurring, Deblurring and Recognition
Haomin He & Boxuan Zhang
References: 
Kasar, Thotreingam, Kumar, Jayant,  Ramakrishnan (2007). Font and Background Color Independent Text Binarization. 
Jasonlfunk. Jasonlfunk/Ocr-Text-Extraction. GitHub, 15 Oct. 2014, github.com/jasonlfunk/ocr-text-extraction.
Optical Character Recognition. Wikipedia, Wikimedia Foundation, 6 Mar. 2019, en.wikipedia.org/wiki/Optical_character_recognition.
Piscani, Francesco. License Plate Recognition with OpenCV 3 : OCR License Plate Recognition. YouTube, YouTube, 18 Feb. 2015, www.youtube.com/watch?v=nmDiZGx5mqU.
https://docs.opencv.org/2.4.13.7/doc/tutorials/imgproc/imgtrans/copyMakeBorder/copyMakeBorder.html
https://docs.opencv.org/3.4/d2/de8/group__core__array.html#ga0547c7fed86152d7e9d0096029c8518a
'''
'''
For plate number recognition we have consulted paper Font and Background Color Independent Text Binarization. 
to get enhanced image and used Tesseract (an optical character recognition engine abbreviated as OCR) to recognize 
text on a license plate. OCR is the electronic conversion of images of typed, handwritten or printed text into 
machine-encoded text.
'''

import cv2
import numpy as np
import sys
import os.path

def retain(contour):
    # retain this contour/EB or not
    if keepEdgeBox(contour) == True and contourConnect(contour) == True:
        return True
    else:
        return False

def keepEdgeBox(contour):
    # check if this edge box satisfies: 15 pixels < EBs size< 1/5th of the image dimension. 
    # 0.1 < EBs aspect ratio < 10
    # get EB coordinates, weight and height(float numbers)
    xEB, yEB, wEB, hEB = cv2.boundingRect(contour)
    wEB = wEB * 1.0
    hEB = hEB * 1.0
    # To eliminate highly elongated regions because they are not text characters
    aspectRatio = wEB / hEB
    boxSize = wEB * hEB
    if aspectRatio < 0.1 or aspectRatio > 10:
        return False
    if (boxSize < 15 or boxSize > ((thisimgX * thisimgY) / 5)):
        return False
    return True

def contourConnect(contour):
    # check if the current contour is connected
    firstPixel = contour[0][0]
    lastPixel = contour[len(contour) - 1][0]
    # if the difference is small, we consider it is a connected contour
    if abs(firstPixel[0] - lastPixel[0]) <= 1:
        if abs(firstPixel[1] - lastPixel[1]) <= 1:
            return True
    return False

def givenContour(index):
    # return a given contour
    global contours
    return contours[index]

def include(count, hierarchy, contour):
    if isChild(count, hierarchy) and childNum(getParent(count, hierarchy), hierarchy, contour) <= 2:
        return False
    if childNum(count, hierarchy, contour) > 2:
        return False
    return True

def getParent(count, hierarchy):
    # get the parent of the contour
    #print(count)
    #print(hierarchy.shape)
    parent = hierarchy[count][3]
    while not retain(givenContour(parent)) and parent > 0:
        parent = hierarchy[parent][3]
    return parent

def isChild(index, hierarchy):
    # if greater than 0, the contour is a child
    return getParent(index, hierarchy) > 0

def childNum(index, hierarchy, contour):
    # if there is no child, returns 0
    if hierarchy[index][2] < 0:
        return 0
    # if there is a child
    else:
        # count contours that satisfy our requirements
        if retain(givenContour(hierarchy[index][2])):
            tempcount = 1
        else:
            tempcount = 0
        
        # count child's siblings and their children
        tempcount += countSiblings(hierarchy[index][2], hierarchy, contour, True)
        return tempcount

def countSiblings(index, hierarchy, contour, hasChildren = False):
    # count the contour's siblings
    if hasChildren:
        count = childNum(index, hierarchy, contour)
    else:
        count = 0
    # look ahead
    ahead = hierarchy[index][0]
    while ahead > 0:
        if retain(givenContour(ahead)):
            count += 1
        if hasChildren:
            count += childNum(ahead, hierarchy, contour)
        ahead = hierarchy[ahead][0]
    # look behind
    behind = hierarchy[index][1]
    while behind > 0:
        if retain(givenContour(behind)):
            count += 1
        if hasChildren:
            count += childNum(behind, hierarchy, contour)
        behind = hierarchy[behind][1]
    return count

def intensityCal(xx, yy):
    global thisimg, thisimgY, thisimgX
    # pixel intensity = 0.30R + 0.59G + 0.11B
    if yy >= thisimgY or xx >= thisimgX:
        # this pixel is out of bounds 
        return 0
    pixel = thisimg[yy][xx]
    return 0.30 * pixel[2] + 0.59 * pixel[1] + 0.11 * pixel[0]

if __name__ == "__main__":
    print('==================================================')
    print('PSU CS 410/510, Winter 2019, Final Project: License Plate Recognition')
    print('==================================================')
    """
    Example command: 
    python PlateNumberRecognition.py 797.jpg 797output.jpg
    tesseract 797output.jpg 797outputext
    """

    # check command arguments
    if len(sys.argv) != 3:
        print("Example command: python PlateNumberRecognition.py 797.jpg 797output.jpg")
        sys.exit()
    else:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
    # if no such file exist 
    if not os.path.isfile(inputFile):
        print("This file '%s' doesn't exist" % inputFile)
        sys.exit()
    
    # load the image
    inputImage = cv2.imread(inputFile)
    # adding borders to images, BORDER_CONSTANT: Pad the image with a constant value 
    thisimg = cv2.copyMakeBorder(inputImage, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
    # get the width and height of the image
    thisimgY = len(thisimg)
    thisimgX = len(thisimg[0])
    # get RGB of the image
    # divides a multi-channel array into several single-channel arrays
    B, G, R = cv2.split(thisimg)
    # first do Canny Edge Detection on color channels
    blue = cv2.Canny(B, 200, 250)
    green = cv2.Canny(G, 200, 250)
    red = cv2.Canny(R, 200, 250)
    # build edge map based on color channel edges
    edgeMap = blue | green | red
    # Finds contours in a binary image
    im2, contours, hierarchy = cv2.findContours(edgeMap.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    hierarchy = hierarchy[0]
    
    # for each countour, find eligible edge boxes EB(bounding boxes) and keep them
    # remove non-eligible edge boxes
    keepEB = []
    for count, contour in enumerate(contours):
        coorX, coorY, widthW, heightH = cv2.boundingRect(contour)
        # check EB size and its connection
        if retain(contour) and include(count, hierarchy, contour):
            keepEB.append([contour, [coorX, coorY, widthW, heightH]])
    
    # build output image
    outputImage = edgeMap.copy()
    outputImage.fill(255)

    # calculate box foreground and background intensities 
    for index, (contour, box) in enumerate(keepEB):
        # foreground intensity is computed as the mean gray level intensity of the pixels that correspond to the edge pixels
        foregroundIntensity = 0.0
        for each in contour:
            foregroundIntensity += intensityCal(each[0][0], each[0][1])
        foregroundIntensity /= len(contour)
        # The background intensity is based on intensity of three pixels each at the 
        # periphery of the corners of the bounding box
        x, y, w, h = box
        backgroundIntensity = \
            [
                # bottom left corner 3 pixels
                intensityCal(x - 1, y - 1),
                intensityCal(x - 1, y),
                intensityCal(x, y - 1),
                # bottom right corner 3 pixels
                intensityCal(x + w + 1, y - 1),
                intensityCal(x + w, y - 1),
                intensityCal(x + w + 1, y),
                # top left corner 3 pixels
                intensityCal(x - 1, y + h + 1),
                intensityCal(x - 1, y + h),
                intensityCal(x, y + h + 1),
                # top right corner 3 pixels
                intensityCal(x + w + 1, y + h + 1),
                intensityCal(x + w, y + h + 1),
                intensityCal(x + w + 1, y + h)
            ]
        # Find the median of the background pixels
        backgroundIntensity = np.median(backgroundIntensity)
        # we binarize each edge component using the estimated foreground intensity 
        # as the threshold. While binarization process, foreground text is output as 
        # black and the background as white.
        if foregroundIntensity >= backgroundIntensity:
            fg = 255
            bg = 0
        else:
            fg = 0
            bg = 255

            # Loop through every pixel in the box and color the
            # pixel accordingly
        for x1 in range(x, x + w):
            for y1 in range(y, y + h):
                # out of bound
                if y1 >= thisimgY or x1 >= thisimgX:
                    continue
                if intensityCal(x1, y1) > foregroundIntensity:
                    outputImage[y1][x1] = bg
                else:
                    outputImage[y1][x1] = fg
    # output the result image
    outputImage = cv2.blur(outputImage, (2, 2))
    cv2.imwrite(outputFile, outputImage)
















