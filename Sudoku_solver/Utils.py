import cv2
import numpy as np
from tensorflow.keras.models import load_model

def initialize_prediction_model():
    '''
    Load the digit recognition model
    Arguments:
        None
    Returns:
        model: tf model that recognizes digit from 1 to 9
    '''
    model_path = 'D:\\Python\\Sudoku_solver\\digit_model.h5'
    model = load_model(model_path)
    return model

def preprocess(image):
    '''
    Preprocess the image 
    Arguments:
        image: cv2 image
    Returns:
        threshold: image with threshold
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    threshold = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    return threshold

def biggest_countour(countours):
    '''
    Find the biggest countour in the image
    Arguments:
        countours: list of countours in the image
    Returns:
        biggest: np array of position of biggest countours in the image
    '''
    biggest = np.array([])
    max_area = 0
    for i in countours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True)
            if area > max_area and len(approx)==4:
                biggest = approx
                max_area = area

    return biggest, max_area

def reorder(points):
    '''
    Reorder the position of the matrix's corner (upper left, upper right, lower left, lower right)
    Arguments:
        points: list of positions of matrix's corner
    Returns:
        points_new: list of ordered positions of matrix's corner
    '''
    points = points.reshape((4, 2))
    points_new = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    points_new[0] = points[np.argmin(add)]
    points_new[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    points_new[1] = points[np.argmin(diff)]
    points_new[2] = points[np.argmax(diff)]

    return points_new

def split_boxes(image):
    '''
    Split the matrix into 81 small squares to predict number in each square
    Arguments:
        image: the matrix to be splitted
    Returns:
        boxes: list of squares
    '''
    boxes = []
    rows = np.vsplit(image, 9)
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes

def get_prediction(boxes, model):
    '''
    Predict the number in each image
    Arguments:
        boxes: list of squares
        model: the tf model to predict digits
    Returns:
        result: list of numbers in the matrix
    '''
    result = []
    for image in boxes:
        image = cv2.resize(image, (28, 28))
        image = image/255.
        image = np.reshape(image, (28, 28, 1))
        predictions = model.predict(np.array([image]))[0]
        class_index = np.argmax(predictions)
        probability = np.max(predictions)
        if probability > 0.8:
            result.append(class_index)
        else:
            result.append(0)
    return result

def display_numbers(image, numbers, color = (0, 255, 0)):
    '''
    Display list of numbers on an image
    Arguments:
        image: the image to be displayed
        numbers: list of numbers to be displayed
        color: the color of numbers diplayed on the image
    Returns:
        image: image with numbers on which numbers are displayed
    '''
    secW = int(image.shape[1]/9)
    secH = int(image.shape[0]/9)
    for i in range(9):
        for j in range(9):
            if numbers[9*j+i] != 0:
                cv2.putText(image, str(numbers[9*j+i]), 
                    (i*secW+int(secW/2)-10, int((j+0.8)*secH)), 
                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    2, color, 2, cv2.LINE_AA)
    
    return image