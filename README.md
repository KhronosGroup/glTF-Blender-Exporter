
[![Blender](misc/Blender_logo.png)](http://www.blender.org/) [![glTF](misc/glTF_logo.png)](https://www.khronos.org/gltf/)  

Blender glTF 2.0 Exporter
=========================

Introduction
------------
This is the offical Khronos Blender glTF 2.0 exporter. This repository mainly contains Python scripts to export the internal Blender data structure to glTF 2.0. Furthermore, node groups are provided, which do simulate the Physically-Based Rendering (PBR) materials using the Cycles renderer. Finally, several Blender scenes are provided, which do demonstrate each feature individually. 

Installation
------------
At point of writing, the Khronos glTF 2.0 exporter is not part of any offical, community or testing Blender add-on, which can be activated in the "User Preferences ..." Add-ons tab.  
Because of this, the exporter has to be added manually, which is described in the [scripts](scripts/) section.

Feature matrix
--------------
Following table shows the belonging of the exported features. The first three columns describe, if a feature belongs to glTF 2.0 (Core), if it is an approved glTF 2.0 extension (Extension) or if the extension is still under development (Experimental).

|Feature export     |Core |Extension|Experimental |
|-------------------|:---:|:-------:|:-----------:|
|Embed images       |  X  |         |             |
|Embed buffers      |  X  |         |             |
|Filtered objects   |  X  |         |             |
|Apply modifiers    |  X  |         |             |
|Indices type       |  X  |         |             |
|Vertices           |  X  |         |             |
|Normals            |  X  |         |             |
|Tangents           |  X  |         |             |
|Texture Coordinates|  X  |         |             |
|Colors             |  X  |         |             |
|Cameras            |  X  |         |             |
|Materials PBR MR   |  X  |         |             |
|Animations         |  X  |         |             |
|Skinning           |  X  |         |             |
|Morph targets      |  X  |         |             |
|GLB                |  X  |         |             |
|Extras             |  X  |         |             |
|Materials PBR SG   |     |    X    |             |
|Lights             |     |         |      X      |
|Materials Common   |     |         |      X      |
|Materials Displace |     |         |      X      |

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
