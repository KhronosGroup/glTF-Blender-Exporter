
[![Blender](misc/Blender_logo.png)](http://www.blender.org/) [![glTF](misc/glTF_logo.png)](https://www.khronos.org/gltf/)  

Blender glTF 2.0 Exporter
=========================

Introduction
------------
This is the offical Khronos Blender glTF 2.0 exporter. This repository mainly contains Python scripts to export the internal Blender data structure to glTF 2.0. Furthermore, node groups are provided, which do simulate the Physically-Based Rendering (PBR) materials using the Cycles renderer. Finally, several Blender scenes are provided, which do demonstrate each feature individually. 

Feature matrix
--------------
Following table shows the current status of the exported features. The first three columns describe, if a feature belongs to glTF 2.0 (Core), if it is an approved glTF 2.0 extension (Extension) or if the extension is still under development (Experimental).  
The last three columns describe in combination the maturity of the exported feature:  
As soon as a feature is implemented, documented and tested, the exported feature data can be considered as production quality.

|Feature export     |Core |Extension|Experimental | |Implemented|Documented|Tested|
|-------------------|:---:|:-------:|:-----------:|-|:---------:|:--------:|:----:|
|Embed images       |  X  |         |             | |     X     |          |      |
|Embed buffers      |  X  |         |             | |     X     |          |      |
|Filtered objects   |  X  |         |             | |   Partly  |          |      |
|Apply modifiers    |  X  |         |             | |     X     |          |      |
|Indices type       |  X  |         |             | |     X     |          |      |
|Vertices           |  X  |         |             | |     X     |          |      |
|Normals            |  X  |         |             | |     X     |          |      |
|Tangents           |  X  |         |             | |     X     |          |      |
|Texture Coordinates|  X  |         |             | |     X     |          |      |
|Colors             |  X  |         |             | |     X     |          |      |
|Cameras            |  X  |         |             | |     X     |          |      |
|Materials PBR MR   |  X  |         |             | |     X     |          |      |
|Animations         |  X  |         |             | |     X     |          |      |
|Skinning           |  X  |         |             | |     X     |          |      |
|Morph targets      |  X  |         |             | |           |          |      |
|GLB                |  X  |         |             | |     X     |          |      |
|Materials PBR SG   |     |    X    |             | |           |          |      |
|Lights             |     |         |      X      | |     X     |          |      |
|Materials Common   |     |         |      X      | |     X     |          |      |
|Materials Displace |     |         |      X      | |     X     |          |      |

Folders
-------

[docs](docs/)  
Documentation about the Blender glTF 2.0 exporter and its usage.  
[environments](environments/)  
Location of environment maps used in the [scenes](scenes/).  
[misc](misc/)  
Miscellaneous files like logos and so on.  
[pbr_node](pbr_node/)  
Blender node groups for simulating the glTF 2.0 material model.  
[scenes](scenes/)  
Basic and enhanced scenes for testing the exporter.  
[scripts](scripts/)  
Blender Python scripts for exporting scenes to the glTF 2.0 format.  
[tests](tests/)  
Python scripts for testing the exporter itself.
