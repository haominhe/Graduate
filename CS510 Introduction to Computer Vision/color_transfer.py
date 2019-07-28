# CS510 Homework 1: Color Transfer between Images
# Haomin He
# Reference:
# http://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf
# https://www.scivision.co/numpy-image-bgr-to-rgb/
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# https://github.com/TamoghnaChattop/Fast-Color-Transfer-between-Images
# https://github.com/jrosebr1/color_transfer


import cv2
import numpy as np
import sys

def convert_color_space_BGR_to_RGB(img_BGR):
    # Return an array of zeros with the same shape and type as a given array.
    img_RGB = np.zeros_like(img_BGR,dtype=np.float32)
    img_RGB = img_BGR[...,::-1]
    return img_RGB

def convert_color_space_RGB_to_BGR(img_RGB):
    img_BGR = np.zeros_like(img_RGB,dtype=np.float32)
    img_BGR = img_RGB[..., ::-1]
    return img_BGR



def convert_color_space_RGB_to_Lab(img_RGB):
    '''
    convert image color space RGB to Lab
    converting RGB signals to Ruderman et al.’s perception-based color space lαβ
    '''
    img_LMS = np.zeros_like(img_RGB,dtype=np.float32)
    # Shape of image is accessed by img.shape. It returns a tuple of number of rows, 
    # columns and channels (if image is color)
    rows = img_RGB.shape[0]
    columns = img_RGB.shape[1]
    # lαβ is a transform of LMS cone space.
    # Transformation between RGB and LMS cone space. Using matrix from the refrenced article.
    RGB_LMS_matrix = [[0.3811, 0.5783, 0.0402],
                      [0.1967, 0.7244, 0.0782],
                      [0.0241, 0.1288, 0.8444]]
    for col in range(0, columns):
        for row in range(0, rows):
            # matmul() function returns the matrix product of two arrays. 
            img_LMS[row, col] = np.matmul(RGB_LMS_matrix, img_RGB[row, col])
            '''
            The data in this color space shows a great deal of skew,
            which we can largely eliminate by converting the data
            to logarithmic space
            '''
            img_LMS[row, col] = np.log10(img_LMS[row, col])


    img_Lab = np.zeros_like(img_RGB,dtype=np.float32)
    rows1 = img_LMS.shape[0]
    columns1 = img_LMS.shape[1]
    '''
    The three resulting orthogonal principal axes have simple forms and are close 
    to having integer coefficients.
    '''
    LMS_Lab_matrix1 = [[1/np.sqrt(3), 0, 0],
                       [0, 1/np.sqrt(6), 0],
                       [0, 0, 1/np.sqrt(2)]]
    LMS_Lab_matrix2 = [[1, 1, 1],
                       [1, 1, -2],
                       [1, -1, 0]]
    for col in range(0, columns1):
        for row in range(0, rows1):
            # matmul() function returns the matrix product of two arrays.
            img_Lab[row, col] = np.matmul(np.matmul(LMS_Lab_matrix1, LMS_Lab_matrix2), img_LMS[row, col])
            
    return img_Lab




def convert_color_space_Lab_to_RGB(img_Lab):
    '''
    convert image color space Lab to RGB
    After color processing, we must transfer the result back to RGB to display it. 
    '''
    img_LMS = np.zeros_like(img_Lab,dtype=np.float32)
    rows = img_Lab.shape[0]
    columns = img_Lab.shape[1]
    # We convert from lαβ to LMS using matrix multiplication
    Lab_LMS_matrix1 = [[1, 1, 1],
                       [1, 1, -1],
                       [1, -2, 0]]
    Lab_LMS_matrix2 = [[np.sqrt(3)/3, 0, 0],
                       [0, np.sqrt(6)/6, 0],
                       [0, 0, np.sqrt(2)/2]]
    for col in range(0, columns):
        for row in range(0, rows):
            img_LMS[row, col] = np.matmul(np.matmul(Lab_LMS_matrix1, Lab_LMS_matrix2), img_Lab[row, col])
            # we did log10 in the previous function, so we need to do power of 10
            # raising the pixel values to the power ten to go back to linear space
            img_LMS[row, col] = np.power(img_LMS[row, col], 10)


    # convert the data from LMS to RGB
    img_RGB = np.zeros_like(img_Lab,dtype=np.float32)
    rows1 = img_LMS.shape[0]
    columns1 = img_LMS.shape[1]
    LMS_RGB_matrix = [[4.4679, -3.5873, 0.1193],
                      [-1.2186, 2.3809, -0.1624],
                      [0.0497, -0.2439, 1.2045]]
    for col in range(0, columns1):
        for row in range(0, rows1):
            img_RGB[row, col] = np.matmul(LMS_RGB_matrix, img_LMS[row, col])

    return img_RGB



def calculation(source_image, target_image):
    '''
    We would like some aspects of the distribution of data points in lαβ space to transfer between
    images.
    For our purposes, the mean and standard deviations along each of the three axes suffice. Thus, we
    compute these measures for both the source and target images. 
    Note that we compute the means and standard deviations for each axis separately in lαβ space.
    '''
    # Work separately on l,a,b channels of image
    sourcel, sourcea, sourceb = cv2.split(source_image)
    sourcel = sourcel.astype("float32")
    sourcea = sourcea.astype("float32")
    sourceb = sourceb.astype("float32")

    sourceLmean = sourcel.mean()
    sourceLstd= sourcel.std()
    sourceAmean= sourcea.mean()
    sourceAstd= sourcea.std()
    sourceBmean= sourceb.mean()
    sourceBstd= sourceb.std()        

    targetl, targeta, targetb = cv2.split(target_image)
    targetl = targetl.astype("float32")
    targeta = targeta.astype("float32")
    targetb = targetb.astype("float32")

    targetLmean = targetl.mean()
    targetLstd= targetl.std()
    targetAmean= targeta.mean()
    targetAstd= targeta.std()
    targetBmean= targetb.mean()
    targetBstd= targetb.std() 

    # First, we subtract the mean from the data points
    sourcel -= sourceLmean
    sourcea -= sourceAmean
    sourceb -= sourceBmean
    # Then, we scale the data points comprising the synthetic image by factors determined by 
    # the respective standard deviations
    sourcel = (targetLstd / sourceLstd) * sourcel 
    sourcea = (targetAstd / sourceAstd) * sourcea
    sourceb = (targetBstd / sourceBstd) * sourceb
    #  We add the averages computed for the photograph. 
    sourcel += targetLmean
    sourcea += targetAmean
    sourceb += targetBmean
    # numpy.clip() function is used to Clip (limit) the values in an array.
    sourcel = np.clip(sourcel, 0, 255)
    sourcea = np.clip(sourcea, 0, 255)
    sourceb = np.clip(sourceb, 0, 255)
    # print(sourcel, sourcea, sourceb)
    new_image = cv2.merge([sourcel, sourcea, sourceb])
    return new_image



def convert_color_space_RGB_to_CIECAM97s(img_RGB):
    '''
    convert image color space RGB to CIECAM97s
    '''
    img_CIECAM97s = np.zeros_like(img_RGB,dtype=np.float32)
    # to be completed ...

    return img_CIECAM97s



def convert_color_space_CIECAM97s_to_RGB(img_CIECAM97s):
    '''
    convert image color space CIECAM97s to RGB
    '''
    img_RGB = np.zeros_like(img_CIECAM97s,dtype=np.float32)
    # to be completed ...

    return img_RGB




def color_transfer_in_Lab(img_RGB_source, img_RGB_target):
    print('===== color_transfer_in_Lab =====')
    # convert images from BGR to RGB to Lab
    source_temp1 = convert_color_space_BGR_to_RGB(img_RGB_source)
    target_temp1 = convert_color_space_BGR_to_RGB(img_RGB_target)
    source_temp2 = convert_color_space_RGB_to_Lab(source_temp1)
    target_temp2 = convert_color_space_RGB_to_Lab(target_temp1)
    # do transformation calculation
    new_image = calculation(source_temp2, target_temp2)
    # convert new image back from Lab to RGB to BGR
    new_image_temp1 = convert_color_space_Lab_to_RGB(new_image)
    new_image_temp2 = convert_color_space_RGB_to_BGR(new_image_temp1)

    return new_image_temp2




def color_transfer_in_RGB(img_RGB_source, img_RGB_target):
    print('===== color_transfer_in_RGB =====')
    # To show the significance of choosing the right color
    # space, we compared three different color spaces. 
    # convert images from BGR to RGB
    source_temp1 = convert_color_space_BGR_to_RGB(img_RGB_source)
    target_temp1 = convert_color_space_BGR_to_RGB(img_RGB_target)
    # do transformation calculation
    new_image = calculation(source_temp1, target_temp1)
    # convert new image back from RGB to BGR
    new_image_temp1 = convert_color_space_RGB_to_BGR(new_image)
    return new_image_temp1



def color_transfer_in_CIECAM97s(img_RGB_source, img_RGB_target):
    print('===== color_transfer_in_CIECAM97s =====')
    # to be completed ...




def color_transfer(img_RGB_source, img_RGB_target, option):
    if option == 'in_RGB':
        img_RGB_new = color_transfer_in_RGB(img_RGB_source, img_RGB_target)
    elif option == 'in_Lab':
        img_RGB_new = color_transfer_in_Lab(img_RGB_source, img_RGB_target)
    elif option == 'in_CIECAM97s':
        img_RGB_new = color_transfer_in_CIECAM97s(img_RGB_source, img_RGB_target)
    return img_RGB_new



if __name__ == "__main__":
    print('==================================================')
    print('PSU CS 410/510, Winter 2019, HW1: color transfer')
    print('==================================================')

    path_file_image_source = sys.argv[1]
    path_file_image_target = sys.argv[2]
    path_file_image_result_in_Lab = sys.argv[3]
    path_file_image_result_in_RGB = sys.argv[4]
    #path_file_image_result_in_CIECAM97s = sys.argv[5]

    # ===== read input images
    # img_RGB_source: is the image you want to change the its color
    # img_RGB_target: is the image containing the color distribution that you want to change the img_RGB_source to (transfer color of the img_RGB_target to the img_RGB_source)
    # Loads a color image.
    img_RGB_source = cv2.imread(path_file_image_source)
    img_RGB_target = cv2.imread(path_file_image_target)

    img_RGB_new_Lab       = color_transfer(img_RGB_source, img_RGB_target, option='in_Lab')
    # todo: save image to path_file_image_result_in_Lab
    # Saves an image to a specified file.
    cv2.imwrite(path_file_image_result_in_Lab, img_RGB_new_Lab)

    img_RGB_new_RGB       = color_transfer(img_RGB_source, img_RGB_target, option='in_RGB')
    # todo: save image to path_file_image_result_in_RGB
    cv2.imwrite(path_file_image_result_in_RGB, img_RGB_new_RGB)

    #img_RGB_new_CIECAM97s = color_transfer(img_RGB_source, img_RGB_target, option='in_CIECAM97s')
    # todo: save image to path_file_image_result_in_CIECAM97s
























