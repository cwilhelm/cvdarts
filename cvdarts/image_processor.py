import cv2
import numpy as np


def erode(captured_input):
    """
    :param captured_input: Image input that needs to be eroded
    :type captured_input: UMat
    :return: The eroded image
    :rtype: UMat
    """
    # Taking a matrix of size 5 as the kernel
    kernel = np.ones((4, 4), np.uint8)
    img_erosion = cv2.erode(captured_input, kernel, iterations=1)
    _, captured_input = cv2.threshold(img_erosion, 30, 255, cv2.THRESH_BINARY)
    return captured_input


def segment(captured_input):
    # Get binary image by applying a threshold
    captured_input = cv2.cvtColor(captured_input, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(captured_input, 30, 255, cv2.THRESH_BINARY)

    # applying morphological operation to join detached segments
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
    threshed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, rect_kernel)

    # Find contours
    contours, hierarchy = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) <= 0:
            return captured_input

    best_contour = find_best_contour(contours)

    x, y, w, h = cv2.boundingRect(best_contour)
    cv2.rectangle(captured_input, (x, y), (x + w, y + h), (255, 255, 255), 3)

    return captured_input


def find_best_contour(contours):
    # find the contour with the biggest area
    best_contour = contours[0]
    best_area = cv2.contourArea(best_contour)
    for cnt in contours:
        if cv2.contourArea(cnt) > best_area:
            best_contour = cnt
            best_area = cv2.contourArea(cnt)
    return best_contour