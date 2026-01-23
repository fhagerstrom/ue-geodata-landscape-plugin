''' Load geo data (TIFF), process it, and export into PNG format '''
import os
import numpy as np
from PIL import Image

def loadTiff(path):
    img = Image.open(path) # Open image from given path
    imgData = np.array(img).astype(np.float32) # Store in an array as a 32-bit float
    return imgData

def normalize(data):
    # Get min and max value from the data
    minHeight = float(data.min())
    maxHeight = float(data.max())

    # Check if the data has height variation
    if maxHeight - minHeight == 0:
        raise ValueError("Seems to be no height variation")
    
    # Normalize the data
    data = (data - minHeight) /  (maxHeight - minHeight)
    return data, minHeight, maxHeight

def saveAsPng(data, path):
    data_16 = (data * 65535).clip(0, 65535).astype(np.uint16) # Convert to 16-bit unsigned integer
    img = Image.fromarray(data_16) # Create image from array
    img.save(path) # Save image to given path

def geoDataToHeightmap(inputPath, outputPath):
    # Load the geo data from TIFF file
    geoData = loadTiff(inputPath)

    # Normalize the data
    normalizedData, minHeight, maxHeight = normalize(geoData)

    # Save the normalized data as PNG
    saveAsPng(normalizedData, outputPath)

    return {"minHeight": minHeight, "maxHeight": maxHeight, "resolution": normalizedData.shape} # Return data about the heightmap