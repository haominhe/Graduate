# CS510 Homework 2: Homography-based Image Stitching
# Haomin He
# Reference:
# https://docs.opencv.org/3.4/da/df5/tutorial_py_sift_intro.html
# https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html
# https://github.com/ojhaChandu/CV-Codes
# https://github.com/krutikabapat/Image_Stitching
# https://github.com/a514514772
# https://github.com/ShrishtiManjeshwar/Image-Stitching
# https://github.com/dani-amirtharaj/KeyPointDetection-Homography-EpipolarGeometry
# https://github.com/hughesj919/HomographyEstimation/
# https://stackoverflow.com/questions/30716610/how-to-get-pixel-coordinates-from-feature-matching-in-opencv-python
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html



import cv2
import sys
import numpy as np
import random

def ex_find_homography_ransac(list_pairs_matched_keypoints, threshold_ratio_inliers=0.85, threshold_reprojtion_error=3, max_num_trial=1000):
    '''
    Apply RANSAC algorithm to find a homography transformation matrix that align 2 sets of feature points, transform the first set of feature point to the second (e.g. warp image 1 to image 2)
    :param list_pairs_matched_keypoints: has the format as a list of pairs of matched points: [[[p1x,p1y],[p2x,p2y]],....]
    :param threshold_ratio_inliers: threshold on the ratio of inliers over the total number of samples, accept the estimated homography if ratio is higher than the threshold
    :param threshold_reprojtion_error: threshold of reprojection error (measured as euclidean distance, in pixels) to determine whether a sample is inlier or outlier
    :param max_num_trial: the maximum number of trials to do take sample and do testing to find the best homography matrix
    :return best_H: the best found homography matrix
    '''
    best_H = None

    listlength = len(list_pairs_matched_keypoints)
    for every in range(listlength):
        list_pairs_matched_keypoints[every] = list_pairs_matched_keypoints[every][0] + list_pairs_matched_keypoints[every][1]
    
    inlinersMost = []
    
    for each in range(max_num_trial):
        # Apply RANSAC algorithm to find a homography transformation matrix
        point1 = list_pairs_matched_keypoints[random.randrange(0, listlength)]
        point2 = list_pairs_matched_keypoints[random.randrange(0, listlength)]
        # Variants of numpy.stack function to stack so as to make a single array vertically
        tempVar = np.vstack((point1, point2))
        point3 = list_pairs_matched_keypoints[random.randrange(0, listlength)]
        tempVar = np.vstack((tempVar, point3))
        point4 = list_pairs_matched_keypoints[random.randrange(0, listlength)]
        tempVar = np.vstack((tempVar, point4))
        
        #print(tempVar[0])
        # build the matrix
        matrixH = buildMatrix(tempVar)
        inlierCount = []
        for count in range(listlength):
            # find the distance between estimated points and original points
            distance = CalDistance(list_pairs_matched_keypoints[count], matrixH)
            if distance < 5:
                inlierCount.append(list_pairs_matched_keypoints[count])
        # set maximum inliner value
        if len(inlierCount) > len(inlinersMost):
            inlinersMost = inlierCount
            best_H = matrixH
        if len(inlinersMost) > (listlength * threshold_ratio_inliers):
            break
    return best_H


def buildMatrix(tempPoints):
    thislist = []
    # build the matrix
    for each in tempPoints:
        point1 = np.matrix([each.item(0), each.item(1), 1])
        #print(point1)
        point2 = np.matrix([each.item(2), each.item(3), 1])
        temp1 = [0, 0, 0, -point2.item(2) * point1.item(0), -point2.item(2) * point1.item(1), -point2.item(2) * point1.item(2),
              point2.item(1) * point1.item(0), point2.item(1) * point1.item(1), point2.item(1) * point1.item(2)]
        temp2 = [-point2.item(2) * point1.item(0), -point2.item(2) * point1.item(1), -point2.item(2) * point1.item(2), 0, 0, 0,
              point2.item(0) * point1.item(0), point2.item(0) * point1.item(1), point2.item(0) * point1.item(2)]
        thislist.append(temp2)
        thislist.append(temp1)
        #print(thislist)
    matrixBuild = np.matrix(thislist)
    # Singular Value Decomposition
    # Factors the matrix a as u * np.diag(s) * v, where u and v are unitary and s is a 1-d array of a‘s singular values
    U, s, V = np.linalg.svd(matrixBuild)
    # shapes an array without changing data of array
    # shape to three by three matrix
    matrixH = np.reshape(V[8], (3, 3))
    matrixH = (1/matrixH.item(8)) * matrixH
    return matrixH


def CalDistance(point, matrixH):
    # find the distance between estimated points and original points
    point1 = np.transpose(np.matrix([point[0], point[1], 1]))
    # find estimated point
    mayPoint2 = np.dot(matrixH, point1)
    mayPoint2 = (1/mayPoint2.item(2)) * mayPoint2
    # find original point
    point2 = np.transpose(np.matrix([point[2], point[3], 1]))
    dis = point2 - mayPoint2
    # return one of eight different matrix norms
    return np.linalg.norm(dis)


def ex_extract_and_match_feature(img_1, img_2, ratio_robustness=0.7):
    '''
    1/ extract SIFT feature from image 1 and image 2,
    2/ use a bruteforce search to find pairs of matched features: for each feature point in img_1, find its best matched feature point in img_2
    3/ apply ratio test to select the set of robust matched points
    :param img_1: input image 1
    :param img_2: input image 2
    :param ratio_robustness: ratio for the robustness test
    :return list_pairs_matched_keypoints: has the format as list of pairs of matched points: [[[p1x,p1y],[p2x,p2y]]]
    '''
    # ==============================
    # ===== 1/ extract features from input image 1 and image 2
    # ==============================

    # First to create SIFT object
    sift = cv2.xfeatures2d.SIFT_create()
    # Finds the keypoint and descriptors in the images
    keypoints1, descriptor1 = sift.detectAndCompute(img_1,None)
    keypoints2, descriptor2 = sift.detectAndCompute(img_2,None)

    # ==============================
    # ===== 2/ use bruteforce search to find a list of pairs of matched feature points
    # ==============================
    list_pairs_matched_keypoints = []
    # using cv2.BFMatcher(). It takes two optional params. First one is normType. It specifies the distance measurement to be used.
    # Second param is boolean variable, crossCheck which is false by default. If it is true, Matcher returns only those matches with value (i,j) 
    bruteforce = cv2.BFMatcher()
    # use BFMatcher.knnMatch() to get k best matches. 
    # we will take k=2 so that we can apply ratio test explained by D.Lowe in his paper.
    bestmatches = bruteforce.knnMatch(descriptor1, descriptor2, k = 2)
    matches = []
    for m,n in bestmatches:
        if m.distance < 0.75 * n.distance:
            matches.append(m)

    #print(matches)

    # queryIdx - The index or row of the kp1 interest point matrix that matches
    # trainIdx - The index or row of the kp2 interest point matrix that matches
    for match in matches:
        # Get the matching keypoints for each of the images
        img1_idx = match.queryIdx
        img2_idx = match.trainIdx
        # x - columns
        # y - rows
        # Get the coordinates
        [x1,y1] = keypoints1[img1_idx].pt
        [x2,y2] = keypoints2[img2_idx].pt

        list_pairs_matched_keypoints.append([[x1,y1], [x2,y2]])
    #print(list_pairs_matched_keypoints)
    return list_pairs_matched_keypoints


def ex_warp_blend_crop_image(img_1,H_1,img_2):
    '''
    1/ warp image img_1 using the homography H_1 to align it with image img_2 (using backward warping and bilinear resampling)
    2/ stitch image img_1 to image img_2 and apply average blending to blend the 2 images into a single panorama image
    3/ find the best bounding box for the resulting stitched image
    :param img_1:
    :param H_1:
    :param img_2:
    :return img_panorama: resulting panorama image
    '''
    img_panorama = None
    # =====  use a backward warping algorithm to warp the source
    # 1/ to do so, we first create the inverse transform; 2/ use bilinear interpolation for resampling
    # ===== blend images: average blending
    # ===== find the best bounding box for the resulting stitched image so that it will contain all pixels from 2 original images
    # It returns a tuple of number of rows, columns and channels
    rows, columns, channels = img_1.shape
    # find corners
    corner1 = np.float32([[0, 0], [0, rows-1], [columns-1, rows-1], [columns-1, 0]]).reshape(-1, 1, 2)
    # transforms every element of src by treating it as a 2D or 3D vector
    corner1Trans = np.squeeze(cv2.perspectiveTransform(corner1, H_1))
    # find all edge points
    # left most point, top most point, right most point, lowest point
    left = min(corner1Trans[0][0], corner1Trans[1][0])
    top = min(corner1Trans[0][1], corner1Trans[3][1])
    right = max(corner1Trans[2][0], corner1Trans[3][0])
    bottom = max(corner1Trans[1][1], corner1Trans[2][1])
    # calculate differences
    temp1 = (right - left, bottom - top)
    temp2 = (len(img_2[0]) - int(left), len(img_2) - int(top))
    pickMax = max(temp1, temp2)
    # warp image img_1 using the homography H_1 to align it with image img_2 
    if left < 0 and top < 0:
        warp = np.float32([[1,0, -left], [0,1, -top], [0,0,1]])
    elif left < 0:
        warp = np.float32([[1,0, -left], [0,1,0], [0,0,1]])
    elif left < 0:
        warp = np.float32([[1,0,0], [0,1, -top], [0,0,1]])
    else:
        warp = np.float32([[1,0,0], [0,1,0], [0,0,1]])
    # alignment transformation
    # Matrix product of two arrays
    img_panorama = cv2.warpPerspective(img_1, np.matmul(warp, H_1), pickMax)
    img_panorama[-int(top):-int(top)+len(img_2), -int(left):-int(left)+len(img_2[0])]=img_2
    
    return img_panorama


def stitch_images(img_1, img_2):
    '''
    :param img_1: input image 1. We warp this image to align and stich it to the image 2
    :param img_2: is the reference image. We will not warp this image
    :return img_panorama: the resulting stiched image
    '''
    print('==============================')
    print('===== stitch two images to generate one panorama image')
    print('==============================')

    # ===== extract and match features from image 1 and image 2
    list_pairs_matched_keypoints = ex_extract_and_match_feature(img_1=img_1, img_2=img_2, ratio_robustness=0.7)

    # ===== use RANSAC algorithm to find homography to warp image 1 to align it to image 2
    H_1 = ex_find_homography_ransac(list_pairs_matched_keypoints, threshold_ratio_inliers=0.85, threshold_reprojtion_error=3, max_num_trial=1000)

    # ===== warp image 1, blend it with image 2 using average blending to produce the resulting panorama image
    img_panorama = ex_warp_blend_crop_image(img_1=img_1,H_1=H_1, img_2=img_2)


    return img_panorama

if __name__ == "__main__":
    print('==================================================')
    print('PSU CS 410/510, Winter 2019, HW2: image stitching')
    print('==================================================')

    path_file_image_1 = sys.argv[1]
    path_file_image_2 = sys.argv[2]
    path_file_image_result = sys.argv[3]


    # ===== read 2 input images
    img_1 = cv2.imread(path_file_image_1)
    img_2 = cv2.imread(path_file_image_2)

    # ===== create a panorama image by stitch image 1 to image 2
    img_panorama = stitch_images(img_1=img_1, img_2=img_2)

    # ===== save panorama image
    cv2.imwrite(filename=path_file_image_result, img=(img_panorama).clip(0.0, 255.0).astype(np.uint8))

