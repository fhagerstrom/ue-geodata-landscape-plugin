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

def loadHeightInfoFromText(pngPath):
    infoPath = os.path.splitext(pngPath)[0] + "_heightinfo.txt"

    if not os.path.exists(infoPath):
        return {}
    
    minHeight = None
    maxHeight = None

    with open(infoPath, "r") as f:
        for line in f:
            if line.startswith("minHeight="):
                minHeight = float(line.split("=")[1].strip())
            elif line.startswith("maxHeight="):
                maxHeight = float(line.split("=")[1].strip())

    if minHeight is None or maxHeight is None:
        return {}
    
    return {
        "minHeight": minHeight,
        "maxHeight": maxHeight
    }

def convertGeodataUE():
    global minHeight, maxHeight, resolution, heightmap # Variables to store results
    minHeight = None
    maxHeight = None
    resolution = None
    heightmap = None
    texture = None

    # Hide root Tk window
    root = Tk()
    root.withdraw()

    # Select input TIFF file
    inputPath = filedialog.askopenfilename(title="Select input GeoTIFF file", filetypes=[("TIFF files", "*.tif;*.tiff")])

    if not inputPath:
        print("No input file selected. Exiting.")
        return {}

    # Output path based on input file name
    defaultOutput = os.path.splitext(inputPath)[0] + "_heightmap.png"

    outputPath = filedialog.asksaveasfilename(title="Select output PNG file", defaultextension=".png", initialfile=os.path.basename(defaultOutput), filetypes=[("PNG files", "*.png")])

    if not outputPath:
        print("No output file specified. Exiting.")
        return {}
    
    # Run conversion
    unreal.log("Converting geodata...")
    info = geoDataToHeightmap(inputPath, outputPath)

    # Save min/max height info to a text file
    info_path = os.path.splitext(outputPath)[0] + "_heightinfo.txt"

    with open(info_path, "w") as f:
        f.write(f"minHeight={info['minHeight']}\n")
        f.write(f"maxHeight={info['maxHeight']}\n")

    # If in Unreal, import the generated PNG into project
    if IN_UNREAL:
        destinationPath = "/Game/Heightmaps" # Where should the asset be imported?

        task = unreal.AssetImportTask() # Create import task
        task.filename = outputPath # File in UE - Same name as output
        task.destination_path = destinationPath # Destination in UE Content Browser
        task.automated = True # No user prompt
        task.save = True # Save after import
        task.replace_existing = True # Replace if already exists

        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]) # Import the asset
    
        # If newly imported, load from imported paths
        if task.imported_object_paths:
            texture = unreal.load_asset(task.imported_object_paths[0])
        else:
            # Asset already exists, load it directly
            asset_name = os.path.splitext(os.path.basename(outputPath))[0]
            asset_path = f"{destinationPath}/{asset_name}"
            texture = unreal.load_asset(asset_path)
        
        if not texture:
            unreal.log_error("Failed to import heightmap texture into Unreal.")
            return {}

    # Assign results to global variables
    minHeight = float(info['minHeight'])
    maxHeight = float(info['maxHeight'])
    resolution = info['resolution']
    heightmap = texture

    # Log results in Unreal
    unreal.log(f"Heightmap imported: {texture.get_name()}")
    unreal.log(f"Min height: {info['minHeight']}")
    unreal.log(f"Max height: {info['maxHeight']}")
    unreal.log(f"Resolution: {info['resolution']}")