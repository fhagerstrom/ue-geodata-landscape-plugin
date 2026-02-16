# Geodata to Landscape - Unreal Engine Plugin Documentation

## 1. Overview
This plugin converts elevation data (`TIFF / TIF` files only) into grayscale `PNG`'s and imports them into Unreal Engine for use as Landscape heightmaps. It also calculates the recommended Landscape scale based on the imported heightmap.

- **Plugin Name:** Geodata To Landscape
- **Current Version:** 1.0.0
- **Supported Unreal Engine Version:** 5.6.1+
- **Platforms:** Windows
- **Intended Audience:** Environmental Artists, Technical Artists

### 1.1 Architecture Overview
The plugin consists of:
- An **Editor Utility Widget** (Blueprint) for user interaction.
- A Python conversion pipeline for:
    - GeoTIFF processing
    - Heightmap generation
    - Asset import into Unreal Engine project
- Bundled Python libraries:
    - NumPy
    - Pillow

---

## 2. Features
- Convert `TIFF` / `TIF` files into grayscale `PNG`'s
- Import converted `PNG` into Unreal Engine
- Give user heightmap data such as minimum / maximum height, resolution and which local path it was saved to.
- Calculate recommended landscape scale based on user inputted overall resolution

> NOTE: Landscape creation is performed manually, as Landscape Mode is not exposed through the Unreal Python API.

---

## 3. Installation

### 3.1 Requirements
- Unreal Engine version 5.6 or newer
- Windows 10 or later
- NumPy and Pillow modules (included in plugin package)

### 3.2 Installation Steps
1. Copy-paste `GeodataToLandscape` folder into `/ProjectFolder/Plugins`. If you do not have a Plugins folder in your project, create one.
2. Launch your Unreal Engine project.
3. Navigate to **Edit --> Plugins** in the top left corner.
4. Enable:
    - GeodataToLandscape
    - Python Editor Script Plugin
    - Editor Scripting Utilities
5. Restart Unreal Engine.

> NOTE: NumPy and Pillow are bundled with this plugin.

---

## 4. How To Use The Plugin

### 4.1 Open the Editor Utility Widget
1. Navigate to:
    `Tools --> Editor Utility Widgets`
2. Run `EUW_GeodataConversion`

Optionally:
1. Navigate to `Plugins/GeodataToLandscape/Blueprints/`
2. Right click `EUW_GeodataConversion` --> Run Editor Utility Widget

The conversion interface will appear as a dockable window.

### 4.2 Convert a GeoTIFF file
1. Click **Import TIFF**
2. A file dialog window will open. Select your `TIF` / `TIFF` file.
3. Choose where to save the generated `PNG`.

The plugin will:
- Convert the GeoTIFF into a grayscale heightmap PNG
- Save the PNG locally on your machine
- Import the PNG into Unreal Engine (Should be located in `/Content/Heightmaps`)
- Display:
    - Minimum height
    - Maximum height
    - Resolution
    - Local file path

### 4.3 Create a Landscape Using the Generated Heightmap
1. Open **Landscape Mode** in Unreal Engine.
2. Select **Import From File**.
3. Choose the generated PNG heightmap.
4. Note the **Overall Resolution** suggested by Unreal Engine.

> NOTE: Heightmaps must be square (e.g 2048 x 2048). Non-square heightmaps may result in incorrect landscape proportions.

### 4.4 Calculate the Recommended Landscape Scale
1. Enter the suggested **Overall Resolution** value into the widget.
2. The plugin will calculate the recommended:
    - X scale
    - Y scale
    - Z scale
3. Copy the calculated scale values into the landscape creation settings. 

### 4.5 Final Result
After applying the recommended scale, the landscape should:
- Match the real-world dimensions
- Preserve correct elevation change
- Maintain correct proportions

### 4.6 Notes and Limitations
- Heightmaps must be square.
- Assumes 1 meter per pixel precision on imported geodata.
- Tested on Windows only.
- Large `TIFF` files may take longer to process.

---

## 5. Scripting Reference

### 5.1 Widget Parameters
#### HeightmapPath (String)
Displays path to generated `PNG` file.

#### Heightmap (Texture2D)
The generated and imported `PNG` heightmap.

#### MinHeight & MaxHeight (Float)
The minimum and maximum height of the geoTIFF file.

#### HeightmapRes (Vector2D)
The given resolution of the generated `PNG` heightmap.

#### Recommended Overall Resolution (Float)
User-Input value from Landscape Mode.

#### Calculated Landscape Scale (Vector3)

Recommended X/Y/Z scale values.
- X/Y scale is based on heightmap's resolution and suggested overall resolution from Landscape Mode.
- Z scale is based on heightspan of heightmap.

---

## 6. Troubleshooting

### 6.1 Plugin Not Showing In Plugins Window
**Possible Cause:**
Unreal Engine is running while plugin was copied to the project.

**Solution:**
1. Ensure that the plugin is in `Plugins` folder.
2. Restart Unreal Engine.
3. Plugin should now show up in Plugins window, under `Project --> Editor` in the list to the left.

### 6.2 "ModuleNotFoundError: No module named 'geodataConverter'"
**Cause:**
The Python folder (including `Lib` and `site-packages`) was not included when plugin was imported.

**Solution:**
Ensure that:
- The `Python` folder exists inside the plugin directory.
- `Lib` and `site-packages` are included.

Restart Unreal Engine after correcting.

### 6.3 "ModuleNotFoundError: No module named 'numpy' or 'PIL'" or Other Module Related Errors
**Cause:**
Unreal Engine cannot find the required Python packages.

This may happen if:
 - The `site-packages` folder was not packaged correctly
 - Plugin was copied without the `Python/Lib/site-packages` directory

**Solution:**
1. Delete all folders related to NumPy and Pillow in `Python/Lib/site-packages`.
2. Install packages directly into Unreal Engine:
    - Locate Unreal's Python executable: 
    `"C:/Program Files/Epic Games/UE_*version*/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"`
3. Open Command Prompt in that directory.
4. Install NumPy and Pillow: `python -m pip install numpy pillow`
5. Restart Unreal Engine.

### 6.4 Heightmap Imports but Landscape Looks Incorrect
**Possible Causes:**
- Incorrect Overall Resolution entered in the widget.
- Heightmap is not square.
- Incorrect scale values used during Landscape creation.

**Solution:**
1. Re-import the PNG in Landscape Mode.
2. Use the recommended Overall Resolution shown by Unreal.
3. Enter that value into the widget.
4. Apply the calculated scale values _exactly_ as displayed (Use copy-paste).

