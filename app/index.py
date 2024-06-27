import os
from PIL import Image, ImageOps
import numpy as np

def countSquares(imagePath):
    # Load the image
    image = Image.open(imagePath)

    # Convert to grayscale
    grayImage = ImageOps.grayscale(image)
    savePath = os.getcwd() + '/app/assets/images/testGray.jpg'
    grayImage.save(savePath)

    # Convert to binary (black and white)
    binaryImage = grayImage.point(lambda x: 0 if x < 128 else 255, '1')

    # Convert to numpy array for easier processing
    binaryArray = np.array(binaryImage)

    # Get image dimensions
    width, height = binaryImage.size

    # Detect vertical lines in the first row
    verticalLines = []
    for x in range(width):
        if all(binaryArray[y, x] == 0 for y in range(5)):  # Check several pixels vertically
            if not verticalLines or x - verticalLines[-1] > 1:
                verticalLines.append(x)

    # Detect horizontal lines in the first column
    horizontalLines = []
    for y in range(height):
        if all(binaryArray[y, x] == 0 for x in range(5)):  # Check several pixels horizontally
            if not horizontalLines or y - horizontalLines[-1] > 1:
                horizontalLines.append(y)

    # Calculate the number of squares
    numSquaresWidth = len(verticalLines) - 1
    numSquaresHeight = len(horizontalLines) - 1

    return numSquaresWidth, numSquaresHeight

# Specify the path to the image
imagePath = './app/assets/images/test.jpg'
countSquares(imagePath)
numSquaresWidth, numSquaresHeight = countSquares(imagePath)

print(f"Grid: {numSquaresWidth}x{numSquaresHeight}")
