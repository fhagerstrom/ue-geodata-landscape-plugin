''' Load geo data (TIFF), process it, and export into PNG format '''
import os
import numpy as np
from PIL import Image

def loadTiff(path):
    img = Image.open(path).convert("I") # Open image from given path as grayscale
    imgData = np.array(img).astype(np.float32) # Store in an array as a 32-bit float

    # Gate large maps for performance reasons
    if imgData.size < 5_000_000: # 
        # Save height values from the image into a separate file for debugging
        np.savetxt(os.path.splitext(path)[0] + "_heights.txt", imgData, fmt="%.2f")

    return imgData

def normalize(data):
    # Get min and max value from the data
    minHeight = float(data.min())
    maxHeight = float(data.max())

    heightRange = maxHeight - minHeight
    # Check if the data has height variation
    if heightRange < 1e-6:
        raise ValueError("The image has very little height variation.")
    
    # Normalize the data
    data = (data - minHeight) /  (maxHeight - minHeight)
    return data, minHeight, maxHeight

def saveAsPng(data, path):
    data_16 = (data * 65535).clip(0, 65535).astype(np.uint16) # Convert to 16-bit unsigned integer
    img = Image.fromarray(data_16, mode="I;16") # Create image from array, making sure it's 16-bit grayscale
    img.save(path) # Save image to given path

def geoDataToHeightmap(inputPath, outputPath):
    print("Starting script...\n")
    print("Choose input file in your file explorer.")

    # Load the geo data from TIFF file
    geoData = loadTiff(inputPath)

    # Normalize the data
    normalizedData, minHeight, maxHeight = normalize(geoData)

    # Save the normalized data as PNG
    saveAsPng(normalizedData, outputPath)

    return {"minHeight": minHeight, "maxHeight": maxHeight, "resolution": normalizedData.shape} # Return data about the heightmap