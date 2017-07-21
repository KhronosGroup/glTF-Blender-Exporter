Developer Documentation
-----------------------

### Preface

In general, the main documentation for developers can be found inside the source files and its functions.
The goal of this document is to provide an understanding for the concept of the exporter.  

### File organisation and description

The Blender glTF 2.0 exporter consists out of nine Python scripts in total. In general, the functions are separated into theses files by their tasks they have to process. The following sections give an overview, what these files and function do.

#### __init__.py

File to initialize the glTF 2.0 exporter package.  
The structure of this file is like the one from other Blender exporters. It is mainly for gathering and storing the exporter settings plus creating the UI for these settings. This file is shared for both `.gltf` and `.glb` export but does have two separate entry points.  
Both call the function `gltf2_export.save()` to export the glTF 2.0 file.

#### gltf2_animate.py

All animation data is gathered and converted in this module.

#### gltf2_create.py

Any binary data - eiter embedded ot stored to the file system - is created in these functions. Beside building up this binary data, also the required glTF 2.0 elements and properties are generated.

#### gltf2_debug.py

The functions provided here are for debugging and profiling the exporter. The debug output is printed to the Blender console and allows output level filtering in the follwing order:  
`ERROR`, `WARNING`, `INFO`, `PROFILE`, `DEBUG`, `VERBOSE`  
The profiler allows to print out a time stamp and to measure the delta time between two given points in the code.

#### gltf2_export.py

This module is saving the generated glTF 2.0 scene either to `.gltf` and `.glb`. It prepares the Blender scene for export by setting the correct frame and mode. Furthermore, temporary helper containers are created and the exported Blender obbjects gathered.  
After the glTF 2.0 scene was created and stored to the filesystem, temporary data is destroyed and previous, important states set back to its original state.

#### gltf2_extract.py

Here, mainly data of the meshes and and its primitives are extracted. Furthermore, all functions for converting to the glTF 2.0 coordinate system are placed here as well.

#### gltf2_filter.py

The purpose of this module is to filter and gather all Blender objects, which need to be exported depending on the settings. Furthermore, in some cases, meshes need to be converted depending on its setting and this also happens during the filtering process. 

#### gltf2_generate.py

In this module, the main glTF 2.0 scene is generated. All top level elements of a glTF 2.0 file are gathered and stored in the JSON structure.

#### gltf2_get.py

glTF 2.0 is referencing other elements by an index and not by a name anymore. The functions provide a convenient method to gather the index of a specific glTF 2.0 element. If the element can not be found, the functions always returns `-1` and never crashes.

### Implementation Details

#### Coordinate system mapping

Blender uses a right-handed coordinate system, where `x` point right, `y` point forward and `z` up. glTF 2.0 also uses a right-handed coordinate system, but with `x` point right, `y` point up and `z` backward.  

To map from Blender to glTF 2.0, the following mapping for meshes is used:

|Blender|glTF 2.0|
|:-----:|:------:|
|x      |x       |
|y      |z       |
|z      |-y      |

Depending on this mapping, following transformation rules for nodes - not joints - exist:

|Blender|glTF 2.0|Translate|Rotate|Scale|
|:-----:|--------|:-------:|:----:|:----|
|x      |        |x        |x     |x    |
|y      |        |z        |z     |z    |
|z      |        |-y       |-y    |y    |
|w      |        |         |w     |     |

Any Euler or Angle rotation is first converted to a Quaternion rotation. For quaternions, in Blender, `w` is located at first position of the vector. During the conversion, `w` is put at the end of vector, to be compliant with glTF 2.0.

### References

#### glTF 2.0 specifications
[glTF 2.0](https://github.com/KhronosGroup/glTF)

#### Blender integration requirements
[Requirements for contributed Scripts](https://wiki.blender.org/index.php/Dev:Py/Scripts/Guidelines/Addons)  
[Addons](https://wiki.blender.org/index.php/Dev:Doc/Process/Addons)  
