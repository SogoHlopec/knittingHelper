<?php

if (!extension_loaded('imagick')) {
    die('Imagick is not installed.');
}

function countSquares($imagePath)
{
    // Load the image
    $imagick = new Imagick($imagePath);

    // Convert to grayscale
    $imagick->setImageType(Imagick::IMGTYPE_GRAYSCALE);

    // Binarize the image
    $imagick->thresholdImage(128 * (1 << (Imagick::getQuantumDepth()['quantumDepthLong'] - 1)));

    // Get image dimensions
    $width = $imagick->getImageWidth();
    $height = $imagick->getImageHeight();

    $verticalLines = [];
    $horizontalLines = [];

    // Detect vertical lines in the first row
    for ($x = 0; $x < $width; $x++) {
        $isLine = true;
        for ($dy = 0; $dy < 5; $dy++) { // Check several pixels vertically
            $pixel = $imagick->getImagePixelColor($x, $dy);
            $color = $pixel->getColor();
            if ($color['r'] > 0) { // Not black color
                $isLine = false;
                break;
            }
        }
        if ($isLine) {
            $verticalLines[] = $x;
        }
    }

    // Detect horizontal lines in the first column
    for ($y = 0; $y < $height; $y++) {
        $isLine = true;
        for ($dx = 0; $dx < 5; $dx++) { // Check several pixels horizontally
            $pixel = $imagick->getImagePixelColor($dx, $y);
            $color = $pixel->getColor();
            if ($color['r'] > 0) { // Not black color
                $isLine = false;
                break;
            }
        }
        if ($isLine) {
            $horizontalLines[] = $y;
        }
    }

    // Remove duplicates and sort coordinates
    $verticalLines = array_unique($verticalLines);
    sort($verticalLines);
    $horizontalLines = array_unique($horizontalLines);
    sort($horizontalLines);

    // Count the number of squares
    $num_squares_width = count($verticalLines) - 1;
    $num_squares_height = count($horizontalLines) - 1;

    echo "Number of squares in width: $num_squares_width\n";
    echo "Number of squares in height: $num_squares_height\n";
}

// Specify the path to the image
$filePath = __DIR__ . '/assets/images/test.jpg';
countSquares($filePath);
