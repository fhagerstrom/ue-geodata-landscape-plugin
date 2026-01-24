''' Main file to exec when using plugin in UE '''
import os
from tkinter import Tk, filedialog
from processGeodata import geoDataToHeightmap

def runConversion():
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
        print("No output file selected. Exiting.")
        return
    
    # Run conversion
    info = geoDataToHeightmap(inputPath, outputPath)

    # Print results
    print("Conversion completed.")
    print(f"Heightmap saved to: {outputPath}")
    print(f"Min Height: {info['minHeight']}")
    print(f"Resolution: {info['resolution']}")

if __name__ == "__main__":
    runConversion()