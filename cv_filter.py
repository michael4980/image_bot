import cv2
import numpy as np

def laplas_filter(img, name):
    img = cv2.imread(img)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.Laplacian(gray_img, cv2.CV_64F)
    cv2.imwrite(f"images/result/{name}.png", result)

def sobel_filter(img, name):
    img = cv2.imread(img)
    img2 = np.array(img)
    strok, stolb, nums = img2.shape
    matrix4 = np.zeros((strok, stolb, nums)).astype(np.uint8)
    for i in range(strok-1):
        for j in range(stolb-1):
            m1 = abs((img2[i+1][j-1][0] + 2*img2[i+1][j][0] + img2[i+1][j+1][0]) - (img2[i-1][j-1][0] + 2*img2[i-1][j][0] + img2[i-1][j+1][0]))
            m2 = abs((img2[i-1][j+1][0] + 2*img2[i][j+1][0] + img2[i+1][j][0]) - (img2[i-1][j-1][0] + 2*img2[i][j-1][0] + img2[i+1][j-1][0]))
            Mxy = m1 + m2
            matrix4[i][j] = [Mxy, Mxy, Mxy]
    cv2.imwrite(f"images/result/{name}.png", matrix4)

def blur(img, name):
    img = cv2.imread(img)
    result = cv2.blur(img, (8,8))
    cv2.imwrite(f"images/result/{name}.png", result)

def inversion(img, name):
    img = cv2.imread(img)
    result = cv2.bitwise_not(img)
    cv2.imwrite(f"images/result/{name}.png", result)