''' Main file to exec when using plugin in UE '''
import os
from tkinter import Tk, filedialog
from processGeodata import geoDataToHeightmap

# Import Unreal module if in Unreal environment
try:
    import unreal
    IN_UNREAL = True
except ImportError:
    unreal = None
    IN_UNREAL = False

def log(msg):
    if IN_UNREAL:
        unreal.log(msg)
    else:
        print(msg)

def runConversionWithDialog():
    # Hide root Tk window
    root = Tk()
    root.withdraw()

    # Select input TIFF file
    inputPath = filedialog.askopenfilename(title="Select input GeoTIFF file", filetypes=[("TIFF files", "*.tif;*.tiff")])

    if not inputPath:
        print("No input file selected. Exiting.")
        return

    # Output path based on input file name
    defaultOutput = os.path.splitext(inputPath)[0] + "_heightmap.png"

    outputPath = filedialog.asksaveasfilename(title="Select output PNG file", defaultextension=".png", initialfile=os.path.basename(defaultOutput), filetypes=[("PNG files", "*.png")])

    if not outputPath:
        print("No output file specified. Exiting.")
        return
    
    # Run conversion
    info = geoDataToHeightmap(inputPath, outputPath)

    # Print results
    print(f"Heightmap saved to: {outputPath}")
    print("Conversion completed.")
    print(f"Min Height: {info['minHeight']}")
    print(f"Max Height: {info['maxHeight']}")
    print(f"Resolution: {info['resolution']}")

def convertGeoDataUE(inputPath, outputPath):
    ''' Function to be called from Unreal Engine '''
    info = geoDataToHeightmap(inputPath, outputPath)
    
    # Log results in Unreal
    if IN_UNREAL:
        unreal.log(f"Heightmap saved to: {outputPath}")
        unreal.log("Conversion completed.")
        unreal.log(f"Min Height: {info['minHeight']}")
        unreal.log(f"Max Height: {info['maxHeight']}")
        unreal.log(f"Resolution: {info['resolution']}")
    else:
        print(info)

# if __name__ == "__main__":
#    runConversionWithDialog()