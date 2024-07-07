import os
from PIL import Image, ImageOps
import numpy as np

def hasBlackBorder(image):
    # Load pixel data
    pixels = image.load()
    width, height = image.size
    
    # Check the top border
    for x in range(width):
        if pixels[x, 0] != 0:
            return False
    
    # Check the bottom border
    for x in range(width):
        if pixels[x, height - 1] != 0:
            return False
    
    # Check the left border
    for y in range(height):
        if pixels[0, y] != 0:
            return False
    
    # Check the right border
    for y in range(height):
        if pixels[width - 1, y] != 0:
            return False
    
    return True

def isolateGrid(imagePath):
    # Load the image
    image = Image.open(imagePath)
    
    # Convert the image to grayscale
    grayImage = ImageOps.grayscale(image)
    savePath = os.getcwd() + '/app/assets/images/testGray.jpg'
    grayImage.save(savePath)
    
    # Convert to binary (black and white)
    binaryImage = grayImage.point(lambda x: 0 if x < 64 else 255, '1')
    
    # Create a new white image
    isolatedGrid = Image.new('1', binaryImage.size, 1)
    
    # Load pixel data
    binaryPixels = binaryImage.load()
    isolatedPixels = isolatedGrid.load()
    
    # Iterate over all pixels
    width, height = binaryImage.size
    for x in range(width):
        for y in range(height):
            if binaryPixels[x, y] == 0:  # If the pixel is black
                isolatedPixels[x, y] = 0  # Keep it black in the new image
    
    outputIsolatePath = os.getcwd() + '/app/assets/images/isolatedGrid.jpg'
    isolatedGrid.save(outputIsolatePath)

    return isolatedGrid

def countSquares(imagePath):
    # Isolate the grid on the image
    isolatedGrid = isolateGrid(imagePath)

    # Convert isolated grid to binary array
    binaryArray = isolatedGrid.load()

    # Get image dimensions
    width, height = isolatedGrid.size

    # Detect vertical lines in the first row
    verticalLines = []
    for x in range(width):
        if all(binaryArray[x, y] == 0 for y in range(5)):  # Check several pixels vertically
            if not verticalLines or x - verticalLines[-1] > 1:
                verticalLines.append(x)

    # Detect horizontal lines in the first column
    horizontalLines = []
    for y in range(height):
        if all(binaryArray[x, y] == 0 for x in range(5)):  # Check several pixels horizontally
            if not horizontalLines or y - horizontalLines[-1] > 1:
                horizontalLines.append(y)

    # Calculate the number of squares
    if hasBlackBorder(isolatedGrid):
        numSquaresWidth = len(verticalLines) - 1
        numSquaresHeight = len(horizontalLines) - 1
    else:
        numSquaresWidth = len(verticalLines) + 1
        numSquaresHeight = len(horizontalLines) + 1

    return numSquaresWidth, numSquaresHeight

# Specify the path to the image
imagePath = './app/assets/images/test11.jpg'
numSquaresWidth, numSquaresHeight = countSquares(imagePath)

print(f"Grid: width {numSquaresWidth} x height {numSquaresHeight}")