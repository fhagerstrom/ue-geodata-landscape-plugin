''' Load geo data (TIFF), process it, and export into PNG format '''
import os
import numpy as np
from PIL import Image

''' Load TIFF file from given path, convert to grayscale, and return as a 2D array of floats.
    Saved as 32 bit grayscale since GeoTIFF can have height values beyond 255.'''
def loadTiff(path):
    img = Image.open(path).convert("I") # Open image from given path as grayscale
    imgData = np.array(img).astype(np.float32) # Store in an array as a 32-bit float

    # Gate large maps for performance reasons, and because it might take a lot of space.
    if imgData.size < 10_000_000:
        # Save height values from the image into a separate file for debugging
        # Saves in same directory as image
        np.savetxt(os.path.splitext(path)[0] + "_heights_info.txt", imgData, fmt="%.2f")
        print(f"Saved height info to {os.path.splitext(path)[0] + '_heights_info.txt'}")

    return imgData

''' Normalize the height data to a 0-1 range.'''
def normalize(data):
    # Get min and max value from the data
    minHeight = float(data.min())
    maxHeight = float(data.max())

    heightRange = maxHeight - minHeight
    # Check if the data has too small height variation. If so, warn the user. 
    # Normalization later on could otherwise produce NaN values because of division by zero.
    if heightRange < 1e-6:
        print("Warning: The image has very little height variation.")
    
    # Normalize the data
    data = (data - minHeight) /  (maxHeight - minHeight)
    return data, minHeight, maxHeight

''' Load the converted heightmap info from heightmap in 16 bit format, and save it as a PNG in specified path. '''
def saveAsPng(data, path):
    data_16 = (data * 65535).clip(0, 65535).astype(np.uint16) # Convert to 16-bit unsigned integer, since UE defaults to 16-bit. Clipped for floating point rounding.
    img = Image.fromarray(data_16, mode="I;16") # Create image from array, making sure it's 16-bit grayscale
    img.save(path) # Save image to given path

''' Main function to run the converter. Opens file dialogs for input and output paths, normalizes the data, and saves the heightmap. '''
def geoDataToHeightmap(inputPath, outputPath):
    print("Starting converter script...\n")
    print("Choose input file in your file explorer.")

    # Load the geo data from TIFF file
    geoData = loadTiff(inputPath)

    # Normalize the data
    normalizedData, minHeight, maxHeight = normalize(geoData)

    # Save the normalized data as PNG
    saveAsPng(normalizedData, outputPath)

    return {"minHeight": minHeight, "maxHeight": maxHeight, "resolution": normalizedData.shape} # Return data about the heightmap